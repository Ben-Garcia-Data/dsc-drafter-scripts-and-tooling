"""The Text tool, rebuilt in Python as a full-parity example.

Reproduces the built-in C++ TextTool on the ``dsc.Tool`` API + ``dsc.ops.draw.text``:

  * click a first corner, then click (or drag-release on) the opposite corner to
    set the text box's width and height — the same box gesture the built-in tool
    uses (click-click and click-drag both work);
  * typed exact-value entry after the first corner: ``W,H`` in mm, the signs
    taken from the cursor's quadrant, ``H`` left blank tracks the live cursor;
  * a zoom warning (``warning_for_view``) matching the built-in tool — the new
    text would be too small / too large to read at the current zoom;
  * on commit the host selects the new text and opens the inline editor on it,
    in the 2D plan or the 3D view (where it is also stamped onto the work
    plane), exactly as for the C++ tool — a tool never opens it itself.

The same clicks produce the same object the C++ tool commits, because both end
at the shared draw op: the C++ tool calls ``Ops::drawText(box)`` and this tool
calls ``dsc.ops.draw.text(top_left, "Text", w, h)``, which build an identical
TextObject (same top-left origin, width/height, and placeholder ``<p>Text</p>``).

Conventions (the whole public API): points are ``(x, y)`` in millimetres, plan
Y up, so the box's TOP-left corner is (min x, max y).

Drop this folder in your scripts folder and enable it from the Scripts menu.
"""

import dsc

_TOOL_ID = None

# Below this the box has no area on that axis; a box zero on BOTH axes is refused
# (the built-in tool waits for a valid second corner rather than committing).
_EPS_MM = 1e-4

# New text uses TextObject's 12 pt default; a point is 254 su on the design
# canvas (TextScale) and a character is roughly half as wide as it is tall. The
# host delivers view_scale as pixels-per-scene-unit, so size the readability
# check in scene units, the same maths as the C++ TextTool::warningForView.
_DEFAULT_PT = 12.0
_SU_PER_PT = 254.0          # design-canvas value (a paperwork sheet differs)
_EM_ASPECT = 0.5
_TOO_BIG_RATIO = 0.30       # > 30 % of the viewport width per character
_TOO_SMALL_RATIO = 0.01     # <  1 % of the viewport width per character




def _sign(v):
    return -1.0 if v < 0.0 else 1.0


def _box(c1, c2):
    """The text box between two corners as (top_left, width, height) in mm, plan
    Y up (top-left = min x, max y). Returns None when the box has no area on
    EITHER axis — matching the built-in tool, which then waits for a valid
    second corner instead of committing."""
    left = min(c1[0], c2[0])
    top = max(c1[1], c2[1])                # Y up: the visual top is the larger y
    width = abs(c2[0] - c1[0])
    height = abs(c2[1] - c1[1])
    if width < _EPS_MM and height < _EPS_MM:
        return None
    return (left, top), width, height


def _fmt(mm):
    """A length in the document's unit, as the built-in readouts show it."""
    return dsc.units.format_length(mm)


class TextTool(dsc.Tool):
    name = "Script Text"
    icon = ":/icons/tools/drawing/Text.svg"
    surface = "both"
    toolset = "Scripts"
    # W then H, active once the first corner is down (parity with the built-in
    # Text tool's typed fields); resolved in on_typed().
    typed_fields = [("W", "mm"), ("H", "mm")]

    def on_activate(self):
        self._reset()

    def _reset(self):
        self.first = None       # the first corner, once placed
        self.hover = None      # live cursor, for the box preview + readout

    # -- events -------------------------------------------------------------
    def on_press(self, e):
        if self.first is None:
            self.first = e.point
            self.hover = e.point
            return True
        # Second click of a click-click gesture: commit first -> this corner.
        self._commit(self.first, e.point)
        return True

    def on_move(self, e):
        self.hover = e.point
        self.refresh()
        return True

    def on_release(self, e):
        # Click-drag (the host's screen-deadzone + minimum-hold call, like the
        # C++ tool) -> commit here. A click waits for the second click.
        if self.first is not None and e.drag:
            self._commit(self.first, e.point)
        return True

    def on_cancel(self):
        self._reset()
        self.refresh()

    def on_typed(self, values):
        if self.first is None:
            self.fail("Click the first corner, then type W,H")
        w = values[0] if values else None
        if w is None:
            self.fail("Type a width")
        h = values[1] if len(values) > 1 and values[1] is not None else None
        cur = self.hover or self.first
        sx = _sign(cur[0] - self.first[0])
        sy = _sign(cur[1] - self.first[1])
        if h is None:
            h = abs(cur[1] - self.first[1])   # blank H tracks the live cursor
        c2 = (self.first[0] + sx * w, self.first[1] + sy * h)
        self._commit(self.first, c2)

    # -- preview ------------------------------------------------------------
    def drawing_anchor(self):
        # The first corner while a text box is being dragged / clicked out.
        return self.first

    def preview(self):
        if self.first is None or self.hover is None:
            return None
        box = _box(self.first, self.hover)
        # Typed entry: the host swaps the readout for the "-> W .. mm" echo.
        if box is None:
            return dsc.Preview(readout=_fmt(0.0) + " × " + _fmt(0.0))
        (left, top), w, h = box
        rect = [(left, top), (left + w, top), (left + w, top - h),
                (left, top - h), (left, top)]
        return dsc.Preview(paths=[rect], readout=_fmt(w) + " × " + _fmt(h))

    def warning_for_view(self, view_scale, width_px, height_px):
        if view_scale is None or view_scale <= 0.0 or not width_px or width_px <= 0:
            return None
        char_width_px = _DEFAULT_PT * _SU_PER_PT * _EM_ASPECT * view_scale
        ratio = char_width_px / width_px
        if ratio > _TOO_BIG_RATIO:
            return "Zoomed in too far to view text at current font size"
        if ratio < _TOO_SMALL_RATIO:
            return "Zoomed out too far to view text at current font size"
        return None

    # -- commit -------------------------------------------------------------
    def _commit(self, c1, c2):
        box = _box(c1, c2)
        if box is None:
            return  # degenerate: keep the gesture pending, like the built-in tool
        (left, top), w, h = box
        # "Text" -> "<p>Text</p>", the same placeholder the C++ tool stamps.
        # The host opens the inline editor on the placed text (2D or 3D).
        dsc.ops.draw.text((left, top), "Text", w, h)
        self._reset()
        self.refresh()


def register():
    global _TOOL_ID
    _TOOL_ID = dsc.register_tool(TextTool)


def unregister():
    if _TOOL_ID:
        dsc.unregister_tool(_TOOL_ID)
