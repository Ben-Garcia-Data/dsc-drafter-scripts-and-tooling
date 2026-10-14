# dsc.ops.transform

Transform a set of objects: move / rotate / scale / mirror / duplicate / array — the same commits the transform tools make.

## `array(objects: object, count: int, dx: float = 0.0, dy: float = 0.0, dz: float = 0.0, *, canvas: object = None) -> list`

Linear array: `count` copies of the objects, copy k offset by k*(dx, dy, dz) mm
from the source. canvas= (a sheet, sheet name or doc.model_space) puts the
copies on that canvas. Returns all the new copies. One undo step.
Example: dsc.ops.transform.array(sel, 5, dx=500)

## `duplicate(objects: object, dx: float = 0.0, dy: float = 0.0, dz: float = 0.0, *, canvas: object = None) -> list`

Duplicate a set of objects, offsetting each copy by (dx, dy, dz) mm (0 = in
place). A group copies its whole subtree. canvas= (a sheet, sheet name or
doc.model_space) puts the copies on that canvas. Returns the new copies. One
undo step.

## `mirror(objects: object, start: object, end: object, copy: bool = True, *, canvas: object = None) -> list`

Mirror a set of objects across the line from start=(x, y) to end=(x, y) mm.
copy=True (default) keeps the originals and adds mirrored copies; False
reflects in place. Text mirrors too (glyphs flip). Returns the mirrored
objects (the copies when copy=True). canvas= (a sheet, sheet name or
doc.model_space) puts the copies on that canvas. One undo step.
Example: dsc.ops.transform.mirror(sel, (0, 0), (0, 1000))

## `move(objects: object, dx: object, dy: object = None, dz: object = None) -> None`

Move a set of objects BY a delta (dx, dy, dz) mm (plan Y up, Z up). Accepts
move(objects, dx, dy[, dz]) or move(objects, (dx, dy[, dz])). `objects` is an
ObjectSet, a list of objects/ids, or one object. A selected parent carries its
children, so only selection roots move. One undo step. Use move_to for an
absolute point.
Example: dsc.ops.transform.move(dsc.doc().selection, 1000, 0)

## `move_to(objects: object, x: object, y: object = None, z: object = None) -> None`

Move a set of objects TO an absolute point: translate the set rigidly so the
centre of the members' world origins lands at (x, y[, z]) mm (plan Y up, Z up;
z unchanged if omitted). Accepts move_to(objects, x, y[, z]) or
move_to(objects, (x, y[, z])). One undo step.
Example: dsc.ops.transform.move_to(sel, 0, 0)

## `rotate(objects: object, degrees: float, about: object = None) -> None`

Rotate a set of objects counter-clockwise by `degrees` about the plan point
about=(x, y) mm, or the selection's centre when about is None. The whole set
turns rigidly as a group. One undo step.
Example: dsc.ops.transform.rotate(sel, 90, about=(0, 0))

## `scale(objects: object, factor: float, about: object = None) -> None`

Uniformly scale a set of objects by `factor` (> 0) about the plan point
about=(x, y) mm, or the selection's centre when about is None. One undo step.
