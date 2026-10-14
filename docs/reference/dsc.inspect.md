# dsc.inspect

Read a drawing: overview, clusters of separate items, texts in reading order, world-space geometry with blocks expanded.

## `block(name: str, limit: int = 1500) -> dict`

One block definition's contents in BLOCK-LOCAL mm (origin = its base
point): name, size, local_bounds and geometry (same item format as
geometry()). Nested blocks are expanded.
Example: dsc.inspect.block('TITLE-A1')['geometry'][:20]

## `blocks(limit: int = 200) -> list`

Block definitions (a DWG block is an Asset): name, instances placed, parts
by type, size and local_bounds in block-local mm (origin = the DWG block base
point), and every text inside in reading order ('TAG=value' for attributes).

## `clusters(gap: object = None, canvas: object = None, of: object = None, frame_fraction: float = 0.6, limit: int = 60, sample_texts: int = 8) -> list`

Split a canvas into its separate drawings/items: top-level objects whose
extents come within `gap` mm of each other (default 1% of the canvas
diagonal) form one cluster. A file with 20 title-block or tag examples laid
side by side comes back as ~20 clusters. Objects spanning at least
frame_fraction of the canvas in both directions (a border around everything)
are returned as their own 'frame' clusters and not used for linking (0 turns
this off). Each cluster: index, bounds (xmin, ymin, xmax, ymax), size,
count, types, blocks, the first `sample_texts` texts in reading order,
text_count and `objects` (an ObjectSet — select it, or pass it as `of`).
Ordered top-left first. canvas: None = model space, a sheet name, or '*'.
Example: for c in dsc.inspect.clusters(): print(c['index'], c['size'], c['texts'][:3])

## `extent(obj: object) -> object`

True plan extent (xmin, ymin, xmax, ymax) in world mm of one object, block
instances and groups included (obj.bounds is only the insertion point for a
block instance). None when it has no extent.

## `find(region: object, inside: bool = False, canvas: object = None) -> object`

Top-level objects whose true extent touches region = (xmin, ymin, xmax,
ymax) mm, or lies wholly inside it with inside=True. Returns an ObjectSet.
Example: doc.select(dsc.inspect.find((0, 0, 420, 297), inside=True))

## `geometry(of: object = None, region: object = None, canvas: object = None, limit: int = 1500) -> list`

The drawn primitives of objects, in WORLD mm, with block instances and
groups expanded to their leaf shapes. Each item has `kind` plus:
  line: points [a, b]            polyline: points, closed, bulges (DWG bulge per
  rectangle: points (4), size        vertex, CCW positive; omitted when all 0)
  circle: center, radius         arc: center, radius, start, mid, end, sweep (deg)
  ellipse: center, rx, ry, rotation   spline: points (fit points), closed
  hatch: loops (list of point lists)  point: at
  text: text, at (top-left), height, rotation, box, align, tag, font
  viewport: bounds, scale, shows_center     box: bounds (anything else)
and type, id, class, stroke '#RRGGBB', weight, style, fill, block +
instance when the shape comes from a block instance, and group (a named
group's label, e.g. an exploded layout block). `of` = objects (an
ObjectSet, list or one object); default every top-level object on `canvas`.
region = (xmin, ymin, xmax, ymax) mm keeps objects whose extent touches it.
Output stops at `limit` items with a final {'kind': 'truncated'} entry.
Example: dsc.inspect.geometry(region=(0, 0, 420, 297))

## `overview(max_items: int = 30) -> dict`

What is in the open drawing, at a glance: per canvas (model space, then each
sheet) the object count, true extents and size in mm (block contents
included), counts by type and by class (an imported DWG layer is a class) and
block instance counts; then the block definitions (name, instance count, part
count, size), the total number of texts and the DWG attribute tags in use.
Lists are capped at max_items (the rest summed as '(N more)').
Example: dsc.inspect.overview()

## `text_extents(text: str, font: object = None, size: float = 12.0, bold: bool = False, italic: bool = False) -> dict`

Measure text with the SAME font metrics the drawing's text renderer uses,
so an agent laying out a table or a label knows line heights and widths in
advance. Returns {width, height, ascent, descent, line_height, lines} — all
lengths in mm, multi-line aware (embed '\n' for line breaks). `size` is a
point size as on a model-space text object (a design point = 25.4 mm; for
printed-point sheet sizing divide the result by 72). font names a family
(default the app default), bold / italic set the weight/slant. To measure a
PLACED text object's box instead, use dsc.inspect.extent(obj).
Example: dsc.inspect.text_extents('Channel 12', size=8)['line_height']

## `texts(region: object = None, canvas: object = None, of: object = None, limit: int = 400) -> list`

Every visible text in reading order (top to bottom, then left to right),
including text inside block instances and DWG attribute values. Each item:
text, at (x, y) mm = the text box's top-left anchor, height mm (the DWG text
height for imported text), rotation (deg, omitted when 0), tag (DWG
attribute tag, when it is one), block (the instance's block name), group
(a named group's label, e.g. an exploded layout block) and id.
region = (xmin, ymin, xmax, ymax) mm keeps texts whose anchor is inside it.
Example: dsc.inspect.texts(region=dsc.inspect.clusters()[0]['bounds'])
