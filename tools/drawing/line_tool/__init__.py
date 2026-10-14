"""The Line tool, rebuilt in Python as a full-parity example.

This reproduces the built-in C++ LineTool on the ``dsc.Tool`` interactive-tool
API + ``dsc.ops.draw``: two-click *and* click-drag placement, a live
length + compass-bearing readout, and typed exact-value entry (``length`` then
``angle``). The same clicks produce the same object the C++ tool commits,
because both end at ``dsc.ops.draw.line`` (the shared DrawOps layer).

Conventions (the whole public API): points are ``(x, y)`` in millimetres, plan
Y up; angles are a COMPASS BEARING — 0 deg is straight up, clockwise-positive
(90 deg right, 180 deg down) — the same convention the built-in drawing tools
read out and accept when typed.

Drop this folder in your scripts folder and enable it from the Scripts menu.
"""

import math

import dsc

_TOOL_ID = None

def _bearing_deg(dx, dy):
    """Compass bearing of the vector (dx, dy) in the plan (Y up): 0 = up,
    clockwise-positive, folded to [0, 360)."""
    deg = math.degrees(math.atan2(dx, dy))
    return deg % 360.0


def _polar(origin, length, bearing_deg):
    """Point at ``length`` mm from ``origin`` along a compass ``bearing_deg``
    (0 = up, clockwise-positive) — the inverse of _bearing_deg."""
    rad = math.radians(bearing_deg)
    return (origin[0] + length * math.sin(rad),
            origin[1] + length * math.cos(rad))


class LineTool(dsc.Tool):
    name = "Script Line"
    icon = ":/icons/tools/design/Line.svg"
    surface = "both"
    toolset = "Scripts"
    # Length, then compass bearing — matches the built-in Line's typed fields.
    typed_fields = [("L", "mm"), ("∠", "°")]

    def on_activate(self):
        self.start = None      # first endpoint, once placed
        self.hover = None     # live cursor, for the rubber band + readout

    def on_press(self, e):
        if self.start is None:
            # First click: anchor the start and begin tracking a possible drag.
            self.start = e.point
            self.hover = e.point
            return True
        # Second click of a click-click gesture: commit start -> this point.
        self._commit(self.start, e.point)
        return True

    def on_move(self, e):
        self.hover = e.point
        self.refresh()
        return True

    def on_release(self, e):
        # Click-drag: the press set the start and the host classed the gesture
        # as a drag (screen deadzone + minimum hold, like the C++ tool) ->
        # commit here. Otherwise it was a click: wait for the second click.
        if self.start is not None and e.drag:
            self._commit(self.start, e.point)
        return True

    def on_cancel(self):
        self.start = None
        self.refresh()

    def on_typed(self, values):
        # values are [length_mm, bearing_deg]; either may be None if left blank.
        if self.start is None or values[0] is None:
            self.fail("Click a start point first")
        length = values[0]
        bearing = values[1] if len(values) > 1 and values[1] is not None else 0.0
        self._commit(self.start, _polar(self.start, length, bearing))

    def drawing_anchor(self):
        # The start point while a line is pending: the host draws axis guides
        # from it and applies the arrow-key axis lock through it (C++ parity).
        return self.start

    def preview(self):
        if self.start is None or self.hover is None:
            return None
        # While typing, the host swaps the readout for the typed echo
        # ("-> L 100 mm") built from typed_fields.
        dx = self.hover[0] - self.start[0]
        dy = self.hover[1] - self.start[1]
        length = math.hypot(dx, dy)
        return dsc.Preview(
            lines=[(self.start, self.hover)],
            # Length in the document unit + compass bearing, as the built-in readout.
            readout="%s  ∠ %.1f°" % (dsc.units.format_length(length), _bearing_deg(dx, dy)),
        )

    # -- helpers ------------------------------------------------------------
    def _commit(self, start, end):
        dsc.ops.draw.line(start, end)  # zero-length is refused by the op
        self.start = None
        self.refresh()




def register():
    global _TOOL_ID
    _TOOL_ID = dsc.register_tool(LineTool)


def unregister():
    if _TOOL_ID:
        dsc.unregister_tool(_TOOL_ID)
