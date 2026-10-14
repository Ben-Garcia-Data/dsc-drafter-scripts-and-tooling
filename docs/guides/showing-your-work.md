# Showing the user what you are doing (AI agents)

When an AI drives DSC Drafter over MCP, the user is usually watching the app. Their
view should always be on whatever you are working on, so they can follow along and
stop you if something looks wrong.

## What happens automatically

After every `run_python` call that **changes objects**, the app:

1. switches to **Design** or **Paperwork** mode, and to the **sheet**, where most of
   the changed objects are;
2. frames them in **every view frame** of a split design view (each frame keeps its
   own 2D or 3D camera angle, and zooms out only if the work doesn't fit);
3. **selects** them (a member of a group or composite selects the whole group).

A read-only call (inspecting, `document_summary`, `screenshot`) moves nothing.
Screenshots always render off-screen and never move the user's view.

## Make it useful: one visible step per call

The view moves when a call finishes, not mid-call. A single giant script that builds
a whole rig shows the user nothing until the very end. Split the work into steps the
user can follow:

```
run_python: place the truss run           -> the view lands on the truss
run_python: hang the fixtures on it       -> the view lands on the fixtures
run_python: make the plot sheet + viewport -> Paperwork mode, on that sheet
```

## Pointing the view yourself: `dsc.ui.focus`

Call `dsc.ui.focus(target)` when the automatic choice would be wrong, or to show
something you only read. It overrides the automatic focus for that call (the last
`focus` in a call wins).

```python
dsc.ui.focus(fixtures)                    # objects, an ObjectSet or a list of ids
dsc.ui.focus(sheet, select=False)         # show a whole sheet in Paperwork mode
dsc.ui.focus(doc.model_space)             # back to Design mode
dsc.ui.focus(problem_objects)             # "here is what I found" after an inspection
dsc.ui.show_mode('paperwork')             # change mode with nothing particular to show
```

Typical cases:

- you edited many objects but the interesting result is a few of them: focus those;
- you created a sheet and a viewport: focus the sheet, `select=False`;
- you are reporting a finding (a clash, an unpatched fixture): focus the objects you
  are talking about, even though nothing changed.

Both calls are presentation only: in a headless run they return `False` and do
nothing, so scripts that use them still run in batch mode.
