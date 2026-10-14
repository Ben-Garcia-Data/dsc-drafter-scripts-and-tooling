# dsc.library

Search the content library (symbols, fixtures, truss profiles).

## `export(item: object) -> None`

Export an asset (title block part, data tag style, symbol) or a title block
layout — bundled with every part it uses — to the User Library, as the
Library's 'Export to User Library' does; from there it publishes to the DSC
Library like any user item. Runs after the script finishes (a failed run
exports nothing); a failure shows as an app error.
Example: dsc.library.export(layout)

## `get(item: object) -> object`

Return the in-document object for a library search result, importing it as its
NATIVE definition (data tag style, title block layout / part, symbol) into the
document first if it isn't already there — the same importer the Library panel
uses on apply, inside the run's transaction. `item` is a dsc.library.search
dict, an (source, id) pair, a bare item name, or an object already in the
document (returned as-is). Raises if nothing resolves. Fixtures are placed with
geometry, so use dsc.ops.lighting.place_fixture for those.
Example: hit = dsc.library.search('Standard', type='title-block')[0]
         layout = dsc.library.get(hit)

## `search(text: str = '', type: object = None) -> list`

Search the content library. `text` matches an item's name or tags (empty =
everything); `type` filters by content type ('Lighting Device', '2d-object',
...). Returns a list of {id, source, name, type, folder, tags}.
Example: dsc.library.search('par', type='Lighting Device')
