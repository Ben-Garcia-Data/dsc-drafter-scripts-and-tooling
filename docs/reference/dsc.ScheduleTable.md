# dsc.ScheduleTable

Live schedule tables: read rows / totals, re-fit with update(), export to CSV — returned by dsc.ops.paperwork.schedule_table.

## class `ScheduleTable`

A placed, LIVE schedule table (dsc.ops.paperwork.schedule_table). Its values
track the document; read them with .rows / .totals, re-fit its structure with
.update() when .out_of_date, and export with .to_csv(). Sizes are mm.

### `id` (read-only)

The table object's id (also dsc.doc().object(id)).


### `exists` (read-only)

False once the table has been deleted or undone.


### `object` (read-only)

The underlying dsc.Object (for style attributes, layer/class, deletion).


### `error` (read-only)

The filter-expression parse error as a string, or None when the query is
valid. A bad filter matches nothing rather than raising.


### `rows` (read-only)

The live detail rows, each a dict keyed by column header (or field). Values
are the raw cell values. Re-evaluated on every access, so a fixture edit is
reflected immediately (before any .update()).
Example: [row['Channel'] for row in t.rows]


### `totals` (read-only)

The grand-total aggregates (a dict of count / sum columns keyed by header).
Empty when the table has no aggregate columns.


### `out_of_date` (read-only)

True when the live rows no longer fit the built structure (rows added /
removed or columns changed) — the table is drawn stale until .update().


### `update(self: dsc.ScheduleTable) -> None`

Re-fit the table to its current rows in one undoable 'Update Table' step
(rebuilds the cells and clears out_of_date). No-op for a snapshot table.


### `size` (read-only)

The laid-out size as {'width', 'height' (mm), 'flow_columns'} across all
side-by-side overflow columns.


### `to_csv(self: dsc.ScheduleTable, path: str, raw: bool = False) -> None`

Write the evaluated rows to a UTF-8 CSV file (RFC-4180). raw=True writes the
unformatted values (no unit suffixes) for round-tripping into Lightwright /
a console; the default writes the formatted display strings.
Example: t.to_csv('schedule.csv')

