"""The Truss placement tool, rebuilt in Python as a proof of the dsc.Tool API.

This mirrors the built-in C++ TrussTool and commits through the SAME shared
rigging ops (``dsc.ops.rigging.place_truss`` / ``place_truss_between``), so a
scripted placement and a click produce the same scene objects.

Two insertion modes, switched from the options bar:

* **Library** — pick a truss (a Straight Truss schema preset) from the content library through
  the tool's ``library_picker`` (the same popup + options-bar button the C++
  tool has; it opens when the tool is activated with nothing armed, on Tab, or
  on a click with nothing armed), then single-click to place. Each click snaps
  the piece to the nearest free connection face across the truss under the
  cursor (``dsc.snap.truss_face``) and butts it on, or drops a standalone piece
  at the cursor. Ctrl+wheel turns a standalone piece before the click
  (``placement_rotation``; Shift+Ctrl for the fine step).
* **Straight** — a two-click (or click-drag) run of one piece between the two
  points, in any direction, at the Elevation option. Each end lands on, and
  joins, a free connection face under it. After the first click, Tab / digits
  give typed exact entry: length, then compass bearing (0 = up, clockwise).

Options (same keys/labels/semantics as the C++ tool): Length (Library-mode
piece length, overridden by the picked truss), Elevation (Straight-mode
placement height), Insert Connections (clamp to overlapping truss).

Works in the 2D plan AND the 3D view (``surface = "both"``, work-plane points
in 3D), like the built-in tool. Straight mode returns its first click from
``drawing_anchor`` so the host draws axis guides from it and the arrow keys lock
the run to X / Y. The previews probe ``dsc.snap.truss_face`` on every move;
that lookup is a cached index, not a rescan of the drawing.
"""

import math

import dsc

_TOOL_ID = None

# The content type of the generic-truss library rows (the TrussPickerPopup filter).
_TRUSS_TYPE = "Straight Truss"
# The built-in Straight mode previews a 300 mm wide footprint.
_STRAIGHT_PREVIEW_WIDTH = 300.0
# The built-in placement crosshair (Straight mode, before the first click).
_CROSS_SIZE, _CROSS_TICK = 50.0, 15.0


def _dist(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])


def _bearing_deg(dx, dy):
    """Compass bearing (0 = up, clockwise-positive), folded to [0, 360)."""
    return math.degrees(math.atan2(dx, dy)) % 360.0


def _polar(origin, length, bearing_deg):
    rad = math.radians(bearing_deg)
    return (origin[0] + length * math.sin(rad), origin[1] + length * math.cos(rad))


def _xy(p):
    return (p[0], p[1])


def _band(a, b, width):
    """Closed footprint rectangle of `width` around the segment a -> b."""
    length = _dist(a, b)
    if length < 1e-6:
        return None
    hw = width * 0.5
    nx, ny = -(b[1] - a[1]) / length * hw, (b[0] - a[0]) / length * hw
    return [(a[0] + nx, a[1] + ny), (b[0] + nx, b[1] + ny),
            (b[0] - nx, b[1] - ny), (a[0] - nx, a[1] - ny), (a[0] + nx, a[1] + ny)]


def _plane_line(face, width):
    """The connection-plane line across a face (twice the truss width), as the
    built-in tool draws it beside the connection diamond."""
    px, py = face["point"][0], face["point"][1]
    dx, dy = face["direction"][0], face["direction"][1]
    return [(px - dy * width, py + dx * width), (px + dy * width, py - dx * width)]


class TrussTool(dsc.Tool):
    name = "Script Truss"
    icon = ":/icons/tools/rigging/StraightTruss.svg"
    surface = "both"      # plan + 3D view, like the built-in Truss
    placement_hover = True  # Library mode is single-click: 3D preview tracks the cursor
    toolset = "Scripts"
    modes = [
        dsc.InsertionMode("Library", ":/icons/tools/rigging/InsertTruss.svg"),
        dsc.InsertionMode("Straight", ":/icons/tools/rigging/StraightTruss.svg"),
    ]
    # The built-in picker flow: popup on activate / Tab / unarmed click, an
    # options-bar button under Elevation, the armed name in the status bar.
    library_picker = dsc.LibraryPicker(_TRUSS_TYPE, title="Select Generic Truss",
                                       search_hint="Search truss…", noun="Truss",
                                       modes=["Library"])
    # Ctrl+wheel turns a standalone Library piece (Straight runs point-to-point).
    placement_rotation = ["Library"]
    # Straight mode, after the first click: length then compass bearing.
    typed_fields = [("L", "mm"), ("∠", "°")]
    options = [
        dsc.NumberOption("length", "Length", 2000.0,
                         tooltip="Library-mode piece length (overridden by the picked truss)."),
        dsc.NumberOption("elevation", "Elevation", 0.0,
                         tooltip="Straight-mode placement height above the origin."),
        dsc.BoolOption("insert_connections", "Insert Connections", False,
                       tooltip="Automatically connect to overlapping truss."),
    ]

    preset = None  # the armed Library-mode truss preset (dsc.presets dict); kept across activations

    def on_activate(self):
        self.hover = None
        self.start = None      # Straight-mode first click (on a face when snapped)

    # --- truss picker (Library mode) --------------------------------------
    def on_library_item(self, item):
        # A library truss is a Straight Truss schema preset; refuse anything else.
        preset = item.get("preset")
        if not preset or preset["type"] != "Straight Truss":
            return False
        self.preset = preset
        self.refresh()
        return True

    def _preset_value(self, key, fallback):
        return (self.preset or {}).get("values", {}).get(key, fallback)

    def on_key(self, e):
        # Tab re-opens the picker in Library mode (C++ parity). Mid-gesture in
        # Straight mode the host takes Tab for typed entry before this runs.
        if e.key == 0x01000001 and self.mode_name == "Library" and self.start is None:
            self.open_library_picker()
            return True
        return False

    def _length(self):
        length = self.option("length")
        if not length or length <= 0.0:
            length = self._preset_value("length", 2000.0)
        return length

    def _snap_end(self, p):
        """(point, face) — where a Straight-mode click at p lands: on a free
        face (joined), on a member's chord when that is closer, else at p. The
        same rule place_truss_between applies, so preview and commit agree."""
        end = dsc.snap.member_end(p)
        return _xy(end["point"]), end["face"]

    # --- events -----------------------------------------------------------
    def on_move(self, e):
        self.hover = e.point
        self.refresh()
        return True

    def on_press(self, e):
        if self.mode_name == "Straight":
            if self.start is None:
                self.start, _ = self._snap_end(e.point)
                return True
            self._straight_commit(e.point)
            return True
        return self._library_press(e)

    def on_release(self, e):
        # Click-drag in Straight mode: the release ends the run (C++ parity).
        if self.mode_name == "Straight" and self.start is not None and e.drag:
            self._straight_commit(e.point)
        return True

    def on_typed(self, values):
        if self.start is None or values[0] is None:
            self.fail("Click a start point first")
        bearing = values[1] if len(values) > 1 and values[1] is not None else 0.0
        self._straight_commit(_polar(self.start, values[0], bearing), snap_end=False)

    def _library_press(self, e):
        if self.preset is None:
            # Nothing armed yet: the click opens the picker (C++ parity).
            self.open_library_picker()
            return True
        # connect=True auto-snaps to the nearest free face; a standalone piece
        # sits at Z 0 (the elevation option drives Straight mode only), turned
        # by the Ctrl+wheel rotation, exactly as the C++ Library-mode commit.
        # preset= carries the picked truss's schema values onto the new piece.
        dsc.ops.rigging.place_truss(
            e.point,
            length=self._length(),
            elevation=0.0,
            connect=True,
            insert_connections=bool(self.option("insert_connections")),
            rotation=self.rotation,
            preset=self.preset,
        )
        self.refresh()
        return True

    def _straight_commit(self, end, snap_end=True):
        if snap_end:
            end, _ = self._snap_end(end)
        if _dist(self.start, end) < 50.0:  # the built-in minimum member (50 mm)
            self.start = None  # too short: end the run unplaced, like the C++ tool
            self.refresh()
            return
        # One piece start -> end; connect=True joins each end to the free face
        # it landed on.
        dsc.ops.rigging.place_truss_between(
            self.start, end,
            elevation=self.option("elevation") or 0.0,
            connect=True,
            insert_connections=bool(self.option("insert_connections")),
        )
        self.start = None
        self.refresh()

    def on_cancel(self):
        self.start = None
        self.refresh()

    def drawing_anchor(self):
        # Straight mode's first click (Library mode is single-click: no anchor).
        return self.start if self.mode_name == "Straight" else None

    # --- status bar -------------------------------------------------------
    def hints(self, held):
        # The built-in strip: place (click), plus Cancel mid-run. The host adds
        # the typed-entry keys (Straight, mid-run) and Ctrl+wheel (Library).
        out: list = [("click", "Place Straight Truss")]
        if self.start is not None:
            out.append((["right", "esc"], "Cancel"))
        return out

    # --- preview ----------------------------------------------------------
    def preview(self):
        if self.hover is None:
            return None
        if self.mode_name == "Straight":
            return self._straight_preview()
        return self._library_preview()

    def _straight_preview(self):
        snap = dsc.snap.member_end(self.hover)
        end, face = _xy(snap["point"]), snap["face"]
        markers, paths = [], []
        if face is not None:
            # Joining a free end face: the connection diamond + plane line.
            markers.append(end)
            paths.append(_plane_line(face, _STRAIGHT_PREVIEW_WIDTH))
        # Landing mid-member on a chord: the host's chord highlight (member
        # outline, chord, ring marker), as the built-in tool shows it.
        chord = end if snap["on_chord"] else None
        if self.start is None:
            # Before the first click: the placement crosshair + the snap chrome.
            cx, cy = end
            s, t = _CROSS_SIZE, _CROSS_TICK
            paths += [[(cx - s, cy), (cx + s, cy)], [(cx, cy - s), (cx, cy + s)],
                      [(cx + s - t, cy - t), (cx + s, cy), (cx + s - t, cy + t)]]
            return dsc.Preview(paths=paths, markers=markers, chord_snap=chord)
        band = _band(self.start, end, _STRAIGHT_PREVIEW_WIDTH)
        if band is not None:
            paths.append(band)
        dx, dy = end[0] - self.start[0], end[1] - self.start[1]
        return dsc.Preview(
            lines=[(self.start, end)], paths=paths, markers=markers, chord_snap=chord,
            readout="%s  ∠ %.1f°" % (dsc.units.format_length(_dist(self.start, end)),
                                     _bearing_deg(dx, dy)))

    def _library_preview(self):
        # A box the size of the piece, extending from a snapped face when one
        # is near, else centred on the cursor and turned by the rotation.
        if self.preset is None:
            return None
        length = self._length()
        width = self._preset_value("width", 300.0)
        face = dsc.snap.truss_face(self.hover)
        if face is not None:
            p = (face["point"][0], face["point"][1])
            d = (face["direction"][0], face["direction"][1])
            box = _band(p, (p[0] + d[0] * length, p[1] + d[1] * length), width)
            # Connection chrome, as the built-in tool: a diamond at the
            # connection point + the connection-plane line across the face.
            return dsc.Preview(paths=[box, _plane_line(face, width)], markers=[p])
        cx, cy = self.hover[0], self.hover[1]
        a = math.radians(self.rotation)
        hx, hy = math.cos(a) * length * 0.5, math.sin(a) * length * 0.5
        return dsc.Preview(paths=[_band((cx - hx, cy - hy), (cx + hx, cy + hy), width)])


def register():
    global _TOOL_ID
    _TOOL_ID = dsc.register_tool(TrussTool)


def unregister():
    if _TOOL_ID:
        dsc.unregister_tool(_TOOL_ID)
