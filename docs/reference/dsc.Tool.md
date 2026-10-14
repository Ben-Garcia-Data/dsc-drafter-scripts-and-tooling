# dsc.Tool

Interactive script tools: subclass dsc.Tool, register with dsc.register_tool.

## class `Tool`

Base class for an interactive scripted tool. Subclass it, set the class
attributes and override the handlers you need, then register it with
dsc.register_tool(MyTool). The host wraps it in a native tool: it feeds
snapped points in mm, renders your options bar and preview, and owns the
typed-entry buffer, Tab and Enter.

Class attributes: name, icon (SVG path), shortcut, surface ('2d' / '3d' /
'both'), toolset (the toolbox chip to file under), options (a list of
dsc.NumberOption / dsc.BoolOption), modes (a list of dsc.InsertionMode),
typed_fields (one entry per typed field, enabling typed entry: a label or a
(label, suffix) pair, shown in the typed echo; a field whose suffix is 'mm'
is a length — typed and echoed in the document's unit, delivered to
on_typed in mm), chord_snap (True to snap to
rig-member chords and get the highlight chrome), chord_side ('bottom' for
things that hang, the default, or 'top' for things that lift, e.g. a hoist).
draws_on_work_plane: True to receive work-plane points in the 3D view (a
drawing tool); None (the default) means True for surface '3d' / 'both'.
placement_hover: True for a single-click placement tool, so the 3D view
feeds on_move before the first click and the preview follows the cursor.
library_picker: a dsc.LibraryPicker for a tool armed from a library row
(picks arrive in on_library_item; reopen it with open_library_picker()).
placement_rotation: True (or a list of insertion-mode names) for a stamp
placement the user turns with Ctrl+wheel (15 deg a notch, Shift+Ctrl 5 deg)
before clicking, as the built-in placement tools do. The host owns the
wheel, the angle readout and the status hint; read the angle as
self.rotation and pass it to the op (rotation=).

Status bar: return hints() to describe what each input does right now; the
host adds the typed-entry and rotation bindings itself. Cursor: return a
cursor() name to change the pointer over the canvas.

Return the gesture's anchor from drawing_anchor() to get the built-in
drawing tools' axis guides, arrow-key axis lock and anchor marker.

Read the host-owned option values and active mode inside a handler with
self.option(key) (mm for a length option), self.mode() and self.mode_name().

Example:
    class TwoClickLine(dsc.Tool):
        name = 'Script Line'
        def on_press(self, e):
            self.start = e.point
        def on_release(self, e):
            dsc.ops.draw.line(self.start, e.point)
    dsc.register_tool(TwoClickLine)

### `name`

Class attribute, default `'Script Tool'`.


### `icon`

Class attribute, default `''`.


### `shortcut`

Class attribute, default `''`.


### `surface`

Class attribute, default `'2d'`.


### `toolset`

Class attribute, default `''`.


### `options`

Class attribute, default `[]`.


### `modes`

Class attribute, default `[]`.


### `typed_fields`

Class attribute, default `[]`.


### `chord_snap`

Class attribute, default `False`.


### `chord_side`

Class attribute, default `'bottom'`.


### `needs_mouse_tracking`

Class attribute, default `True`.


### `draws_on_work_plane`

Class attribute, default `None`.


### `placement_hover`

Class attribute, default `False`.


### `library_picker`

Class attribute, default `None`.


### `placement_rotation`

Class attribute, default `False`.


### `on_activate(...)`

Called when the tool becomes active; set up per-session state here.


### `on_deactivate(...)`

Called when the tool is switched away; clear any transient state.


### `on_press(...)`

Left-button press at e.point (mm, snapped). Return True to consume.


### `on_move(...)`

Cursor moved to e.point; update preview state and call self.refresh().


### `on_release(...)`

Left-button release at e.point; commit geometry via dsc.ops here.


### `on_double_click(...)`

Double-click at e.point, e.g. to finish a multi-point gesture.


### `on_key(...)`

A key press (e.key / e.text). Return True to consume it.


### `on_key_release(...)`

A key release (e.key; e.modifiers is the state AFTER the release).
Use it to drop a modifier-driven preview (e.g. Shift-constrain) the
moment the key comes up, without waiting for a mouse move.


### `on_cancel(...)`

The gesture was cancelled (Esc / right-click); discard pending state.


### `on_typed(...)`

Typed exact-value entry committed: values is the list of typed_fields
numbers (mm for lengths, degrees for angles). Place the resolved point.


### `on_library_item(...)`

The user picked a row in this tool's library_picker popup. item is
the row dict {id, source, name, type, folder, tags} (+ a `preset` dict
{type, name, values} when the row is a schema preset, e.g. a library
truss — pass it to the op as preset=). Arm the placement from it; return
False to refuse the row (nothing is armed). Runs outside a
transaction: don't edit the drawing here.


### `open_library_picker(...)`

Open this tool's library_picker popup (e.g. on Tab, or a click
with nothing armed), as the built-in tools do. Non-blocking: the pick
arrives later in on_library_item.


### `preview(...)`

Return a dsc.Preview for the current drag, or None. The host redraws
it after self.refresh().


### `drawing_anchor(...)`

While a creation gesture is in progress, the (x, y) mm point it
radiates from (the previously placed point), else None. The host draws
axis-extension guides from it, applies the arrow-key axis lock through
it and marks it, exactly as for the built-in drawing tools. Read once
after each event, so keep it a plain attribute lookup.

Example: return self.start  # None until the first click


### `on_wheel(...)`

The mouse wheel turned over the canvas (e.notches steps, e.modifiers).
Return True to consume it; otherwise the view zooms as usual. Not
called for Ctrl+wheel when placement_rotation is on (the host turns
the placement).


### `hints(...)`

The status-bar hint strip for the current state, or None for the
drawing-tool defaults (Place point / Next point / Cancel). held lists
the modifiers held now ('shift', 'ctrl', ...). Return a list of
(input, label) or (input, label, active) tuples, where input is one
spelling or a list of them: 'click', 'drag', 'double_click', 'right',
'middle', 'wheel', a key ('tab', 'esc', 'enter', 'a', ...) or a held
modifier ('shift'), optionally prefixed ('ctrl+wheel', 'shift+click').
Re-read after every event, so list only what the handlers honour now.

Example: return [('click', 'Place truss'), ('tab', 'Pick truss')]


### `cursor(...)`

The pointer over the canvas: None for the host default, a shape
name ('arrow', 'cross', 'pointing', 'open_hand', 'closed_hand',
'forbidden', 'ibeam', 'size_all', 'size_hor', 'size_ver', 'wait',
'busy', 'blank'), or 'icon' for the tool's own icon (the transform
tools' cursor). Re-read after every event.


### `rotation` (read-only)

The Ctrl+wheel placement rotation in degrees counter-clockwise (plan
Y up), 0 until the user turns it; reset when the tool is switched away.
Only moves when placement_rotation is on. Turn the preview by it and
pass it to the op, e.g. dsc.ops.rigging.place_hoist(..., rotation=self.rotation).


### `warning_for_view(...)`

Return a status-bar warning for the current zoom (e.g. 'zoom in to
edit'), or None for no warning.


### `refresh(...)`

Ask the host to redraw this tool's preview() now.


### `mode` (read-only)

Index of the active insertion mode (0-based), matching the order of
this tool's modes list; 0 when the tool declares no modes. The host
keeps it live as the user picks a mode button, so read it in on_press /
preview to branch (as Circle does for Centre / Corner / Axis Ends).


### `typed_active` (read-only)

True while typed exact-value entry is engaged (Tab armed it, or a
digit has been typed). The host owns the buffer and commits it through
on_typed on Enter, and swaps the readout for the typed echo itself.


### `typed_text` (read-only)

The raw typed-entry buffer as the user is typing it (a comma
separates fields), or '' when nothing is being typed. Pair it with
typed_active to echo the value near the cursor in preview().


### `mode_name` (read-only)

Name of the active insertion mode (e.g. 'Library'), or None when the
tool declares no modes.


### `option(...)`

The current value of one of this tool's options (mm for a length
option, the number as typed otherwise, True/False for a toggle). Returns
None for an unknown key. Read it inside a handler to drive placement, as
the built-in tools read numericOption / boolOption.

Example: length = self.option('length')


### `fail(...)`

Refuse the current action with a status-bar error instead of a silent
dead click. Aborts the handler; the host rolls back any pending edit and
shows the message.


## class `ToolEvent`

One input event handed to a dsc.Tool handler.

Attributes: point — the snapped cursor as (x, y, z) in mm, plan Y up; raw —
the same cursor without snapping; button — 'left' / 'right' / 'middle' /
'none'; modifiers — a list drawn from 'shift' / 'ctrl' / 'alt' / 'meta'. For
on_key, key is the Qt key code and text the character typed. chord is set to
(member_id, z_mm) when a chord-snap tool is snapped onto a rig member.
drag is the built-in tools' click-vs-drag call: True on on_move once the
pressed cursor has left a small screen deadzone, and on on_release only when
that drag was held long enough to count (a quick flick stays a click). Use it
instead of comparing points, so a slow click never reads as a drag.
For on_wheel, notches is the wheel steps (+ = rolled away from the user).

## class `Preview`

What a tool draws mid-drag. lines: straight rubber-band segments, each
((x, y), (x, y)) in mm — use these for straight edges. paths: polylines, each
a list of (x, y) points. readout: near-cursor text such as a live length.
readout_at: where to place it (x, y in mm), or None to keep it by the cursor.
typed_labels: the typed-entry fields for the CURRENT stage, each a label or a
(label, suffix) pair, e.g. [('R', 'mm')]. While typed entry is engaged the
host replaces the readout with them ('-> R 100 mm'); None falls back to the
tool's typed_fields names. markers: points (x, y) in mm that get a small
screen-sized diamond, e.g. a connection point (the built-in rigging tools'
marker). chord_snap: a point (x, y) on or near a rig member's chord - the host
draws the built-in chord highlight there (member outline, chord, ring marker,
3D drop line) without moving your event points; pair it with
dsc.snap.member_end's on_chord. All points are mm, plan Y up.

## class `NumberOption`

A numeric field for the tool's options bar. key is the stable id used to
read the value back, label the caption, default the starting value, is_length
True to show and parse it in drawing units (mm), tooltip an optional hint.

### `kind`

Class attribute, default `'number'`.


## class `BoolOption`

An on/off toggle for the tool's options bar. key is the stable id, label
the caption, default the starting state, tooltip an optional hint.

### `kind`

Class attribute, default `'bool'`.


## class `InsertionMode`

A named insertion-mode button (like Circle's Centre / Corner / Axis Ends).
name is shown on the button; icon is an optional SVG resource path.

## class `LibraryPicker`

Declares that a tool's placement is armed from a content-library row
(set it as the tool's library_picker). The host then gives the tool the
built-in picker flow: the filtered library popup opens when the tool is
activated with nothing armed, the options bar shows a picker button with
the armed row's name, and the status bar names it. content_type is the
library type the popup lists (e.g. 'Straight Truss'); title / search_hint
caption the popup; noun names the item ('Truss' -> 'Select Truss...');
modes lists the insertion modes (names or indices) the picker applies to,
empty for all. The pick arrives in Tool.on_library_item.

Example: library_picker = dsc.LibraryPicker('Straight Truss', noun='Truss',
                                            modes=['Library'])
