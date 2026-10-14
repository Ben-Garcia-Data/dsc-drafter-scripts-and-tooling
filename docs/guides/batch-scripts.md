# Writing a batch script

A batch script is a `.py` file that edits the open drawing in one go.

## Where scripts live

`%APPDATA%\DSC Drafter\scripts\` (Scripts ▸ Open Scripts Folder). Every `.py`
file directly in that folder appears in the **Scripts** menu. Helper modules you
want to `import` go in `scripts\modules\`.

You can also run any file with Scripts ▸ Run Script File…, or type into
Scripts ▸ Python Console.

## Shape of a script

```python
import dsc

doc = dsc.doc()
lights = doc.objects(type="LightingDevice", layer=None)
print(len(lights), "fixtures")
```

- The whole run is one undo step. Ctrl+Z undoes all of it.
- `print()` output goes to the Python Console.
- An exception undoes the run and shows its traceback in the console.
- Esc cancels a long run.

## Finding objects

```python
doc.objects()                          # every drawing object
doc.objects(type="Circle")             # by type ('Line', 'Circle', 'Text', ...)
doc.objects(layer=doc.active_layer)    # by layer
doc.selection                          # what is selected on the canvas
doc.objects().filter(lambda o: o["Radius"] > 500 if "Radius" in o else False)
```

## Changing objects

```python
sel = doc.selection
sel.move(1000, 0)                      # 1 m to the right
sel.set("StrokeColor", "#00AAFF")
for obj in sel:
    obj.rotation = 45
```

## Several undo steps

```python
with doc.transaction("Add grid"):
    for i in range(10):
        dsc.ops.draw.line((i * 1000, 0), (i * 1000, 9000))
with doc.transaction("Label grid"):
    ...
```

See `conventions.md` for units and `reference/` for every call.