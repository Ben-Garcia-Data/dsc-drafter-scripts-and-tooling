# dsc.ops.dimension

Dimensions: place linear / aligned / radius dimensions through the same layer the dimension tools commit.

## `aligned(p1: object, p2: object, line_point: object, *, canvas: object = None) -> object`

Aligned dimension: measures the full straight-line distance p1->p2, with the
dimension line running parallel to the span and passing through line_point.
All points are (x, y) in mm. Returns the dimension object.
Example: dsc.ops.dimension.aligned((0, 0), (1000, 500), (300, 600))

## `linear(p1: object, p2: object, line_point: object, angle: object = None, *, canvas: object = None) -> object`

Linear dimension measuring p1->p2 along a fixed axis; the dimension line
passes through line_point. All points are (x, y) in mm. `angle` is the
measurement axis in degrees CCW; omit it (None) to pick horizontal or
vertical automatically from which way line_point is pulled — the classic
DIMLINEAR behaviour. Returns the dimension object.
Example: dsc.ops.dimension.linear((0, 0), (1000, 0), (500, -300))

## `radius(center: object, arc_point: object, *, canvas: object = None) -> object`

Radius dimension: a leader from a point on a circle/arc back to its centre,
labelled 'R<value>'. center and arc_point are (x, y) in mm; the distance
between them is the radius. Returns the dimension object.
Example: dsc.ops.dimension.radius((0, 0), (250, 0))
