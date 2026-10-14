# DSC Drafter Scripts

Python tools, plugins and example scripts for **DSC Drafter**, plus the stubs and
reference you need to write your own.

DSC Drafter has Python built in. The `dsc` module gives scripts the same operations the
built-in tools use. Every tool in this repo is a Python version of a built-in DSC Drafter
tool, with the same modes, options, typed entry, snapping and preview, and it commits the
same objects. Read them to see how a tool is built, or copy one to start your own.

Everything here is under the **MIT licence**: use, copy, change and ship it, commercially
or not. Keep the copyright and licence notice with any copy or substantial portion. See
[LICENSE](LICENSE).

## Turn on the tools in this repo

DSC Drafter installs this repository for you. Its tools start switched off:

1. Open **Scripts ▸ Plugins**. The tools from this repo are listed under
   **Scripts Repository Tools**.
2. Tick the ones you want. Each one appears in the **Scripts** toolset straight away, with
   a small Python badge on its icon. Untick it to remove it again.

If a plugin fails to load, its traceback is in the Python Console.

## Use your own fork

Fork this repository on GitHub, then in DSC Drafter choose **Scripts ▸ Scripts Repository…**:

- **A fork on GitHub**: enter your fork's address (and branch, `main` if you leave it
  blank) and press **Download and Use**. DSC Drafter downloads it, so you don't need Git
  installed. Press it again to get your latest changes. The fork must be public.
- **A folder on this computer**: point it at your clone of the fork while you work on it.
  Edit a tool, then choose **Scripts ▸ Reload Scripts** to try it.
- **Official scripts** switches back to the copy installed with DSC Drafter.

The tools you switched on stay on when you change repository. Scripts from a fork run with
the same access to your computer as DSC Drafter, so only use forks you trust.

## Install a plugin of your own

1. In DSC Drafter, choose **Scripts ▸ Open Scripts Folder**
   (normally `%APPDATA%\DSC Drafter\scripts\`).
2. Copy the plugin folder into it. Copy the whole folder, `plugin.json` included.
3. Choose **Scripts ▸ Reload Scripts**. Tools appear in the **Scripts** toolset. Commands
   appear in the **Scripts** menu.

Plugins in your scripts folder are on by default. If one has the same folder name as a
tool in this repo, yours is the one that loads, so you can copy a tool here and change it.

## Your first tool in five minutes

You'll build **My Line**: click once to start a line, move the mouse to see it stretch,
click again to draw it. It's the smallest complete tool, and every part of it is
explained below.

A plugin is just a folder. In the scripts folder (**Scripts ▸ Open Scripts Folder**),
make a folder called `my_first_tool` and put two files in it.

### 1. `plugin.json`: tells DSC Drafter what the plugin is

```json
{
  "name": "My First Tool",
  "version": "1.0.0",
  "description": "Click twice to draw a line.",
  "dsc_api": "0.2"
}
```

- `name` is what the plugin is called in **Scripts ▸ Plugins**. It's the only required field.
- `version` is your own version number, for your users' benefit.
- `description` is shown next to the name in the Plugins list.
- `dsc_api` is the oldest scripting API version your code needs. DSC Drafter won't load
  the plugin on an older API, so users get a clear message instead of a crash.

### 2. `__init__.py`: the tool itself

```python
# Every script starts by importing dsc, DSC Drafter's scripting module. It only exists
# inside DSC Drafter, which is why you can't run this file in a normal Python.
import dsc

# register_tool() hands back an id for the tool. We keep it here so unregister()
# can remove the same tool again when the plugin is reloaded or switched off.
_TOOL_ID = None


# A tool is a class that inherits from dsc.Tool. DSC Drafter does the heavy lifting
# (mouse handling, snapping, drawing the preview, undo) and calls the methods below
# at the right moments. You only write the parts that make your tool different.
class TwoClickLine(dsc.Tool):

    # --- Settings: plain class attributes that describe the tool ---------------------

    # The tool's name in the toolbox, in Find Tool and in its tooltip.
    name = "My Line"

    # The toolbox icon. ":/icons/..." paths are DSC Drafter's own icons; you can also
    # give the full path to an SVG file of your own. A small Python badge is added to
    # the corner automatically, so users can tell script tools from built-in ones.
    icon = ":/icons/tools/design/Line.svg"

    # Where the tool works: "2d" (the plan), "3d" (the 3D view) or "both".
    surface = "2d"

    # Which toolbox group the tool appears under.
    toolset = "Scripts"

    # --- Event handlers: DSC Drafter calls these while the tool is in use ------------

    def on_activate(self):
        # Called when the user picks the tool. Reset the tool's memory here.
        # self.start is the first click; None means "no line in progress yet".
        self.start = None
        # self.hover is the latest mouse position, for the rubber-band preview.
        self.hover = None

    def on_press(self, e):
        # Called when the left mouse button goes down. e.point is where, as (x, y)
        # in millimetres with Y pointing up the plan. It's already snapped, so if
        # the user clicked near a corner or an endpoint, you get that exact point.
        if self.start is None:
            # First click: remember where the line starts. We also set hover, so the
            # preview has both ends straight away.
            self.start = self.hover = e.point
        else:
            # Second click: draw the line. dsc.ops.draw.line is the same operation the
            # built-in Line tool uses, so the result is an ordinary line, exactly as
            # if the user had drawn it with that tool. It's one undo step, so Ctrl+Z
            # removes it.
            dsc.ops.draw.line(self.start, e.point)
            # Forget the start point so the next click begins a new line.
            self.start = None
        # Ask DSC Drafter to redraw the preview now that our state has changed.
        self.refresh()
        # Returning True means "I handled this click", so nothing else reacts to it
        # (for example, the click doesn't also select whatever is under the cursor).
        return True

    def on_move(self, e):
        # Called every time the mouse moves. Keep this quick: it runs many times a
        # second. Here we only store the position and ask for a redraw.
        self.hover = e.point
        self.refresh()
        return True

    def on_cancel(self):
        # Called when the user presses Esc or right-clicks. Drop the line in progress.
        self.start = None
        self.refresh()

    def preview(self):
        # Called by DSC Drafter whenever it redraws the tool (after self.refresh()).
        # Return what to show on screen, or None to show nothing. Nothing drawn
        # here is saved in the drawing; it's only a guide for the user.
        if self.start is None:
            return None
        # One straight rubber-band segment from the first click to the mouse.
        # dsc.Preview can also draw multi-point paths and a text readout.
        return dsc.Preview(lines=[(self.start, self.hover)])


# --- Plugin entry points: DSC Drafter calls these when it loads the plugin -----------

def register():
    # Called when the plugin loads (at startup, and on Scripts > Reload Scripts).
    # This is where you add your tools and menu commands.
    global _TOOL_ID
    _TOOL_ID = dsc.register_tool(TwoClickLine)


def unregister():
    # Called just before the plugin unloads or reloads. DSC Drafter removes the
    # plugin's tools for you, but cleaning up yourself makes the intent clear.
    if _TOOL_ID:
        dsc.unregister_tool(_TOOL_ID)
```

### 3. Try it

Choose **Scripts ▸ Reload Scripts**, then pick **My Line** from the Scripts toolset and
click twice on the plan. After you edit the file, reload again; you don't need to restart.
If something goes wrong, the error and the line it happened on appear in
**Scripts ▸ Python Console**.

### 4. Where to go next

- [tools/drawing/line_tool](tools/drawing/line_tool/) is the full version of this tool.
  It adds click-drag, a live length and angle readout, and typed exact values (press Tab).
- [tools/drawing/circle_tool](tools/drawing/circle_tool/) shows insertion modes and
  holding Shift to constrain the shape.
- [docs/reference/dsc.Tool.md](docs/reference/dsc.Tool.md) lists every setting and handler
  a tool can use: options bars, the 3D view, snapping to truss, Ctrl+wheel rotation and more.

To try the API without writing a plugin, open **Scripts ▸ Python Console** and type:

```python
import dsc
doc = dsc.doc()
doc.objects(type="Line")
```

## Tool index

Each tool matches its built-in twin: same modes, options, typed entry, snapping and
result. If a tool ever differs, the difference is stated in its docstring.

| Tool | Folder | What it shows |
|---|---|---|
| Line | [line_tool](tools/drawing/line_tool/) | Two-click and click-drag, length + bearing readout, typed length / angle, axis guides |
| Circle / Ellipse | [circle_tool](tools/drawing/circle_tool/) | Insertion modes (Centre / Corner / Axis Ends), Shift constraint, typed R / W,H / axis |
| Text | [text_tool](tools/drawing/text_tool/) | Click or drag a box, typed W,H, hands off to the inline text editor |
| Truss | [truss_tool](tools/rigging/truss_tool/) | Library and Straight modes, library picker, chord / face snapping, Ctrl+wheel rotation, 2D + 3D |
| Hoist | [hoist_tool](tools/rigging/hoist_tool/) | Top-chord snap and attach, Ctrl+wheel rotation, 2D + 3D |

## Examples

| Example | What it does |
|---|---|
| [plugins/hello](examples/plugins/hello/) | The smallest plugin: one Scripts-menu command, a relative import |
| [grid_lines.py](examples/grid_lines.py) | Batch script: draws a 10 × 10 m setting-out grid on its own layer |
| [layer_report.py](examples/layer_report.py) | Batch script: counts objects per layer |
| [rig_truss_with_fixtures.py](examples/rig_truss_with_fixtures.py) | Batch script: builds a truss run, flies it on two hoists and hangs six fixtures |

Run a batch script from **Scripts ▸ Run Script File…**, or put it in the scripts folder
and it appears in the Scripts menu.

## Reference

- [docs/conventions.md](docs/conventions.md) covers units (mm, Z up, degrees), axes,
  undo/transactions, bulk operations and versioning. Read it first.
- [docs/reference/](docs/reference/) is the full API, one page per module.
- [docs/guides/](docs/guides/) has guides on plugins, batch scripts, reading imported
  drawings, performance, and connecting an AI client over MCP.
- [docs/llms.txt](docs/llms.txt) is an index for AI assistants.
- [stubs/dsc.pyi](stubs/dsc.pyi) is a type stub. Point your editor at `stubs/` for
  autocomplete (this repo's `pyproject.toml` already does that for Pyright and Pylance).

The `dsc` module exists only inside DSC Drafter, so scripts run there and not in a
standalone Python. The docs and stub are generated from the app on each release. Don't
edit them here.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
