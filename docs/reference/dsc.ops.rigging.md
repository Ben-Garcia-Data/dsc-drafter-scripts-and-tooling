# dsc.ops.rigging

Rigging: place truss and hoists through the same layer the Truss / Hoist tools commit.

## `hang(object: object, at: object = None, side: str = 'bottom', lift: bool = True, *, member: object = None, offset: object = None, t: object = None, chord: object = None, span: bool = False) -> bool`

Hang an existing object (fixture, hoist, anything) on a truss/pipe chord.
side is 'bottom' (hang under, the default) or 'top' (rest on / lift by).
Two ways to say where:
  snap (no member) - the chord within snap range of at=(x, y) mm, else of
      the object's own position; lift raises it to the chord's elevation.
      Returns False when no chord is near.
  member=truss - explicit, and MOVES the object there: offset= mm from the
      member's start face, or t= 0..1; span=True measures along the whole
      connected run (see span()). With neither, the object's position (or
      at=) is projected onto the member. chord= picks which chord, counted
      from the left looking along the member/run from its start (0 = left);
      default = the chord nearest the object. A fixture's clamp lands on the
      chord and it then moves with the truss; a hoist keeps its body and
      re-runs its chain. Returns True; raises ValueError when out of range.
Example: dsc.ops.rigging.hang(fixture, member=truss, offset=1500)

## `host_of(object: object) -> object`

What an object hangs on: {object, member, offset mm from the member's start
face, point (x, y, z) mm}, or None when it is not rigged.

## `hung_objects(member: object, span: bool = False) -> list`

Everything hanging on a truss/pipe (fixtures, hoists, soft goods), sorted
along it: [{object, member, offset mm, point (x, y, z) mm}]. span=True
covers the whole connected run and measures offset along the run.
Example: [h['object'] for h in dsc.ops.rigging.hung_objects(truss, span=True)]

## `member_info(member: object) -> dict`

Geometry of a truss/pipe (a part of one resolves to it). Returns {member,
kind 'truss'|'pipe', start, end (x, y, z) mm = centre line from face 0 to
face 1, direction, up, length, width, height, chord_diameter mm, shape,
bottom_chords / top_chords [{chord, a, b}] (chord = the index hang() takes,
0 = leftmost looking from start to end), connected [member at start, member
at end] (None = free), run_length mm of its whole connected run}.
Example: info = dsc.ops.rigging.member_info(truss); info['length']

## `place_hoist(at: object = None, insert_height: float = 1000.0, attach: bool = True, *, member: object = None, offset: object = None, t: object = None, span: bool = False, rotation: float = 0.0, preset: object = None, canvas: object = None) -> object`

Place a chain hoist. insert_height (mm, default 1000) is the motor body's
world elevation; the chain drops from it to the truss's TOP chord.
Two ways to say where:
  at=(x, y) mm  - snaps to a truss under the point when attach=True, else
                  free-standing (chain to the ground).
  member=truss  - explicit: offset= mm from the member's start face (or t=
                  0..1); span=True measures along its whole connected run.
                  With neither, at= (if given) is projected onto it, else
                  the middle. Raises ValueError when out of range.
rotation turns the hoist about its vertical axis (degrees counter-clockwise).
preset= (a Hoist preset - dsc.presets.list('Hoist') / make) sets the model's
fields (capacity, speed, ...); insert height and chain drop still come from
the placement.
Returns the hoist.
Example: dsc.ops.rigging.place_hoist(member=truss, offset=500, insert_height=9000)

## `place_run(start: object, end: object, elevation: float = 0.0, lengths: object = None, shape: str = 'Square', width: float = 300.0, height: float = 300.0, chord_diameter: float = 50.0, name: str = '', *, canvas: object = None) -> list`

Build a straight, face-connected truss run from start=(x, y) to end=(x, y) mm
with its centre line at `elevation` mm. Pieces are standard lengths (4, 3, 2,
1, 0.5 m, longest first, plus a custom make-up piece for any remainder), or
exactly `lengths` (mm, in order; must add up to the run). Profile arguments
as place_truss. Returns the pieces in order from start to end; any of them
addresses the run (span=True).
Example: run = dsc.ops.rigging.place_run((-5000, 4000), (5000, 4000), elevation=7000)

## `place_truss(at: object, length: object = None, elevation: float = 0.0, connect: bool = True, shape: str = 'Square', width: float = 300.0, height: float = 300.0, chord_diameter: float = 50.0, name: str = '', insert_connections: bool = False, *, rotation: float = 0.0, preset: object = None, canvas: object = None) -> object`

Place a straight generic truss at plan point at=(x, y) in mm.
length/width/height/chord_diameter are mm (length defaults to 2000);
shape is a cross-section name ('Square', 'Triangle', ...). With connect=True
(the default) the piece snaps to the nearest free connection face of a truss
under the cursor and butts onto it; otherwise it is standalone at `elevation`
mm, running along +X turned by rotation (degrees counter-clockwise; ignored
when it snaps to a face). insert_connections also clamps to any overlapping
truss. preset= (a Straight Truss preset - a library truss from
dsc.presets.list, or a dsc.presets.make dict) replaces shape/width/height/
chord_diameter/name, and its length is used unless length= is given.
Returns the truss.
Example: dsc.ops.rigging.place_truss((0, 0), length=3000, rotation=45)

## `place_truss_between(start: object, end: object, elevation: float = 0.0, connect: bool = True, insert_connections: bool = False, *, shape: object = None, width: object = None, height: object = None, chord_diameter: object = None, name: str = '', preset: object = None, canvas: object = None) -> object`

Place ONE straight generic truss from start=(x, y) to end=(x, y) mm at
`elevation` mm, in any direction - the Truss tool's Straight-mode commit.
With connect=True (the default) each end lands where a Straight-mode click
would (see dsc.snap.member_end): on a free connection face, which it joins,
or on a member's chord when that is closer. shape/width/height/
chord_diameter/name stamp a cross-section; left out, the Straight Truss
type defaults apply; preset= (a Straight Truss preset) sets them instead.
Returns the truss. (For a run of stock lengths use
truss_run.)
Example: dsc.ops.rigging.place_truss_between((0, 0), (3000, 3000), elevation=6000)

## `runs(member: object = None) -> list`

Summarise every truss/pipe RUN in the drawing so you needn't recompute run
geometry from primitives. With no argument: one dict per face-connected run;
pass a truss/pipe (or a part of one) to summarise just its run. Built from the
same run model place_run / member_info / hung_objects use. Each run:
  name    - the rigging Position Name of a member, else its label, else ''
  start / end (x, y, z) mm - the run's centre line, first end to last
  trim    - centre-line elevation mm (start z)
  length  - run length mm
  profile - {kind 'truss'|'pipe', shape, width, height, chord_diameter mm}
  pieces  - the members in run order
  hoists  - [{object, id, offset mm along the run, load kg, capacity kg}]
            (load = the run's known load split evenly across its hoists; a
            first-order estimate. load/capacity are None when unknown.)
  hung_objects - [{object, id, name, offset mm, chord (bottom-chord index,
            run order, None if none), weight kg or None}] sorted along the run
  total_load kg (sum of known hung + truss self weights), weight_complete
            (False when a hung object had no weight — total_load is a floor).
Example: [(r['name'], r['length']) for r in dsc.ops.rigging.runs()]

## `span(member: object) -> list`

The face-connected run a truss/pipe belongs to, in order from one free end
to the other: [{member, offset mm (run distance where the piece starts),
length mm, reversed (the run passes it end-to-start)}]. The run distance is
what span=True offsets in hang / place_hoist / place_fixtures_along measure.
Clamp crossings (overhung truss) are a different run.

## `unhang(object: object) -> bool`

Detach an object from the truss/pipe it hangs on. It keeps its world
position (it just stops following the truss). Returns False when it was not
hanging.
Example: dsc.ops.rigging.unhang(fixture)
