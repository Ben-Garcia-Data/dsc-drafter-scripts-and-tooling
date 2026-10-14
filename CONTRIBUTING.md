# Contributing

Contributions are welcome under the same MIT licence as the rest of the repo. By opening
a pull request you agree your contribution is released under [LICENSE](LICENSE).

## Layout

```
tools/<domain>/<tool>/    one plugin per tool: plugin.json + __init__.py
examples/                 batch scripts, and small plugins under examples/plugins/
docs/, stubs/             generated from DSC Drafter on each release - do not edit
scripts/                  repo checks (run by CI)
```

Domains: `drawing`, `edit`, `paperwork`, `rigging`, `lighting`, `staging`, `video`,
`audio`, `threed`.

## A new tool

- Copy the closest existing tool as a starting point. Keep its shape: a `dsc.Tool`
  subclass, `register()` / `unregister()`, and a module docstring explaining what the
  tool does and any way it differs from its built-in twin.
- Put the heavy work in `dsc.ops` / `dsc.snap` calls, not Python loops. Each event
  handler should do a small, constant amount of work, and `preview()` should return at
  most a few dozen points.
- Use the public conventions throughout: mm, plan Y up, Z up, degrees
  (see [docs/conventions.md](docs/conventions.md)). Format lengths you show to the user
  with `dsc.units.format_length`; never hard-code "mm".
- Add the tool to the tool index in [README.md](README.md) (CI checks it is listed) and
  a line to [CHANGELOG.md](CHANGELOG.md).
- Use only your own icons or DSC Drafter's built-in `:/icons/...` resources. Don't
  include another product's icons, screenshots, text or library content.

## Before you open a pull request

```
pip install ruff pyright
ruff check .
pyright
python scripts/check_plugins.py
```

Then load the plugin in DSC Drafter (Scripts ▸ Reload Scripts) and try it next to the
built-in tool it copies.
