# dsc.ops.draw

Draw primitives: the same operations the Line / Rectangle / Circle / Text tools commit.

## `circle(center: object, radius: float, *, canvas: object = None) -> object`

Circle by centre and radius (mm).

## `ellipse(center: object, rx: float, ry: float, rotation: float = 0.0, *, canvas: object = None) -> object`

Ellipse by centre, semi-axes (mm) and rotation (degrees CCW).

## `line(start: object, end: object, *, canvas: object = None) -> object`

Line from start to end. Example: dsc.ops.draw.line((0, 0), (1000, 0))

## `polyline(points: object, closed: bool = False, *, canvas: object = None) -> object`

Polyline through (x, y) mm points with straight segments; `closed=True` makes a
closed, fillable shape (at least 3 points).
Example: dsc.ops.draw.polyline([(0, 0), (8000, 0), (4000, 6000)], closed=True)

## `rectangle(corner1: object, corner2: object, *, canvas: object = None) -> object`

Axis-aligned rectangle between two opposite corners (mm) — what the Rectangle
tool draws. Example: dsc.ops.draw.rectangle((0, 0), (12000, 8000))

## `text(top_left: object, text: str, width: float = 0.0, height: float = 0.0, *, size_mm: float = 0.0, canvas: object = None) -> object`

Text box at its top-left corner. width/height 0 = auto-size. size_mm sets the
text's drawn height in mm directly (recommended on the model canvas, where the
FontSize attribute is in DRAWING-SCALE points — a 10 pt label is metres tall in a
1:50 model); omit it to keep the default point size.
Example: dsc.ops.draw.text((0, 0), 'PLAN', size_mm=200)
