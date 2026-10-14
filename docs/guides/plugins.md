# Packaging a plugin

A plugin is a folder in the scripts folder with a `plugin.json`:

```
%APPDATA%\DSC Drafter\scripts\
    number_lights\
        plugin.json
        __init__.py
        helpers.py
```

`plugin.json`:

```json
{
  "name": "Number Lights",
  "version": "1.0.0",
  "description": "Numbers lighting fixtures left to right.",
  "dsc_api": "0.2",
  "entry": "__init__.py"
}
```

Only `name` is needed; `entry` defaults to `__init__.py`. `dsc_api` makes the app
refuse to load the plugin on an older API (see `conventions.md`, Versioning).

`__init__.py`:

```python
import dsc
from . import helpers          # relative imports work inside the plugin

def run():
    helpers.number(dsc.doc().selection)

def register():                # called when the plugin loads
    dsc.register_command("Number Lights", run)

def unregister():              # called before it unloads / reloads
    pass
```

- `register_command` adds an entry to the Scripts menu; running it is one undo
  step named after the label. Commands are removed automatically on unload.
- Scripts ▸ Reload Scripts re-imports every plugin after you edit its files — no
  restart.
- Scripts ▸ Plugins lists each plugin; untick one to disable it (remembered).
- If loading fails, the plugin shows "(failed)" and the traceback is in the
  Python Console. Other plugins still load.

A complete example is in `examples/plugins/hello/`.