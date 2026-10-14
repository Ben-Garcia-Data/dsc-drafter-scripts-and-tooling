# dsc.ops.pushpull

Push/pull: extrude a closed 2D shape into a solid, the same commit the Push/Pull tool makes.

## `extrude(shape: object, distance: float) -> object`

Extrude a closed 2D shape into a solid by `distance` mm along its work-plane
normal (Z up for a shape on the ground plane). Wraps the shape into a solid and
generates its mesh in one undo step; re-extruding an existing solid sets its new
height. A negative distance extrudes the other way. Returns the solid.
Example: dsc.ops.pushpull.extrude(dsc.ops.draw.circle((0, 0), 500), 2000)
