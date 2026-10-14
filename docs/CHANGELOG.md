# dsc API changelog

## Unreleased
- Scripted tools (`dsc.Tool`) feel like the built-in ones:
  - New `drawing_anchor()` hook: return the point the pending gesture
    radiates from (e.g. the first click) and the host draws axis guides from
    it, applies the arrow-key axis lock through it and marks it.
  - New `draws_on_work_plane` attribute (default True for surface '3d' /
    'both'): the 3D view feeds the tool work-plane points, so a drawing tool
    draws in 3D as the built-in ones do.
  - Faster: the preview is re-drawn once per event (a `self.refresh()` inside
    a handler no longer doubles it), and `dsc.snap.*` / rigging calls reuse
    one cached rig-member index instead of rescanning the drawing per call.
  - New `on_key_release(e)` handler (auto-repeat filtered), so a modifier
    preview such as Circle's Shift-constrain drops the moment the key is
    released.
  - New `placement_hover` attribute: a single-click placement tool gets
    `on_move` in the 3D view before the first click (preview follows the cursor).
  - Scripted tools now have their own toolbox identity, so a Python tool that
    reuses a built-in icon no longer takes over the built-in tool's slot.
  - Line, Circle, Text and Truss examples implement `drawing_anchor()`; Hoist
    and Truss now work in the 3D view (`surface = "both"`, `placement_hover`).
- File import from scripts:
  - `doc.import_file(path, options=...)` now imports **immediately** and returns
    the created objects as an `ObjectSet`; it raises if the file can't be
    imported. The import is its own undo step (work before it is committed
    first, and it stays if the script later raises); it can't run inside
    `with doc.transaction()`. `interactive=True` still shows the Import dialog
    after the script and returns None.
  - `doc.import_options(path)` lists the options `import_file` accepts (key,
    label, kind, default, choices) without importing anything.
- File export from scripts (no dialogs, synchronous, results returned):
  - `doc.export_dxf(path, units='mm')` - the design to DXF (File > Export > DXF).
  - `doc.export_mvr(path, objects=None, visible_only=True, include_scenery=True)`
    - the design to an MVR scene. Both return `{'path', 'counts', 'warnings',
    'notes'}` and raise on failure.
  - `Sheet.export_image(path, width=1920, height=None, background='white',
    quality=90)` - a sheet as PNG / JPEG.
  - `doc.export_sheets(format='png' | 'jpg', width=..., background=...,
    quality=...)` - every sheet as an image (PDF as before).
  - A long import / export no longer counts against the run's time budget.

- Input validation hardening (869fc8y1r) — bad input now raises at the call
  instead of silently poisoning the drawing or hanging the app:
  - Non-finite numbers (NaN / infinity) are rejected centrally in every
    coordinate, delta, angle, rotation, scale, dimension, size and attribute
    write (one NaN object used to break 2D framing).
  - Count / size caps: `place_fixtures_along(count=...)` and `array(count=...)`
    cap at 100000; `place_run` caps its piece count; stage-deck and truss
    dimensions must be `> 0` and `<= 1 000 000 mm` (and the stage leg loop is
    bounded so no size can spin forever).
  - DMX: `patch()` requires `universe >= 1` / `address` 1..512;
    `number_channels` / `renumber_units` require `start >= 1` and no longer
    overflow to negative numbers.
  - File actions validate the path first: `save_as` needs an existing folder and
    a `.DSC` name; `open` / `import_file` need an existing file; a NUL or an
    over-long path raises (`OSError` / `ValueError`).
  - `create_viewport` accepts only a closed 2D shape (or a box) as the crop and
    never deletes a non-shape via `delete_crop`.
  - `objects(type=...)` and schedule `type=` accept both the `"LightingDevice"`
    and `"Lighting Device"` spellings and raise on an unknown type; unknown `dsc`
    members and object attributes raise with a "did you mean" suggestion.

- More scripting additions (869f9r5dm):
  - `dsc.doc().objects(type=..., name='glob*')` — a case-insensitive glob on the
    object label that COMBINES with the type / layer / class / canvas filters
    (`doc.objects(type='SceneObject3D', name='Box Corner*')`).
  - `dsc.ops.draw.text(..., size_mm=)` — set a text's drawn height in mm directly
    (the FontSize attribute is in drawing-scale points on the model canvas).
  - `dsc` is now pre-imported into every run — no explicit `import dsc` needed
    (the first MCP `run_python` call used to fail on it).
  - `dsc.ops.group(objects, name)` — group two or more objects under a new
    `dsc.Group` at their centroid (the Group tool / Ctrl+G).
  - `dsc.Object.rotate3d(axis, degrees, about=(x, y, z))` — rotate in 3D about any
    axis and point, updating both Rotation and Location; documented Euler order
    (Z-Y-X) in `conventions.md`.
  - `dsc.Object.bounds3d` (world) and `.mesh_bounds` (authored/local) — a 3D box
    dict `{min, max, size, center}` mm; plus `.mesh_center` and `.pivot`. Imported
    models record their local bounds at import so these work headlessly. The
    importer's centre-on-drop-point / axis-mapping conventions are in
    `conventions.md`.
  - `dsc.ops.paperwork.create_viewport(..., view='iso'|'front'|..., target=)` makes
    a 3D viewport (camera pose + framing distance + CameraRevision bump), not just a
    plan view.
  - New `dsc.Viewport` type (returned by create_viewport): `vp.frame_size = (w, h)`
    mm resizes the paper frame; `vp.set_layer_visibility` / `set_class_visibility` /
    `set_department_visibility` take the same `{name: 'visible'|'grey'|'hidden'}`
    dict as `create_viewport(layers=...)`.
  - 3D paper-viewport capture fixes (`Viewport3DSource::capture`): per-viewport
    layer/class/department visibility now reaches imported mesh models in the SAME
    capture (was one behind), and capture mode is applied before the bake/grab so
    the first capture is no longer grey with view-cube chrome.
  - `dsc.Sheet.duplicate(name)` — copy a sheet with its page setup, title block and
    all viewports / texts / shapes.
  - `dsc.ops.paperwork.assign_title_block(...)` now RETURNS the sheet's title block
    instance (a `dsc.TitleBlock`); `TitleBlock.refresh()` rebuilds it after editing
    its parts or the project fields (no unassign/reassign dance).
  - New `dsc.Layout` (`layout.part(name)`, `layout.slots`) and `dsc.TitleBlockPart`
    (`part.texts`, `part.name`) — reach a title-block part's editable Text objects
    without searching by content.
  - `dsc.Document.import_file(path, options=..., interactive=False)` — imports with
    NO review dialog by default, so it never leaves a modal dialog blocking later
    calls; `options` overrides importer defaults. It runs after the script (an
    importer owns its transaction), so it does not return objects — find them by
    `o.source_file == path`.
  - `dsc.Object.source_file` — the path an object was imported from (set by
    import_file / File > Import; None for objects made in the app).
  - `dsc.app.wait_idle()`, `dsc.Viewport.render()` and `dsc.Sheet.render(wait=True)`
    finish pending viewport renders synchronously, so a following screenshot / read
    isn't caught mid-render. A sheet screenshot now also forces a synchronous render
    (3D viewports included), so an off-screen sheet capture no longer sits on
    "Rendering…".
  - MCP `screenshot` gains `objects=[id, ...]` — frame the given objects directly,
    independent of the canvas selection (fixes doc.select() + frame='selection' not
    lining up).
- Scripting additions (869f999da):
  - PDF export with no dialog: `dsc.Sheet.export_pdf(path, dpi=300)` and
    `dsc.Document.export_sheets(directory, format='pdf', dpi=300)` reuse the
    File > Export > PDF render path (print-mode title blocks). GUI-host only.
  - `dsc.Object.material_color` — a plain solid colour override for an object's 3D
    mesh in the 3D viewport (a SceneObject3D, a push/pull solid or an imported
    model); '#RRGGBB' / '#AARRGGBB' / int / (r,g,b[,a]), None = unset. Not a full
    material model (roughness/textures are a separate decision); the native balsam
    PBR channel keeps its authored glTF materials.
  - `dsc.Object.emitted_color` — a fixture's emitted light colour as RGB, stored as
    CIE xyY in the MVR colour slot (mvrColorXyY) so it round-trips through MVR.
    NOTE: the 3D viewport does not yet render emitted light (beams), so today this
    drives MVR interchange, not the live render.
- API consistency pass (869f8jen4): `move(...)` now moves BY a delta and accepts
  either `move(dx, dy[, dz])` or `move((dx, dy[, dz]))` on `Object`, `ObjectSet`
  and `dsc.ops.transform`. New `move_to(...)` moves TO an absolute point — an
  object's origin, or (for a set / `dsc.ops.transform`) the centre of the members'
  world origins. `doc.objects()` still returns every canvas by default and takes a
  new `canvas=` filter (`doc.model_space`, a sheet, or a sheet name). Simple fixed
  collections stay properties (`doc.sheets` / `layers` / `classes` / `selection`);
  parameterised lookups stay methods — see `conventions.md`.
- `Document.add_department(name)` creates a department; assign it with
  `obj["Department"] = dept`, list them with `doc.objects(type="Department")`.
- Lighting operations: `dsc.ops.lighting.place_fixture` (native library fixture,
  optionally hung on a chord — GUI-host only), `dsc.ops.lighting.patch` /
  `number_channels` / `renumber_units` (DMX universe/address, console channel and
  unit numbering, with an optional route/axis `sort`) and `dsc.ops.lighting.fixtures`.
- Staging operations: `dsc.ops.staging.place_deck` — a stage deck composite,
  the same commit the Stage Deck tool makes.
- Transform operations: `dsc.ops.transform.move` / `rotate` / `scale` / `mirror` /
  `duplicate` / `array` — operate on an object set in one undo step, through the
  same headless layer the Move / Rotate / Scale / Mirror tools commit.
- Align & distribute: `dsc.ops.align.align` (edges / centres per axis) and
  `dsc.ops.align.distribute` (equal spacing / centres) — the same layout the
  Align & Distribute panel computes.
- Dimension operations: `dsc.ops.dimension.linear` / `aligned` / `radius` — the
  same headless layer the built-in Linear / Aligned / Radius dimension tools
  commit through.
- Boolean + push/pull operations: `dsc.ops.boolean.combine` (2D shape
  union/difference/intersection) and `combine_solids` (3D solid CSG), plus
  `dsc.ops.pushpull.extrude` (extrude a closed 2D shape into a solid) — the same
  headless layer the Boolean 2D / Boolean 3D / Push-Pull tools commit through.
- Rigging operations: `dsc.ops.rigging.place_truss` / `place_hoist` / `hang` —
  the same headless layer the built-in Truss and Hoist tools commit through.
- Snap search: `dsc.snap.chord`, `dsc.snap.connection_faces`, `dsc.snap.truss_face`.
- `dsc.library.search` (GUI-host only; raises in a headless run).
- Interactive script tools: `dsc.Tool` base class (subclass + override
  `on_press` / `on_move` / `on_release` / `on_double_click` / `on_key` /
  `on_cancel`, `preview()`, `on_typed()`, `warning_for_view()`, `self.fail()`,
  `self.refresh()`), `dsc.ToolEvent`, `dsc.Preview`, `dsc.NumberOption`,
  `dsc.BoolOption`, `dsc.InsertionMode`, and `dsc.register_tool` /
  `dsc.unregister_tool` / `dsc.tools()`. A registered tool joins the toolbox and
  behaves like a built-in tool; points arrive snapped in mm.
- `dsc.Tool` now exposes live host state as read-only properties: `self.mode`
  (active insertion-mode index), `self.typed_active` and `self.typed_text` (the
  host-owned typed-entry buffer) — read them in `on_press` / `preview` to branch
  by mode or echo what is being typed.
- Example plugins: `examples/plugins/line_tool` (full-parity Line: two-click +
  click-drag, length/bearing readout, typed length,angle) and
  `examples/plugins/circle_tool` (Circle/Ellipse: Centre / Corner / Axis Ends
  modes, Shift circle constraint, typed R / W,H / axis entry).
- `dsc.Tool` additions for the rigging proof tools: `self.option(key)` (length
  options read back in mm), `self.mode_name` (property, beside `self.mode`), and the
  `chord_side` class attribute (`'bottom'` to hang, `'top'` to lift — a hoist).
- `dsc.ui.pick_library_item(type)` — open the app's library picker (v1: the
  generic-truss profile picker) and return the chosen row, with a `profile`
  dict (mm) for a picked truss. GUI-host only; raises in a headless run.
- Example plugins: `examples/plugins/truss_tool` and `examples/plugins/hoist_tool`
  — the Truss and Hoist tools rebuilt on `dsc.Tool` + `dsc.ops.rigging`.
- `dsc.ui` submodule (GUI-host capabilities): `dsc.ui.edit_text(obj)` opens the
  inline text editor on a text object, the same editor the built-in Text tool
  opens after placement. GUI-only; raises in a headless run.
- Example plugin: `examples/plugins/text_tool` (full-parity Text: click or drag a
  box, typed W,H entry, zoom warning, then `dsc.ui.edit_text` hand-off).

## 0.2.0
- Object model: `dsc.doc()`, `Document` (objects, selection, layers, classes,
  sheets, transaction, save, import_file), `Object` + `Line` / `Circle` / `Text` /
  `Group` / `Layer` / `Class`, `ObjectSet` bulk operations, `dsc.ObjectGone`,
  `dsc.ReadOnlyError`, `dsc.app`, `dsc.ops.draw`, `dsc.object_types()`.
- `add_line` / `count` (Scripting 0 spike) are deprecated.

## 0.1.0
- Embedded runtime, scripts folder, plugins (`plugin.json`, `register()` /
  `unregister()`), `dsc.register_command`, `dsc.scripts_dir()`.