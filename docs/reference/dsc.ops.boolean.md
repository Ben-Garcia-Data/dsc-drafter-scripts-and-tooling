# dsc.ops.boolean

Boolean: 2D shape union/difference/intersection and 3D solid CSG, the same commits the Boolean tools make.

## `combine(objects: Iterable, op: str = 'union') -> object`

Fold two or more closed 2D shapes with op='union' (default), 'difference' or
'intersection'. For 'difference' the FIRST object in the list is the subject
(objects[0] minus the rest). The operands are consumed and the result inherits
the first object's appearance and layer. Returns the new shape (the first loop
when the result splits). Raises when there are fewer than two usable shapes.
Example: dsc.ops.boolean.combine([a, b], op='difference')

## `combine_solids(objects: Iterable, op: str = 'union') -> object`

Solid CSG on two or more 3D solids (push/pull extrusions, generated solids)
with op='union' (default), 'difference' or 'intersection'. For 'difference' the
first solid is the subject. The inputs are consumed; the result is ONE new solid
inheriting the first input's layer. Meshes are read in world space, so solids at
different positions combine correctly. Raises when fewer than two produce a mesh
(an imported-model solid whose mesh lives only in the viewer cache is skipped).
Example: dsc.ops.boolean.combine_solids([a, b], op='difference')
