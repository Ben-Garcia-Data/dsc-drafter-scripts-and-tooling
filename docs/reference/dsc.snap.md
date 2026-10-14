# dsc.snap

Snap targets: attachment chords and free rig connection faces.

## `chord(point: object, side: str = 'bottom') -> object`

The nearest truss/pipe attachment chord within snap range of point=(x, y) mm,
or None. side is 'bottom' (things that hang, the default) or 'top' (things
that lift, e.g. a hoist). Returns {member, point (x, y, z) mm, z mm}.

## `connection_faces(member: object = None) -> list`

Free end-to-end connection faces of rig members: every one in the document,
or — given a `member` (object or id) — the free faces across its connected
span. Each is {member, index, point (x, y, z) mm, direction, width, height, free}.

## `member_end(point: object) -> dict`

Where one end of a point-to-point member run lands for a cursor at
point=(x, y) mm - the Truss tool's Straight-mode click rule, and what
place_truss_between(connect=True) does to each end. Returns {point: (x, y)
mm, face: the free connection face it joins or None, on_chord: True when it
landed on a member's chord instead}. Of a face and a chord, the closer wins.

## `truss_face(point: object) -> object`

The free connection face a truss placement would snap to at point=(x, y) mm —
the nearest free face across the span of the truss under the cursor — or None.
Feed it to place_truss for explicit control over the auto-snap.
