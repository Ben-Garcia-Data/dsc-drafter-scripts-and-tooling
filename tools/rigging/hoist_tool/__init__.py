"""The Hoist placement tool, rebuilt in Python as a dsc.Tool proof tool.

Mirrors the built-in C++ HoistTool and commits through the SAME shared op
(``dsc.ops.rigging.place_hoist``), so a scripted placement and a click produce
the same scene objects.

A hoist LIFTS a truss, so it rigs to the TOP chord: the tool opts into chord
snapping (``chord_snap = True``) on the ``top`` side, and the host feeds each
event the on-chord point plus ``e.chord`` and draws the highlight chrome. On
click the motor body is placed at the Insert Height and the chain drops to the
snapped chord; with no chord under the cursor the hoist free-stands and the
chain drops to the ground.

Like the built-in tool it works in the 2D plan AND the 3D view (``surface =
"both"``): in 3D the host feeds work-plane points (``draws_on_work_plane``
defaults on for 'both'), so the same chord snap and placement apply. It is a
single-click stamp, so it has no ``drawing_anchor``.

Ctrl+wheel turns the hoist before the click (``placement_rotation``; the host
owns the wheel, the angle readout and the hint), and the preview is the built-in
placement crosshair with a tick on the side the hoist will face.
"""

import math

import dsc

_TOOL_ID = None


class HoistTool(dsc.Tool):
    name = "Script Hoist"
    icon = ":/icons/tools/rigging/Hoist.svg"
    surface = "both"      # plan + 3D view, like the built-in Hoist
    placement_hover = True  # single-click stamp: 3D preview tracks the cursor
    toolset = "Scripts"
    chord_snap = True     # snap to a rig-member chord + get the highlight chrome
    chord_side = "top"    # a hoist lifts, so it grabs the TOP chord
    placement_rotation = True  # Ctrl+wheel turns it before the click
    options = [
        dsc.NumberOption("insert_height", "Insert Height", 1000.0,
                         tooltip="World elevation of the hoist body; the chain drops to the "
                                 "truss it lifts (or the ground)."),
    ]

    def on_activate(self):
        self.hover = None

    def on_move(self, e):
        # e.point is already the on-chord point when snapped (chord_snap lands it).
        self.hover = e.point
        self.refresh()
        return True

    def on_press(self, e):
        # attach when a chord is under the cursor; place_hoist re-finds the top
        # chord at the on-chord point and rehosts the hanging connection, exactly
        # as the C++ HoistTool does. Off a member it free-stands.
        dsc.ops.rigging.place_hoist(
            e.point,
            insert_height=self.option("insert_height") or 1000.0,
            attach=e.chord is not None,
            rotation=self.rotation,
        )
        self.refresh()
        return True

    def hints(self, held):
        # The built-in placement strip; the host appends Ctrl+wheel Rotate.
        return [("click", "Place Hoist")]

    def preview(self):
        if self.hover is None:
            return None
        # The built-in placement crosshair (50 mm arms) with a tick on the +X arm
        # showing which way the hoist will face, turned by the Ctrl+wheel
        # rotation. The chord highlight is drawn by the host from the chord snap.
        cx, cy = self.hover[0], self.hover[1]
        c, s = math.cos(math.radians(self.rotation)), math.sin(math.radians(self.rotation))

        def at(u, v):
            return (cx + u * c - v * s, cy + u * s + v * c)

        size, tick = 50.0, 15.0
        return dsc.Preview(paths=[
            [at(-size, 0.0), at(size, 0.0)],
            [at(0.0, -size), at(0.0, size)],
            [at(size - tick, -tick), at(size, 0.0), at(size - tick, tick)],
        ])


def register():
    global _TOOL_ID
    _TOOL_ID = dsc.register_tool(HoistTool)


def unregister():
    if _TOOL_ID:
        dsc.unregister_tool(_TOOL_ID)
