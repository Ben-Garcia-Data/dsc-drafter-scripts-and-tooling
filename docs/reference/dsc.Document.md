# dsc.Document

A drawing: queries, selection, layers, classes, sheets, transactions, save.

## class `Document`

An open drawing.

### `transaction(self: dsc.Document, name: str) -> dsc.Transaction`

with doc.transaction('Name'): ... — one named undo step. An exception inside
the block undoes it (objects it created are removed) and propagates.


### `objects(self: dsc.Document, type: object = None, layer: object = None, cls: object = None, canvas: object = None, name: object = None) -> dsc.ObjectSet`

Drawing objects, optionally filtered by type name ('Line', 'LightingDevice'),
layer and class. Without `type`, layers/classes/containers are excluded.
By DEFAULT returns objects on EVERY canvas (the model space and all sheets).
canvas= narrows to one canvas: doc.model_space, a sheet, or a sheet name
(case-insensitive, like doc.sheet()). name= is a case-insensitive glob on the
object's label ('Box Corner*', '*coupler*') that COMBINES with the other
filters, so doc.objects(type='SceneObject3D', name='Box Corner*') selects only
the meshes and never a viewport that shares the name prefix.


### `get(self: dsc.Document, id: str) -> object`

The object with this id, or None.


### `selection` (read-only)

The canvas selection (ObjectSet).


### `select(self: dsc.Document, objects: object) -> None`

Select objects (an ObjectSet, list of objects/ids, or one object).


### `layers` (read-only)

Design layers.


### `classes` (read-only)

Classes (object types).


### `sheets` (read-only)

Paperwork sheets.


### `sheet(self: dsc.Document, name: str) -> object`

The paperwork sheet with this name (case-insensitive), or None.
Example: sheet = doc.sheet('Sheet 1')


### `add_sheet(self: dsc.Document, name: object = None, *, size: object = None, orientation: object = None, margins: object = None, unit: object = None) -> object`

Add a paperwork sheet (like the + in the sheet list) and return it. `name`
defaults to 'Sheet N'. New sheets are A3 landscape with 10 mm margins and take
the document's default title block; `size` ('A1', ... or a (w, h) mm pair),
`orientation`, `margins` and `unit` override that (see dsc.Sheet).
Example: plot = doc.add_sheet('Lighting Plot', size='A1')


### `export_sheets(self: dsc.Document, directory: object = None, format: str = 'pdf', dpi: int = 300, *, combined: bool = False, filename: object = None, width: int = 1920, background: object = 'white', quality: int = 90) -> list`

Export every paperwork sheet as PDF (or format='png' / 'jpg' images). `directory` defaults to the folder the
drawing's .DSC is saved in — leave it out unless the user asked for another
place. A never-saved drawing is saved after the run, under its date-stamped
name in the Save As default folder, so the PDFs sit beside it. A missing
folder is created. By default one PDF per
sheet (named after the sheet, illegal characters replaced); combined=True
writes ONE multi-page PDF instead, a page per sheet in sheet-list order, each
page sized to its own sheet, named `filename` (default 'Sheets.pdf').
PDF sheets are true vector geometry (selectable text); `dpi` is the resolution
(72..2400, default 300). For 'png' / 'jpg': one image per sheet, `width` px wide
(height from the sheet's aspect), `background` 'white' / 'black' /
'transparent' (PNG) / a colour, `quality` 1..100 for JPEG.
Returns the list of written paths. Reuses File > Export > PDF; GUI-host only
(raises in a headless run).
Example: doc.export_sheets(combined=True, filename='Lighting Set')


### `model_space` (read-only)

The design canvas (model space) — the canvas new objects go on by default.


### `active_canvas` (read-only)

The canvas new objects go on right now: doc.model_space, a sheet, or None.


### `on_canvas(self: dsc.Document, canvas: object) -> dsc.CanvasContext`

with doc.on_canvas(sheet): ... — every object created inside the block (draw,
place and duplicate ops) goes on that canvas instead of the design canvas, and
undoes with the run. `canvas` is a sheet, a sheet name or doc.model_space.
The previous canvas is restored when the block ends, also on error.
Example:
    with doc.on_canvas('Sheet 1'):
        dsc.ops.draw.text((20, -20), 'GENERAL NOTES')  # paper runs -Y


### `active_layer`

Layer new objects go on.


### `active_class`

Class new objects get.


### `layer(self: dsc.Document, name: str) -> object`

The design layer with this name (case-insensitive), or None.
Example: layer = doc.layer('Lighting') or doc.add_layer('Lighting')


### `cls(self: dsc.Document, path: str) -> object`

The class with this name or dashed path (case-insensitive), or None.
Example: rig = doc.cls('RIG-TRUSS')


### `department(self: dsc.Document, name: str) -> object`

The department with this name (case-insensitive), or None.
Example: dept = doc.department('Lighting')


### `add_layer(self: dsc.Document, name: str, *, exist_ok: bool = True) -> object`

Create a design layer, or return the existing one of that name (exist_ok=True,
the default). exist_ok=False raises if a layer of that name already exists.
Example: layer = doc.add_layer('Lighting')


### `add_class(self: dsc.Document, path: str, *, exist_ok: bool = True) -> object`

Create a class; 'RIG-TRUSS' creates the missing levels and returns the leaf, or
returns the existing one of that path (exist_ok=True, the default). exist_ok=False
raises if the class path already exists.


### `add_department(self: dsc.Document, name: str, *, exist_ok: bool = True) -> object`

Create a department, or return the existing one of that name (exist_ok=True, the
default). exist_ok=False raises if a department of that name already exists.
Its StackOrder breaks 2D draw-order ties within a layer and class. List them with
doc.objects(type='Department'); assign one with obj['Department'] = dept.
Example: doc.add_department('Lighting')


### `modified` (read-only)

Unsaved changes?


### `save(self: dsc.Document) -> None`

Save (File > Save). Runs after the script finishes.


### `save_as(self: dsc.Document, path: str) -> None`

Save to a new .DSC file with no dialog (File > Save As); the document then
lives at that path. Runs after the script finishes. Save a document set up with
units, classes, sheets and a title block to make a template.
Example: doc.save_as(r'C:/Templates/Metric A3.DSC')


### `import_file(self: dsc.Document, path: str, *, options: object = None, interactive: bool = False) -> object`

Import a file (DWG, DXF, PDF, SVG, GDTF, MVR, 3D models...) into this document
NOW, with no dialog, and return the created objects as an ObjectSet. Raises
if the file can't be imported. `options` is a dict of importer options keyed
by name, overriding the defaults — list them with doc.import_options(path).
The import is its OWN undo step: whatever the script did before it is
committed first, and the import stays if the script later raises. It can't
run inside `with doc.transaction()`. Every created object's source_file is
the path. interactive=True instead shows the normal Import dialog AFTER the
script finishes and returns None.
Example: objs = doc.import_file(r'C:/plans/venue.dwg', options={'unitScale': 1.0})


### `import_options(self: dsc.Document, path: str) -> list`

Read a file and list the options doc.import_file(path, options=...) accepts,
without importing anything. Each option is a dict: key (the name to pass),
label, kind ('choice' or 'toggle'), default, choices (for a choice: a list of
{label, value}) and tooltip.
Example: for o in doc.import_options(r'C:/plans/venue.dwg'): print(o['key'], o['default'])


### `export_dxf(self: dsc.Document, path: str, *, units: str = 'mm') -> dict`

Export the design (model space) to a DXF file, no dialog - the same output as
File > Export > DXF. `units` is the drawing unit the DXF is written in: 'mm'
(default), 'cm', 'm', 'in' or 'ft'. Sheets are not included (use
export_sheets for those). A missing folder is created; an existing file is
overwritten. Returns {'path', 'counts': {'entities': n}, 'warnings', 'notes'};
raises if the export fails. GUI-host only.
Example: doc.export_dxf(r'C:/out/venue.dxf', units='m')


### `export_mvr(self: dsc.Document, path: str, *, objects: object = None, visible_only: bool = True, include_scenery: bool = True) -> dict`

Export the design to an MVR scene file, no dialog - the same output as
File > Export > MVR Scene (fixtures with their GDTF, trusses, hoists, scenery
meshes). `objects` (an ObjectSet / list) limits it to those objects, else the
whole drawing; visible_only=True skips hidden layers / classes;
include_scenery=False leaves out stage / set / venue models. A missing folder is
created. Returns {'path', 'counts': {'fixtures', 'trusses', 'hoists', ...},
'warnings', 'notes'}; raises if the export fails. GUI-host only.
Example: doc.export_mvr(r'C:/out/rig.mvr', objects=doc.objects(type='LightingDevice'))


## class `Transaction`

Context manager returned by Document.transaction().
