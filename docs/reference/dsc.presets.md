# dsc.presets

Schema presets: named value sets for an object type's schema (a library truss is one): read, make, save to the User Library, apply.

## `apply(object: object, preset: object) -> None`

Set an equipment object's schema fields from a preset of the SAME type (only
the fields the preset holds change). Undoable with the run.
Example: dsc.presets.apply(truss, dsc.presets.list('Straight Truss', '290')[0])

## `fields(type: str) -> list`

The fields a preset of `type` can set: a list of {key, label, kind ('number' /
'integer' / 'bool' / 'text'), unit ('mm', 'deg' or ''), options (allowed text
values, empty = any), description}.
Example: [f['key'] for f in dsc.presets.fields('Straight Truss')]

## `get(item: object) -> dict`

One preset as a dict: from a dsc.presets.list / dsc.library.search result or a
(source, id) pair (read from the library), or a preset dict (validated).

## `list(type: object = None, text: str = '') -> list`

The presets in the content library, optionally of one `type` and matching
`text` (name or tags). Each is a preset dict plus {id, source, folder}.
Example: [p['name'] for p in dsc.presets.list('Straight Truss', '290')]

## `make(type: str, name: str, values: object = None) -> dict`

Build a preset dict {type, name, values}, checking every value against the
type's schema (unknown field, wrong kind or a value outside a choice raises).
Nothing is saved — pass it to save() to add it to the library.
Example: p = dsc.presets.make('Straight Truss', '400 Box — 3 m',
             {'crossSectionShape': 'Square', 'width': 400, 'height': 400,
              'chordDiameter': 50, 'length': 3000})

## `of(object: object, name: object = None) -> dict`

Capture an equipment object's current schema values as a preset dict (named
after the object unless `name` is given) — configure one, then save() it.
Example: dsc.presets.save(dsc.presets.of(truss, 'My 400 Box'), folder='Truss/Mine')

## `save(preset: object, folder: str = '') -> str`

Save a preset to the User Library under `folder` (e.g. 'Truss/Mine') — it then
lists with the type's other items, so tools pick it like any library row (the
Truss tool's picker shows a saved Straight Truss preset). Returns the row id.
Runs after the script finishes; a failed run saves nothing.
Example: dsc.presets.save(dsc.presets.make('Straight Truss', '400 Box — 3 m',
             {'width': 400, 'height': 400, 'length': 3000}), folder='Truss/Mine')

## `types() -> list`

The object type names a preset can be made for, e.g. 'Straight Truss', 'Hoist'.
