# dsc.app

The running application: active document, status bar, open/new.

## `active_document() -> object`

The document scripts act on, or None.

## `error(message: str) -> None`

Show an error in the status bar.

## `new() -> None`

Start a new document. Runs after the script finishes.

## `open(path: str) -> None`

Open a .DSC file. Runs after the script finishes.

## `status(message: str) -> None`

Show a message in the status bar.

## `wait_idle() -> None`

Finish any pending viewport / sheet renders and drain the event loop, so a
following screenshot or read sees fully-rendered content rather than a
half-finished 'Rendering…' viewport. A no-op in a headless run.
Example: dsc.app.wait_idle()
