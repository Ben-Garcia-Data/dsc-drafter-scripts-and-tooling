# Reading a drawing (imported DWG / DXF)

How to work out what an imported drawing contains and how it is laid out — for an
agent over MCP or a person at the console. Everything here is read-only; use
`run_python` for the Python parts and the `screenshot` tool to look.

All coordinates are **world mm, plan X right / Y up, degrees CCW** — the same as
the rest of the `dsc` API, so a `bounds` from one call can be fed straight into
another call or into `screenshot rect=`.

## The shape of an imported DWG

| In the DWG | In DSC | What to read |
|---|---|---|
| Model space | the design canvas (`canvas=None`) | `dsc.inspect.*` with no `canvas` |
| Each paper-space layout | a sheet | `canvas='<layout name>'` |
| Layer | a **class** (`'RIG-TRUSS'` nests as RIG > TRUSS); the whole file is ONE design layer named after the file | `obj.cls.path`, the `class` key in results |
| Block definition | an **Asset**; its base point is the local origin | `dsc.inspect.blocks()`, `dsc.inspect.block(name)` |
| Block reference (INSERT) in model space | an `Actor` (type `'Actor'`, counted as `Block`) | expanded automatically by `geometry()` / `texts()`; items carry `block` |
| Block reference on a layout | exploded into a group labelled with the block name | items carry `group` |
| Attribute (ATTRIB) | a text with a `tag` | `texts()` items with `tag` |
| TEXT / MTEXT | `Text` | `texts()` |
| LWPOLYLINE, LINE, ARC, CIRCLE, ELLIPSE, SPLINE, HATCH, SOLID, WIPEOUT | the matching 2D object (SOLID / WIPEOUT → closed filled polyline) | `geometry()` |
| DIMENSION, LEADER | a composite whose parts are lines + text | `geometry()` expands them |
| Paper-space VIEWPORT | a `Viewport` on the sheet | `geometry()` kind `viewport` (scale, centre it shows) |

Two traps the inspect functions handle for you, and plain attribute reads do not:
- A block instance's `obj.bounds` is only its insertion point. Use
  `dsc.inspect.extent(obj)` for its real footprint.
- Geometry attributes (`obj['Points']`, a line's `StartPoint`) are **local** to
  the object's origin, and block contents are local to the block.
  `dsc.inspect.geometry()` returns them in world mm.

## Recipe

1. **Overview** — what is in the file, how big, which layers and blocks:
   ```python
   import dsc
   dsc.inspect.overview()
   ```
   Look at each canvas's `size` (mm), the top `classes` (the DWG layers — names
   like `TITLE`, `TEXT`, `BORDER` say a lot), `blocks` (name, instances, size)
   and `attribute_tags` (e.g. `DWG_NO`, `SCALE`, `CHANNEL` — the fields a title
   block or tag exposes).

2. **Find the separate items** — a reference file often holds many examples side
   by side (20 title blocks, a page of lighting tags):
   ```python
   for c in dsc.inspect.clusters():
       print(c['index'], c.get('frame', ''), c['size'], c['count'], c['texts'][:4])
   ```
   Tune `gap=` (mm) if items merge (smaller) or split (larger). A border around
   everything comes back first as a `frame` cluster.

3. **Look at one** — screenshot exactly that cluster:
   `screenshot` with `view="2d"`, `rect=<cluster bounds>` (or `view="sheet"`,
   `sheet="<name>"` for a layout). The picture gives the gestalt; the next steps
   give the numbers.

4. **Read its text in reading order** — labels vs values, field names, sizes:
   ```python
   c = dsc.inspect.clusters()[3]
   for t in dsc.inspect.texts(region=c['bounds']):
       print(t['at'], t['height'], t.get('tag', ''), t['text'])
   ```
   Text `height` is the DWG text height in mm; labels are usually the small
   heights, values larger, titles largest.

5. **Read its geometry** — box sizes, divider positions, line weights:
   ```python
   g = dsc.inspect.geometry(of=c['objects'])
   rects = [x for x in g if x['kind'] in ('rectangle', 'polyline') and x.get('closed', True)]
   ```
   Each item has `kind`, its points in world mm, `stroke` / `weight` / `fill`,
   `class`, and `block` when it came from a block instance. Output is capped at
   `limit` with a final `{'kind': 'truncated'}` entry — narrow with `region=` or
   `of=` rather than raising the limit a lot.

6. **Blocks** — reusable parts are usually blocks; read the definition once:
   ```python
   dsc.inspect.blocks()               # every definition: size, parts, texts
   dsc.inspect.block('TB-A1')         # its geometry in block-local mm
   ```

## Describing what you found

When the goal is inspiration for our own content (see
`Documentation/Asset Research/`), record per item: overall size (mm), the grid of
boxes (row/column sizes), each field's label and whether it is a label, a fixed
value or a per-sheet value (an attribute `tag` or a token-like value), the text
heights used, and line weights for frame vs dividers. That maps directly onto
title block parts and data tag styles (`dsc.ops.paperwork`).

## Performance

The inspect calls run in C++ and are fine on 100k-object files. Prefer them to
Python loops over `doc.objects()`; pass `region=` or `of=` to keep outputs small.
