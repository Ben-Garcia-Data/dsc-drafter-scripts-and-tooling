"""Example plugin. Copy the whole 'hello' folder into the scripts folder, then
Scripts > Reload Scripts. A 'Circle each selected object' command appears in the
Scripts menu."""
import dsc

from . import shapes   # relative imports work inside a plugin


def circle_selection():
    sel = dsc.doc().selection
    if not sel:
        dsc.app.error("Select something first.")
        return
    for obj in sel:
        shapes.ring_around(obj)
    dsc.app.status(f"Circled {len(sel)} object(s).")


def register():
    dsc.register_command("Circle each selected object", circle_selection)


def unregister():
    pass  # commands are removed automatically
