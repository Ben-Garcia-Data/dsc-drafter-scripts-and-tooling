# dsc.units

The document display units: format and parse lengths the way the built-in tools show them.

## `format_length(mm: float, precision: object = None) -> str`

A length in mm as the built-in tools show it: in the document's unit with
its suffix (e.g. '1.50 m', '5' 6"'). precision = decimal places (default:
the unit's own). Example: dsc.units.format_length(1500)

## `parse_length(text: str) -> object`

Parse a typed length in the document's unit (a bare number, or with a
suffix; feet-inches forms too) to mm, or None if it is not a length.

## `suffix() -> str`

The document unit's short suffix ('mm', 'm', 'ft', ...; '' for feet-inches).
