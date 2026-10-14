# dsc.ops.lighting

Lighting: place library fixtures and assign DMX patch / channel / unit numbers.

## `fixtures() -> list`

Every patchable lighting fixture in the document, in document order — the
default set the patch / numbering ops act on. Returns a list of objects.

## `number_channels(start: int = 1, fixtures: object = None, sort: str = '', descending: bool = False) -> bool`

Write the console `channel` number sequentially from `start` over the
fixtures (all when None), in `sort` order (see patch). One undo step.
Returns True when anything was written.

## `patch(universe: int = 1, address: int = 1, fixtures: object = None, sort: str = '', descending: bool = False) -> bool`

Assign DMX universe/address sequentially over the fixtures (all patchable
fixtures when fixtures=None), advancing by each footprint and rolling to the
next universe past channel 512. universe/address are 1-based. `sort` orders
the fixtures first (x/y/z/position/purpose/line/serpentine/loopback/circle/
spiral); descending reverses it. One undo step. Returns True when anything
was written.
Example: dsc.ops.lighting.patch(1, 1, sort='line')

## `place_fixture(item: object, at: object = None, attach: bool = True, *, member: object = None, offset: object = None, t: object = None, chord: object = None, span: bool = False, canvas: object = None) -> object`

Place a lighting fixture from the content library. `item` is a
dsc.library.search result (its dict) or an (source_id, item_id) pair; the
asset is placed NATIVELY (converted at ingest, never here). A DSC Library
(cloud) item that isn't downloaded yet is downloaded first; the call waits
for it and raises if the download fails.
Two ways to say where:
  at=(x, y) mm  - with attach=True it hangs on the bottom chord of a
                  truss/pipe under the point when one is in snap range.
  member=truss  - explicit: hung under that member at offset= mm from its
                  start face (or t= 0..1); span=True measures along its
                  whole connected run. chord= picks the bottom chord (0 =
                  leftmost looking from the start; default 0). Raises
                  ValueError when out of range. See dsc.ops.rigging.member_info.
Returns the LightingDevice. Needs the GUI host (raises in a headless run).
Example: hit = dsc.library.search('par', type='Lighting Device')[0]
         dsc.ops.lighting.place_fixture(hit, member=truss, offset=1000)

## `place_fixtures_along(item: object, member: object, count: object = None, spacing: object = None, offsets: object = None, margin: float = 0.0, span: bool = True, chord: object = None, canvas: object = None) -> list`

Hang a row of library fixtures under a truss/pipe in one call. Give exactly
one of:
  count=N     - N fixtures evenly from `margin` to length-`margin` mm (one
                fixture = the middle);
  spacing=mm  - as many as fit inside the margins at that pitch, centred;
  offsets=[mm, ...] - exact distances from the start.
span=True (the default) lays them along the whole connected run the member
belongs to (see dsc.ops.rigging.span), crossing piece joins; span=False
uses just this member. chord= picks the bottom chord (0 = leftmost looking
from the start; default 0) and stays on the same side all along the run.
Every fixture hangs on the truss (it moves with it). Returns the fixtures
in order from the start. Needs the GUI host.
Example: par = dsc.library.search('par', type='Lighting Device')[0]
         dsc.ops.lighting.place_fixtures_along(par, truss, count=6, margin=250)

## `renumber_units(start: int = 1, fixtures: object = None, sort: str = '', descending: bool = False) -> bool`

Write the position `unitNumber` sequentially from `start` over the fixtures
(all when None), in `sort` order (see patch). One undo step. Returns True
when anything was written.
