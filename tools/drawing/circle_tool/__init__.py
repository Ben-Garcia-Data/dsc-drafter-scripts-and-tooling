"""The Circle / Ellipse tool, rebuilt in Python as a full-parity example.

Reproduces the built-in C++ CircleTool on the ``dsc.Tool`` API + ``dsc.ops.draw``.
The three insertion modes match the built-in tool one-for-one:

  0 - Centre     click 1 = centre, click 2 = a radius point. Always a circle.
  1 - Corner     click 1 + click 2 = opposite corners of a box. An ELLIPSE
                 inscribed in the box, or a CIRCLE while Shift is held (the box
                 is squared off to the larger span).
  2 - Axis Ends  click 1 + click 2 = the two ends of the major axis; click 3 =
                 any point, whose perpendicular distance to that axis sets the
                 minor semi-axis. A rotated ellipse.

Both click-click and click-drag placement work, Shift toggles corner circle /
ellipse live, and typed exact-value entry follows the active mode/stage (``R``
for a circle radius, ``W,H`` for the corner box, the major axis then the full
minor axis ``H`` for Axis Ends). The same clicks produce the same object the C++
tool commits, because both end at ``dsc.ops.draw.circle`` / ``.ellipse``.

Conventions (the whole public API): points are ``(x, y)`` in millimetres, plan
Y up; ``dsc.ops.draw.ellipse`` takes semi-axes in mm and a rotation in degrees
CCW; the typed major-axis angle is a compass bearing (0 = up, clockwise).
"""

import math

import dsc

_TOOL_ID = None

_EPS_MM = 1e-4
_CURVE_SEGMENTS = 96  # preview tessellation only; the committed object is exact


# -- geometry helpers -------------------------------------------------------

def _dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _sign(v):
    return -1.0 if v < 0.0 else 1.0


def _fmt(mm):
    """A length the way the built-in tools read it out: in the document's unit."""
    return dsc.units.format_length(mm)


def _bearing_deg(dx, dy):
    """Compass bearing (0 = up, clockwise-positive), folded to [0, 360)."""
    return math.degrees(math.atan2(dx, dy)) % 360.0


def _polar(origin, length, bearing_deg):
    rad = math.radians(bearing_deg)
    return (origin[0] + length * math.sin(rad),
            origin[1] + length * math.cos(rad))


def _ellipse_pts(cx, cy, rx, ry, rot_rad):
    """A closed polyline approximating an ellipse centred at (cx, cy) with
    semi-axes (rx, ry) rotated CCW by rot_rad. Used for the preview only."""
    cos_r, sin_r = math.cos(rot_rad), math.sin(rot_rad)
    pts = []
    for i in range(_CURVE_SEGMENTS + 1):
        t = 2.0 * math.pi * i / _CURVE_SEGMENTS
        lx, ly = rx * math.cos(t), ry * math.sin(t)
        pts.append((cx + lx * cos_r - ly * sin_r, cy + lx * sin_r + ly * cos_r))
    return pts


def _corner_circle(c1, c2):
    """Corner + Shift: square the box off to its larger span so the shape is a
    circle passing through the squared corner. Returns (centre, radius) or None."""
    dx, dy = c2[0] - c1[0], c2[1] - c1[1]
    side = max(abs(dx), abs(dy))
    if side < _EPS_MM:
        return None
    centre = (c1[0] + _sign(dx) * side * 0.5, c1[1] + _sign(dy) * side * 0.5)
    return centre, side * 0.5


def _box_ellipse_args(c1, c2):
    """Corner (no Shift): the ellipse inscribed in the box between two corners,
    as (centre, rx, ry, rotation_deg) for dsc.ops.draw.ellipse. The major axis
    is kept the larger semi-span (matching the built-in tool's stored values):
    a horizontal box stays at rotation 0, a taller box is stored rotated so the
    major axis is vertical. Returns None when the box is degenerate."""
    cx, cy = 0.5 * (c1[0] + c2[0]), 0.5 * (c1[1] + c2[1])
    hw, hh = 0.5 * abs(c2[0] - c1[0]), 0.5 * abs(c2[1] - c1[1])
    if hw < _EPS_MM or hh < _EPS_MM:
        return None
    if hw >= hh:
        return (cx, cy), hw, hh, 0.0
    # Taller than wide: major axis (hh) vertical. rotation -90 deg CCW keeps the
    # stored orientation identical to the C++ tool (scene rotation +pi/2).
    return (cx, cy), hh, hw, -90.0


def _perp_distance(p, origin, angle_rad):
    """Perpendicular distance from p to the line through origin at angle_rad."""
    dx, dy = p[0] - origin[0], p[1] - origin[1]
    return abs(-math.sin(angle_rad) * dx + math.cos(angle_rad) * dy)


# -- the tool ---------------------------------------------------------------

class CircleTool(dsc.Tool):
    name = "Script Circle"
    icon = ":/icons/tools/design/Circle.svg"
    surface = "both"
    toolset = "Scripts"
    modes = [
        dsc.InsertionMode("Centre", ":/icons/tools/design/Circle.svg"),
        dsc.InsertionMode("Corner", ":/icons/tools/design/circle_modes/CircleCorner.svg"),
        dsc.InsertionMode("Axis Ends", ":/icons/tools/design/circle_modes/CircleAxisEnds.svg"),
    ]
    # Up to two typed fields (R, or W,H, or the axis L,angle) — the meaning
    # follows the active mode/stage, resolved in on_typed(); preview() names
    # them per stage (typed_labels) for the host's typed echo.
    typed_fields = ["a", "b"]

    def on_activate(self):
        self._reset()
        self._last_mode = self.mode

    def _reset(self):
        self.pts = 0
        self.first = None         # centre / first corner / first axis end
        self.axis_centre = None   # mode 2, after the 2nd click
        self.second = None        # mode 2: the 2nd axis end (the rubber band's anchor)
        self.semi_major = 0.0
        self.rot_rad = 0.0
        self.hover = None
        self._shift = False

    def _sync_mode(self):
        # Switching insertion mode mid-gesture abandons the pending points
        # (parity with the built-in tool cancelling on mode change).
        m = self.mode
        if m != self._last_mode:
            self._last_mode = m
            self._reset()

    # -- events -------------------------------------------------------------
    def on_press(self, e):
        self._sync_mode()
        self._shift = "shift" in e.modifiers
        self._place_point(e.point)
        return True

    def on_move(self, e):
        self._sync_mode()
        self._shift = "shift" in e.modifiers
        self.hover = e.point
        self.refresh()
        return True

    def on_release(self, e):
        self._shift = "shift" in e.modifiers
        # Click-drag (the host's screen-deadzone + minimum-hold call, like the
        # C++ tool): the press placed a point, the release places the next.
        if self.pts >= 1 and e.drag:
            self._place_point(e.point)
        return True

    def on_key(self, e):
        # Live-toggle the corner preview between ellipse and circle as Shift is
        # tapped without moving the mouse (parity with the C++ tool).
        held = "shift" in e.modifiers
        if held != self._shift:
            self._shift = held
            self.refresh()
        return False

    def on_key_release(self, e):
        # Releasing Shift without moving the mouse drops the constraint at once.
        return self.on_key(e)

    def on_cancel(self):
        self._reset()
        self.refresh()

    def on_typed(self, values):
        self._sync_mode()
        mode = self.mode
        v0 = values[0] if values else None
        v1 = values[1] if len(values) > 1 else None

        if mode == 0 and self.pts == 1:
            if v0 is None:
                self.fail("Type a radius")
            self._commit_circle(self.first, v0)
            return

        if mode == 1 and self.pts == 1:
            sx = _sign((self.hover or self.first)[0] - self.first[0])
            sy = _sign((self.hover or self.first)[1] - self.first[1])
            if self._shift:
                if v0 is None:
                    self.fail("Type a radius")
                centre = (self.first[0] + sx * v0, self.first[1] + sy * v0)
                self._commit_circle(centre, v0)
            else:
                if v0 is None:
                    self.fail("Type a width")
                w = v0
                h = v1 if v1 is not None else v0
                c2 = (self.first[0] + sx * w, self.first[1] + sy * h)
                self._commit_box_ellipse(self.first, c2)
            return

        if mode == 2 and self.pts == 1:
            # Typed major axis: length + compass bearing places the 2nd axis end.
            if v0 is None:
                self.fail("Type the major-axis length")
            bearing = v1 if v1 is not None else 0.0
            self._place_point(_polar(self.first, v0, bearing))
            return

        if mode == 2 and self.pts == 2:
            if v0 is None:
                self.fail("Type the minor-axis length")
            self._commit_axis_ellipse(self.hover, full_minor=v0)
            return

        self.fail("Nothing to place yet")

    # -- point placement (mirrors the C++ onPointPlaced state machine) -------
    def _place_point(self, p):
        mode = self.mode

        if mode == 0:
            if self.pts == 0:
                self.first = p
                self.pts = 1
                return
            self._commit_circle(self.first, _dist(self.first, p))
            return

        if mode == 1:
            if self.pts == 0:
                self.first = p
                self.pts = 1
                return
            if self._shift:
                res = _corner_circle(self.first, p)
                if res:
                    self._commit_circle(res[0], res[1])
            else:
                self._commit_box_ellipse(self.first, p)
            return

        # mode 2 (Axis Ends)
        if self.pts == 0:
            self.first = p
            self.pts = 1
            return
        if self.pts == 1:
            dx, dy = p[0] - self.first[0], p[1] - self.first[1]
            length = math.hypot(dx, dy)
            if length < _EPS_MM:
                return  # zero-length axis: wait for a valid second end
            self.second = p
            self.axis_centre = (0.5 * (self.first[0] + p[0]),
                                0.5 * (self.first[1] + p[1]))
            self.semi_major = 0.5 * length
            self.rot_rad = math.atan2(dy, dx)
            self.pts = 2
            return
        self._commit_axis_ellipse(p)

    # -- commits ------------------------------------------------------------
    def _commit_circle(self, centre, radius):
        if radius is None or abs(radius) < _EPS_MM:
            return
        dsc.ops.draw.circle(centre, abs(radius))
        self._reset()
        self.refresh()

    def _commit_box_ellipse(self, c1, c2):
        args = _box_ellipse_args(c1, c2)
        if args is None:
            return
        (cx, cy), rx, ry, rot_deg = args
        dsc.ops.draw.ellipse((cx, cy), rx, ry, rot_deg)
        self._reset()
        self.refresh()

    def _commit_axis_ellipse(self, third, full_minor=None):
        if third is None:
            return
        b = 0.5 * full_minor if full_minor is not None \
            else _perp_distance(third, self.axis_centre, self.rot_rad)
        if b < _EPS_MM or self.semi_major < _EPS_MM:
            return
        dsc.ops.draw.ellipse(self.axis_centre, self.semi_major, b,
                             math.degrees(self.rot_rad))
        self._reset()
        self.refresh()

    # -- preview ------------------------------------------------------------
    def drawing_anchor(self):
        # The last placed point, like the built-in tool: the first click, then
        # (Axis Ends, after the 2nd click) the second axis end.
        if self.pts == 0:
            return None
        return self.second if self.pts == 2 else self.first

    def preview(self):
        self._sync_mode()
        mode = self.mode
        if self.first is None or self.hover is None:
            return None
        # Typed entry: the host swaps the readout for the typed echo, labelled
        # per stage by typed_labels (the C++ tool's R / W,H / L,angle / H).
        r_label = [("R", "mm")]

        if mode == 0 and self.pts == 1:
            r = _dist(self.first, self.hover)
            if r < _EPS_MM:
                return None
            return dsc.Preview(lines=[(self.first, self.hover)],
                               paths=[_ellipse_pts(self.first[0], self.first[1], r, r, 0.0)],
                               readout="R " + _fmt(r), typed_labels=r_label)

        if mode == 1 and self.pts == 1:
            if self._shift:
                res = _corner_circle(self.first, self.hover)
                if not res:
                    return None
                (cx, cy), r = res
                return dsc.Preview(paths=[_ellipse_pts(cx, cy, r, r, 0.0)],
                                   readout="R " + _fmt(r), typed_labels=r_label)
            args = _box_ellipse_args(self.first, self.hover)
            if args is None:
                return None
            (cx, cy), rx, ry, rot_deg = args
            w = abs(self.hover[0] - self.first[0])
            h = abs(self.hover[1] - self.first[1])
            return dsc.Preview(paths=[_ellipse_pts(cx, cy, rx, ry, math.radians(rot_deg))],
                               readout=_fmt(w) + " × " + _fmt(h),
                               typed_labels=[("W", "mm"), ("H", "mm")])

        if mode == 2 and self.pts == 1:
            length = _dist(self.first, self.hover)
            return dsc.Preview(lines=[(self.first, self.hover)],
                               readout="%s  ∠ %.1f°" % (_fmt(length), _bearing_deg(
                                   self.hover[0] - self.first[0], self.hover[1] - self.first[1])),
                               typed_labels=[("L", "mm"), ("∠", "°")])

        if mode == 2 and self.pts == 2:
            b = _perp_distance(self.hover, self.axis_centre, self.rot_rad)
            if b < _EPS_MM or self.semi_major < _EPS_MM:
                return None
            pts = _ellipse_pts(self.axis_centre[0], self.axis_centre[1],
                               self.semi_major, b, self.rot_rad)
            return dsc.Preview(lines=[(self.second, self.hover)], paths=[pts],
                               readout=_fmt(2.0 * self.semi_major) + " × " + _fmt(2.0 * b),
                               typed_labels=[("H", "mm")])
        return None


def register():
    global _TOOL_ID
    _TOOL_ID = dsc.register_tool(CircleTool)


def unregister():
    if _TOOL_ID:
        dsc.unregister_tool(_TOOL_ID)
