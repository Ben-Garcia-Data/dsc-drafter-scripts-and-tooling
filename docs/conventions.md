# dsc conventions — read first

Everything in the `dsc` API follows these rules. The reference files
(`reference/*.md`) assume them.

## Units and axes

| Quantity | In the API | Notes |
|---|---|---|
| Length | millimetres (float) | Always mm, whatever unit the user displays. |
| Plan axes | X right, **Y up** (north on the plan), right-handed | The canvas shows the same orientation. |
| Elevation | Z up, mm | |
| Rotation | degrees, **counter-clockwise** seen from above (+Z) | `obj.rotation`, `obj["Rotation"]` = (x, y, z) degrees. |
| Arc / plan angles | degrees CCW from +X | `StartAngle`, `EndAngle`, … |
| Colour | `"#RRGGBB"` or `"#AARRGGBB"` | Setting also accepts `(r, g, b[, a])` or an int. Colours are **opaque** unless you give alpha: an int `<= 0xFFFFFF` (e.g. `0xFF0000`) and `"#RRGGBB"` are opaque; alpha comes only from `"#AARRGGBB"`, `(r, g, b, a)` or an int above `0xFFFFFF` (`0xAARRGGBB`). An accidental fully-transparent result (alpha 0 with no explicit alpha) raises. |

Headings shown to users in the app (the Line tool's readout) are **compass
bearings** (0° = up, clockwise). The API always uses the maths convention above.

Attributes whose unit is listed as `""` in `reference/object-types.md` are passed
through unchanged (flags, counts, enums, text, and paper sizes that are already mm).

### Text size

A text object's `FontSize` attribute is in **points at the canvas's drawing scale**,
not millimetres. On a paperwork sheet a point is a printed point (as in any
document). On the **model** canvas the drawing scale applies, so a 10 pt label is
metres tall in a 1:50 model — that is why labels drawn on the model come out
enormous. To size model text predictably, pass `size_mm=` to `dsc.ops.draw.text`
(the drawn height in mm), rather than setting `FontSize` directly.

## Documents, runs and undo

- A script, a console line and a menu command each run as **one undo step**,
  automatically. You never need to open a transaction to get undo. A run that
  changes nothing (it only reads) leaves **no** undo step.
- `with doc.transaction("Name"):` makes that block its **own** named undo step.
  An exception inside the block undoes the block (objects it created are removed)
  and then propagates.
- If a run raises, everything it did since its last completed `transaction()`
  block is undone and removed. The document is never left half-edited.
- A run can be cancelled with **Esc**, and is stopped after its time budget
  (120 s by default). Both undo the run like an exception.
- File actions — `dsc.app.open()`, `dsc.app.new()`, `doc.save()` — run
  **after** the script finishes, never mid-script. `doc.import_file()` is the
  exception: it imports immediately as its OWN undo step (what the script did
  before it is committed first, and the import is kept if the script later
  raises), so it can't be used inside `with doc.transaction()`. Exports
  (`export_dxf`, `export_mvr`, `export_sheets`, `Sheet.export_pdf` /
  `export_image`) also run immediately: they only read the drawing, return what
  they wrote and raise on failure. Time spent importing / exporting does not count
  against the run's time budget.
- A raising run rolls back **completely**: no object is left behind, and no
  survivor is left pointing at a removed layer / class / department. If your
  script reassigned an existing object's layer and then raised, that object is
  restored to its original, valid layer. Objects your script **deleted** (via
  `Object.delete()` / `ObjectSet.delete()`, including inside a `transaction()`
  block) are **recreated** with their prior state if the run then raises — a
  failed run never loses existing content.
- All `dsc` document and UI calls must run on the run's **main thread**. Do not
  start a `threading.Thread` and edit the document from it: the document is not
  thread-safe and a background-thread edit raises `RuntimeError` (and, before this
  guard, could crash the app). Do any dsc work on the thread the run started on.

## Which canvas new objects go on

New objects land on the **active canvas** — the design model space, or a paperwork
sheet. Two rules keep an AI script from putting model geometry on whatever sheet
the user happened to have open:

- **MCP `run_python` always starts on the model space** (design canvas), whatever
  sheet the GUI has active; the user's sheet is restored when the run ends. So a
  bare `dsc.ops.draw.*` / `place_*` / `duplicate` in an AI run goes on the model,
  never a sheet, unless you say otherwise. The interactive console and user scripts
  keep the active canvas as-is.
- **Every creating call takes an explicit `canvas=`** — a sheet, a sheet name or
  `doc.model_space` — that overrides the active canvas for **just that call**
  (`dsc.ops.draw.*`, rigging / lighting / staging `place_*`, `dsc.ops.dimension.*`,
  `transform.duplicate` / `mirror` / `array`, `obj.duplicate()`,
  `dsc.ops.paperwork.data_tag` / `tag_all`). It is `doc.on_canvas(canvas)` scoped
  to one line, and the previous canvas is restored afterwards.

```python
dsc.ops.draw.rectangle((0, 0), (12000, 8000))                 # on the model space
dsc.ops.draw.text((20, -20), 'NOTES', canvas='Sheet 1')       # on that sheet only (paper runs -Y)
with doc.on_canvas(plot):                                      # a block of sheet work
    dsc.ops.draw.line((0, 0), (100, 0))
```

`create_viewport` is different: it always targets its `sheet=` argument (default the
active sheet), so it has no `canvas=`.

## Collections: properties vs methods

A **simple, fixed collection** is a **property** — no parentheses:
`doc.sheets`, `doc.layers`, `doc.classes`, `doc.selection`. A **filtered or
parameterised lookup** is a **method** — it takes arguments: `doc.objects(...)`,
`doc.sheet(name)`, `doc.layer(name)`. Rule of thumb: if it takes an argument it is
a method; if it is just "all of X", it is a property.

## Moving objects

- `move(...)` moves **by a delta** (a relative offset); `move_to(...)` moves **to
  an absolute point**. Both accept either three numbers or one tuple:
  `obj.move(100, 0)` = `obj.move((100, 0))`; likewise `move_to`.
- `Object.move_to(x, y[, z])` sets the object's **origin** (its `location`) to that
  point — in the parent group's frame, world for a top-level object. `z` is kept
  when omitted.
- `ObjectSet.move_to` and `dsc.ops.transform.move_to` translate the **whole set
  rigidly** so the **centre of the members' world origins** lands on the point; the
  objects keep their relative layout.

```python
obj.move(0, -500)                       # 500 mm down (delta)
obj.move_to(1000, 1000)                 # origin to (1000, 1000)
dsc.ops.transform.move(sel, (300, 0))   # nudge a whole selection by a tuple delta
dsc.ops.transform.move_to(sel, 0, 0)    # centre the selection on the origin
```

## Objects

- `dsc.Object` holds an object's **id**, not the object. If the object is deleted
  (by your script, the user, or undo) any access raises `dsc.ObjectGone`.
  Check `obj.exists` if you need to.
- **Match on the object kind, not the Python class.** Only Line, Circle, Text,
  Group, Layer and Class have their own Python classes. Every other kind
  (fixtures, truss, hoists, decks, equipment) comes back as a plain `dsc.Object`,
  or as `dsc.Group` for composites. So `isinstance()` and `type(obj).__name__`
  miss them. Use `obj.type == "LightingDevice"`, `doc.objects(type="Hoist")` or
  `objs.of_type("RigMember")`. `reference/object-types.md` lists the kinds.
  `doc.objects(type=...)` accepts either spelling — `"LightingDevice"` or
  `"Lighting Device"` — and **raises** on a type it does not recognise (with a
  "did you mean" suggestion), rather than silently returning nothing.
- Attribute names are the names in the file format (`"Radius"`, `"StrokeColor"`).
  snake_case also works (`obj["stroke_color"]`). `obj.describe()` lists them with
  units; `reference/object-types.md` lists them for every type.
- Parts generated by a composite (dimension text, stage decks, truss meshes,
  title-block cells) are **read-only**: writing raises `dsc.ReadOnlyError`. Edit
  the composite's own attributes and it regenerates.
- The structural link attributes are **type-checked**: `"DesignLayer"` must be a
  layer, `"ObjectType"` a class, `"Department"` a department, `"ParentGroup"` a
  group, `"AttachParent"` a scene object, `"ParentAsset"` an asset — writing the
  wrong kind raises `TypeError`. `"ParentGroup"` / `"AttachParent"` also reject a
  value that would make an object its own ancestor (a cycle) with `ValueError`;
  likewise `dsc.ops.rigging.hang` refuses to hang an object on itself or on a
  member already hanging from it.
- An object inside a group stores its `location` in the group's frame;
  `world_location` and `bounds` are always world.
- A Text's `bounds` is its laid-out box (the extent the canvas draws), not just
  its insertion point.

## Sheets and screenshots

- **Sheet coordinates:** the paper's top-left sits at about (0, 0) and the paper
  runs **downward into negative Y** (a landscape A3 sheet spans roughly x 0..420,
  y 0..-297). Anything drawn at positive Y on a sheet lands *above* the paper,
  and a default sheet screenshot, framed on the paper, will not show it. Read the
  sheet's paper size (or the bounds of its existing content) before placing.
- **Sheets and viewports:** `doc.add_sheet()` makes a sheet; its `dsc.Sheet`
  `size` / `orientation` / `margins` set the page, and `width` / `height` give the
  paper in mm. A viewport is made like a user does: draw a crop shape on the design
  canvas, then `dsc.ops.paperwork.create_viewport(shape, sheet, scale=...)`.
- **3D screenshots** include the viewport chrome: the view cube, the 2D / Reset
  buttons and the scale bar. Don't mistake them for drawing content.

## 3D geometry, imported models and rotate3d

- **Bounds.** `obj.bounds` is the 2D plan box (world mm). For 3D geometry use
  `obj.bounds3d` (world) and `obj.mesh_bounds` (authored/local — the twin of a
  glTF file's accessor min/max). Both return a dict
  `{'min': (x, y, z), 'max': (x, y, z), 'size': (w, d, h), 'center': (x, y, z)}`
  in mm, plan Y up, Z up, or `None` when the object has no 3D mesh.
- **Imported model origin and axes (the trap that cost two wrong placements).**
  The 3D importer **centres each file's bounding box on the drop point** — the
  object's origin (`location` / `world_location`) is the *volumetric centre* of the
  model, not its authored origin. It also maps the file's axes into the drawing's:
  glTF/OBJ **X → plan X**, **Y (file up) → plan Z (elevation)**, **Z → plan Y**, and
  the plan Y flip (file/CAD Y-up → the plan's Y-up-north) is already applied. To see
  where the geometry sits relative to the object's origin, read `obj.mesh_center`
  (centre of the authored bounds) and `obj.pivot` (the edit-origin offset, zero
  until Set Origin is used).
- **rotate3d and Euler order.** `obj.rotate3d(axis, degrees, about=(x, y, z))`
  rotates about `axis` (`'x'`, `'y'`, `'z'` or an `(x, y, z)` vector, public
  orientation) by `degrees` **counter-clockwise seen from the +axis**, about the
  point `about` (default the object's own origin), updating **both** the object's
  `Rotation` and `Location`. The stored `Rotation` (`obj["Rotation"]`, degrees)
  composes **Z, then Y, then X (Z-Y-X)**. `rotate3d('z', d)` is the plan rotation
  `obj.rotate(d)` performs.

```python
m = doc.objects(type='SceneObject3D')[0]
print(m.bounds3d['size'], m.mesh_center)     # world extent; authored offset
m.rotate3d('x', 90, about=m.world_location)  # stand it up about its own origin
```

## Scale

Documents can hold 100 000 objects. A Python loop that touches every object is
slow; use the **bulk** calls, which run in C++:

```python
doc.objects(type="Circle").set("StrokeColor", "#FF0000")   # good
for c in doc.objects(type="Circle"):                        # slow at scale
    c["StrokeColor"] = "#FF0000"
```

## Input validation

The API rejects bad input at the call, so a mistake raises where you make it
rather than silently poisoning the drawing or spinning forever:

- **Numbers must be finite.** NaN or infinity in any coordinate, delta, angle,
  rotation, scale, dimension, size, scale factor, viewport scale/margin, or an
  attribute write (`Location`, `Rotation`, `Scale`, polyline `Points` / `Bulges`,
  …) raises `ValueError`. One non-finite object otherwise broke 2D framing.
- **Counts and sizes are bounded.** `place_fixtures_along(count=...)` and
  `array(count=...)` cap at 100000; `place_run` caps the piece count; stage decks
  and truss dimensions must be `> 0` and `<= 1 000 000 mm`. An absurd value raises
  instead of exhausting memory or freezing the app.
- **DMX numbers stay in range.** `patch()` wants `universe >= 1` and
  `address` 1..512; `number_channels` / `renumber_units` want `start >= 1` and
  raise rather than overflow to negative numbers.
- **File paths are checked first.** `doc.save_as` needs an existing folder and a
  `.DSC` name; `dsc.app.open` / `doc.import_file` need an existing file; a NUL or a
  wildly long path raises (`OSError` / `ValueError`) — the deferred action can no
  longer fail in silence or behind a modal dialog. A failed `import_file` raises.
- **A viewport crop must be a closed 2D shape** (rectangle, circle, ellipse,
  closed polyline) or a box — never a fixture, group or open line. Passing one
  raises instead of deleting it via `delete_crop`.
- **Unknown names suggest the right one.** An unknown `dsc` member or object
  attribute, and an unknown `objects(type=...)` / schedule type, raises with a
  "did you mean 'X'?" hint.

## Versioning

`dsc.API_VERSION` is semver. A plugin's `plugin.json` can require a version with
`"dsc_api": "0.2"`; the app refuses plugins that need a newer minor or another
major. Renamed attributes keep their old name as an alias for at least one minor
version. Changes are listed in `CHANGELOG.md`.