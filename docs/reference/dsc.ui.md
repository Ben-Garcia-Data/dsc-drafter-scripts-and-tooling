# dsc.ui

App UI a script can invoke: the library picker and the inline text editor (GUI-only).

## `edit_text(obj: object) -> None`

Open the inline text editor on a text object, focused for typing — the same editor the built-in Text tool opens after it places a box. Call it after dsc.ops.draw.text to let the user type straight away. A dsc.Tool does NOT need it: text a tool places is opened for editing by the host (2D and 3D), like the built-in tool. GUI-only: raises RuntimeError in a headless run.

Example: t = dsc.ops.draw.text((0, 0), 'Text'); dsc.ui.edit_text(t)

## `focus(target: object, select: bool = True) -> bool`

Move the user's view onto what you are working on, so they can watch it. `target` is an object, an ObjectSet, a list of objects/ids, a sheet, or doc.model_space. The app switches to Design or Paperwork and to the sheet where most of the objects live, frames them in EVERY design view frame (each keeps its 2D or 3D camera angle; zooms out only if they don't fit) and, with select=True, selects them. A sheet on its own just shows that sheet. Members of a group or composite focus as the whole group.

Applied when the run ends (so call it anywhere in the run; the last call wins). An AI run_python call that changes objects is focused on them automatically; calling focus overrides that (e.g. to show a sheet, or to focus a subset). Returns True if the app will show it, False in a headless run (never raises there).

Example: fx = dsc.ops.lighting.place_fixture(item, (0, 0, 6000)); dsc.ui.focus(fx)
Example: dsc.ui.focus(sheet, select=False)  # show a whole sheet

## `pick_library_item(type: object = None) -> object`

Open the content-library picker filtered to content `type` and block until the user picks a row or dismisses it. Returns the chosen row as {id, source, name, type, folder, tags} (plus a `preset` dict — {type, name, values} in mm / degrees, see dsc.presets — when the row is a schema preset, e.g. a library truss), or None if dismissed. Raises in a headless host. A dsc.Tool armed from a library row should declare library_picker instead (the built-in tools' non-blocking picker + options button).
Example: item = dsc.ui.pick_library_item('Straight Truss')

## `show_mode(mode: str) -> bool`

Switch the app to 'design' or 'paperwork' mode, as the mode switch does. Applied when the run ends. Prefer dsc.ui.focus(objects_or_sheet), which also picks the sheet and frames the work; use this only to change mode with nothing particular to show. Returns False in a headless run.

Example: dsc.ui.show_mode('paperwork')
