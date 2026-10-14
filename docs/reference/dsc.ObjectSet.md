# dsc.ObjectSet

Bulk operations over many objects (use these at scale, not Python loops).

## class `ObjectSet`

An ordered set of objects. Bulk calls (set, move, delete) run in C++ — at
100k objects prefer them to a Python loop.

### `ids` (read-only)

The ids, in order.


### `first(self: dsc.ObjectSet) -> object`

The first object that still exists, or None.


### `filter(self: dsc.ObjectSet, predicate: Callable) -> dsc.ObjectSet`

Objects for which predicate(obj) is true.


### `of_type(self: dsc.ObjectSet, type: str) -> dsc.ObjectSet`

Only objects of this type name.


### `get(self: dsc.ObjectSet, attribute: str) -> list`

One value per object (raises if one lacks the attribute).


### `set(self: dsc.ObjectSet, attribute: str, value: object) -> int`

Set one attribute on every object that has it (generated parts are skipped).
Returns how many were set.


### `move(self: dsc.ObjectSet, dx: object, dy: object = None, dz: object = None) -> int`

Move every object BY a delta (dx, dy, dz) mm. Accepts move(dx, dy[, dz]) or
move((dx, dy[, dz])). Returns how many moved. Use move_to(...) for an
absolute point.


### `move_to(self: dsc.ObjectSet, x: object, y: object = None, z: object = None) -> int`

Move the whole set TO an absolute point: translate it rigidly so the centre
of the members' world origins lands at (x, y[, z]) mm (relative layout kept;
z unchanged if omitted). Accepts move_to(x, y[, z]) or move_to((x, y[, z])).
Returns how many moved.


### `delete(self: dsc.ObjectSet) -> int`

Delete every object (one bulk removal). Returns how many were removed.


### `select(self: dsc.ObjectSet) -> None`

Make these objects the canvas selection.

