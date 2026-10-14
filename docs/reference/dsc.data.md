# dsc.Data

One stored data file: read / write bytes, text, JSON or CSV, export a copy, provenance metadata.

## class `Data`

A data file stored in the drawing (CSV, JSON, XML, ...): the exact bytes plus
where and when they came from. Get one from dsc.data.files() / get() /
create() / import_file(). Read with read_bytes / read_text / read_json /
read_csv; write with the matching write_* calls; export(path) saves a copy.
Changes take effect at once, like writing a file: they are NOT part of the
run's undo step, so Undo and a failed run do not revert them. They are saved
with the drawing.

### `id` (read-only)

The data file's id (stable for the life of the drawing).


### `name`

Display name in the Library (initially the file name). Settable.


### `format` (read-only)

Format tag from the file name: 'csv', 'tsv', 'json', 'xml', 'yaml',
'text' or 'binary'.


### `mime_type` (read-only)

MIME type for the format, e.g. 'text/csv', 'application/json'.


### `size` (read-only)

Size of the contents in bytes.


### `original_name` (read-only)

File name it was imported from (or created with); export() suggests it.


### `source_path` (read-only)

Absolute path it was imported from, or None when created by a script.


### `source_path_relative` (read-only)

Import path relative to the drawing's folder at import time, or None
(untitled drawing, another drive, or created by a script).


### `imported_at` (read-only)

When it was imported (or created), as a UTC datetime.


### `modified_at` (read-only)

When its contents were last rewritten (UTC datetime), or None if never.


### `checksum` (read-only)

SHA-256 of the contents, hex — compare to tell whether two files match.


### `read_bytes(self: dsc.Data) -> bytes`

Return the contents exactly as stored, as bytes.
Example: raw = d.read_bytes()


### `write_bytes(self: dsc.Data, content: object) -> None`

Replace the contents with `content` (bytes, or str written as UTF-8).
Updates checksum and modified_at. Not undoable.
Example: d.write_bytes(b'a,b\r\n1,2\r\n')


### `export(self: dsc.Data, path: str) -> str`

Write the contents to a file at `path` (byte-for-byte; the folder must
exist). Returns the path. File > Export > Data does the same.
Example: d.export(r'C:/Shows/out/patch.csv')


### `delete(self: dsc.Data) -> None`

Remove the data file from the drawing. Not undoable.
Example: dsc.data.get('old.json').delete()


### `read_text(...)`

Return the contents decoded as text (UTF-8 by default; a leading byte-order
mark is dropped).
Example: print(dsc.data.get('notes.txt').read_text())


### `write_text(...)`

Replace the contents with `text`, encoded (UTF-8 by default).
Example: d.write_text('hello')


### `read_json(...)`

Parse the contents as JSON and return the value (dict, list, ...).
Example: cfg = dsc.data.get('rig.json').read_json()


### `write_json(...)`

Replace the contents with `value` serialised as JSON (UTF-8, `indent`
spaces; None = compact).
Example: d.write_json({'trims': [7000, 7500]})


### `read_csv(...)`

Parse the contents as CSV. header=True returns a list of dicts keyed by the
first row; header=False returns a list of lists (every row, all strings).
delimiter defaults to a tab for TSV files, else a comma.
Example: for row in dsc.data.get('patch.csv').read_csv(): print(row['Channel'])


### `write_csv(...)`

Replace the contents with `rows` as CSV. Rows of dicts write a header row
(`fields` = column order; default every key in first-seen order); rows of
sequences are written as-is, after `fields` as a header when given.
delimiter defaults to a tab for TSV files, else a comma.
Example: d.write_csv([{'Unit': 1, 'Channel': 101}, {'Unit': 2, 'Channel': 102}])

