# dsc.ops.paperwork

Paperwork: viewports from crop shapes, data tags, data tag styles, title block parts and layouts, the same objects the paperwork tools and the Library make.

## `assign_title_block(layout: object, *, sheet: object = None, default: bool = False) -> object`

Put a title block layout on a sheet (`sheet`: a sheet or its name; layout None
removes it) and/or make it the document default new sheets adopt (`default`).
Returns the sheet's title block instance (a dsc.TitleBlock, or None when only the
document default was set) — call .refresh() on it after editing its parts.
Example: tb = dsc.ops.paperwork.assign_title_block(layout, sheet='Sheet 1')

## `create_viewport(crop: object = None, sheet: object = None, *, scale: float = 50.0, at: object = None, delete_crop: bool = True, layers: object = None, classes: object = None, departments: object = None, bounds: object = None, margin: float = 0.0, view: object = None, target: object = None) -> object`

Make a viewport — what right-click > Create Viewport does. Three ways to say
what area it shows:
  crop shapes  one drawing object or several on the design canvas: a closed
               shape (rectangle, circle, ellipse, closed polyline) crops to its
               own outline, anything else to its bounds, and several union.
               `delete_crop` (default True, like the dialog) removes them in the
               same undo step.
  crop box     `crop=((x0, y0), (x1, y1))` mm model-space corners (or a
               `{'min': (x, y), 'max': (x, y)}` dict) — a rectangular crop with
               NO temporary shape (delete_crop is ignored).
  bounds=      an object or ObjectSet — crop to the combined bounds of those
               objects. `margin` mm grows a box / bounds crop on every side.
The viewport lands on `sheet` (a sheet or its name; default the active sheet,
else the first) at 1:`scale`, centred on the paper, or with its centre at `at`
(x, y mm in sheet coordinates: (0, 0) top-left, Y down is negative). `layers` /
`classes` / `departments` are dicts {layer or name: 'visible' | 'grey' | 'hidden'}
for this viewport only. Returns the viewport (a dsc.Viewport); its SourceScale /
SourceCenter attributes pan and rescale, vp.frame_size resizes the paper frame,
and vp.set_layer_visibility / set_class_visibility change the per-viewport
overrides later.
  view=  makes a 3D viewport instead of a plan: 'iso', 'front', 'back', 'left',
         'right', 'top', 'bottom', or a (yaw, pitch) pair in degrees. It sets the
         camera to frame the crop's model extent; target= (x, y mm, model space)
         re-aims it, and vp['CameraDistance'] / vp['CameraYaw'] fine-tune it. A 3D
         viewport only renders while its sheet is on screen — force a render with
         vp.render() or a sheet screenshot (see docs).
Example:
    vp = dsc.ops.paperwork.create_viewport(((0, 0), (12000, 8000)), 'Sheet 1',
                                           scale=100, margin=500)
    iso = dsc.ops.paperwork.create_viewport(bounds=doc.objects(type='SceneObject3D'),
                                            margin=1000, view='iso', scale=25)

## `data_tag(target: object, at: object = None, *, style: object = None, viewport: object = None, offset: bool = False, model_scale: float = 1.0, leader: object = None, size: object = None, attribute: object = None, format: object = None, canvas: object = None) -> object`

Place a graphic data tag on `target` — the SAME DataTagInstance the Data Tags
tool commits (via Ops::placeDataTag). `style` is a data tag style (make one with
data_tag_style()); its drawn children carry the {object.<field>} tokens, resolved
to the fixture's values at draw/export time. `at` (x, y mm) is where the tag lands
in with-leader mode (omitted = hung off the target by the style's default offset).
`offset=True` (or `leader=False`) makes an offset label — the leader is dropped and
the tag tracks the object. Data tags are SHEET-ONLY content: pass `viewport`
(omitted = the first viewport on the sheet showing the target). Called off a
sheet, the tag goes onto the sheet whose viewport shows the target; with no such
viewport it raises ValueError. Legacy `attribute`/`format`/
`size` build a one-field style when no `style` is given.
Example: dsc.ops.paperwork.data_tag(fixture, (120, -80), style=channel_style,
                                    canvas='Lighting Plot', viewport=vp)

## `data_tag_style(name: str, *, objects: object = None, origin: object = None, applies_to: object = None, tag: object = None, attribute: object = None, format: object = None, font: object = None, size: object = None, color: object = None, bold: object = None, italic: object = None, align: object = None, box: object = None, leader: object = None) -> object`

A graphic Data Tag Style (library content type 'data-tag-style') — the drawn
content the Data Tags tool copies onto each tag, with {object.<field>} tokens
resolved per fixture at render/export time. Two ways to build it:
  objects  — a list of drawn shapes / lines / text (with {object.channel} etc.)
             become the style's children; `origin` (x, y mm) is the leader point
             (default the bounds centre).
  attribute/format — the one-field shorthand: a single bound text ('{value}' in
             `format` is the field), with font / size / color / bold / italic /
             align / box ((w, h) mm) / leader (bool); `tag` seeds from a data tag.
Field names match case-insensitively (attribute='Channel' resolves 'channel'),
the same match obj['Channel'] uses. `applies_to` filters which equipment types
the style tags. Returns the style.
Example: dsc.ops.paperwork.data_tag_style('Channel', attribute='Channel',
    format='CH {value}', size=10, bold=True)

## `layout_slots(layout: object) -> list`

A layout's slots as dicts, in the form title_block_layout() takes.

## `schedule_table(columns: object = None, at: object = None, *, source: object = None, type: object = None, subtypes: bool = True, summarise: bool = True, name: str = '', filter: object = None, sort: object = None, group: object = None, preset: object = None) -> dsc.ScheduleTable`

Place a LIVE ScheduleTable — the SAME table the Schedule panel's Insert-to-sheet
button makes (Ops::createScheduleTable, live). It defines a saved query and drops
a formatted table on the active canvas at `at` (x, y mm, plan Y up; default near
the origin). Wrap the call in doc.on_canvas(sheet) to put it on a sheet. The table
tracks the document: its values update in place, and when rows are added / removed
it marks itself out of date — call .update() on the returned object to re-fit it.
  columns   the report's columns, in order. Each item is an attribute-key string
            (e.g. 'Wattage', or a pseudo-key '@type' / '@layer' / '@name' /
            '@host'), or a dict with at least one of 'field' (an attribute key) or
            'format' (a field-token string, '{universe}.{address|pad=3}'), plus
            optional 'header', 'align' ('left'|'center'|'right'), 'width',
            'widthMode' ('auto'|'fixed'), 'sort' ('asc'|'desc'), and 'count' or
            'sum' (True for a per-group count / summed total column). Optional
            when a preset supplies columns.
  source    where rows come from: a dict {'type'|'layer'|'class'|'department':
            name} or {'ids': objects}. `type=` is the legacy shorthand for
            {'type': ...}; `subtypes` (default True) also matches descendant
            classes.
  filter    an expression filter, ANDed with the columns, e.g.
            "purpose == 'FRT' and layer == 'OPT A'". A parse error matches
            nothing and shows in the returned table's .error.
  sort      a list of column identifiers (field / header) to sort by, ascending,
            or dicts/tuples ({'field','dir'} / (field, 'desc')).
  group     a single group-by key for the live table (empty = no grouping).
  summarise True groups matching objects and adds a Count; False lists one row
            per object.
  preset    'instrument_schedule' or 'equipment_summary' — fills the definition
            before the other kwargs override it.
Returns a dsc.ScheduleTable: read .rows / .totals, check .out_of_date, .update(),
read .size (mm) and .to_csv(path).
Example: t = dsc.ops.paperwork.schedule_table(preset='instrument_schedule')
         t = dsc.ops.paperwork.schedule_table(
                 columns=[{'field': '@type'}, {'field': 'Wattage', 'sum': True}],
                 source={'class': 'Lighting Device'}, summarise=True)

## `set_layout_slots(layout: object, slots: object) -> None`

Replace a layout's slots (same dict form as title_block_layout()).

## `tag_all(style: object, targets: object, *, viewport: object = None, offset: bool = True, model_scale: float = 1.0, canvas: object = None) -> dict`

Tag every matching object in `targets` with `style` in ONE undo step (the same
Ops::tagAll the Data Tags tool's Tag All uses) — offset label legends by default.
Skips targets the style's Applies-To filter rejects and targets already tagged
with this style in this attachment context. Data tags are SHEET-ONLY: pass
`viewport` (targets outside its crop are skipped); off a sheet with no viewport
it raises ValueError. Returns
{'created', 'skipped_existing', 'skipped_filter', 'skipped_outside'}.
Example: dsc.ops.paperwork.tag_all(channel_style, fixtures, viewport=vp)

## `title_block_layout(name: str, slots: object) -> object`

A Title Block Layout (library content type 'title-block'): an ordered list of
slots, each placing one part on the sheet's printable area. A slot is a dict:
  id           str, required; later slots refer to it
  part         a title block part (or None for an empty slot)
  relative_to  'sheet' (default) or an EARLIER slot's id
  anchor       where the part's origin lands on that reference: 'bottom-right'
               (default), 'bottom', 'bottom-left', 'left', 'center', 'right',
               'top-left', 'top', 'top-right', or (fx, fy) fractions across
               and UP (0, 0 = bottom-left)
  offset       (dx, dy) mm, Y up
  fill_h       (start_ref, 'left'|'center'|'right', end_ref, edge): stretch the
               part across between two references ('sheet' or a slot id)
  fill_v       the same vertically, edges 'top'|'center'|'bottom'
Raises ValueError for a reference to a later or unknown slot.
Example: dsc.ops.paperwork.title_block_layout('Standard', [
    {'id': 'A', 'part': title},
    {'id': 'B', 'part': revisions, 'relative_to': 'A', 'anchor': 'top-right'}])

## `title_block_part(objects: object, name: str, *, origin: object = 'bottom-right', stretch: object = None, stretch_line: object = None, stretch_line_v: object = None, min_width: object = None, min_height: object = None, place: bool = False) -> object`

Turn drawing objects (boxes, lines, text with {field} tokens such as
{sheet.name}, {project.name}, {date}) into a Title Block Part — library content
type 'title-block-part'. The objects move into the part. `origin` is the point
a layout anchors: 'bottom-right' (default), 'bottom-left', 'top-left',
'top-right', 'center' or an (x, y) mm point. `stretch` 'horizontal' / 'vertical'
/ 'both' lets a Fill slot grow the part; `stretch_line` (mm from the origin along
that axis; for 'both' the vertical line, with `stretch_line_v` the horizontal
one) is where it grows; `min_width` / `min_height` mm. `place` True also leaves
an instance where the objects were. Returns the part.
Example: part = dsc.ops.paperwork.title_block_part([box, title], 'Sheet Title')
