# dsc.ops.align

Align & distribute a set of objects — the same layout the Align & Distribute panel computes.

## `align(objects: object, x: object = None, y: object = None, z: object = None) -> int`

Align a set of objects on one or more axes. Each axis is an edge word or None:
x = 'left' | 'center' | 'right', y = 'top' | 'center' | 'bottom',
z = 'back' | 'center' | 'front' (plan Y up, Z up). Returns how many moved.
One undo step.
Example: dsc.ops.align.align(sel, x='left')

## `distribute(objects: object, x: object = None, y: object = None, z: object = None) -> int`

Evenly space a set of objects on one or more axes (needs >= 3 objects on that
axis; the two extremes stay fixed). Each axis is 'spacing' (equal gaps between
edges), 'centers' (equal stride between centres), or None. Returns how many
moved. One undo step.
Example: dsc.ops.align.distribute(sel, x='centers')
