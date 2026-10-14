# dsc.ops.staging

Staging: place stage decks through the same layer the Stage Deck tool commits.

## `place_deck(at: object, width: float = 2000.0, depth: float = 1000.0, height: float = 600.0, shape: str = 'Rectangular', label: str = '', *, canvas: object = None) -> object`

Place a stage deck centred on plan point at=(x, y) mm. width/depth/height
are mm (deck top above the floor); shape is a deck-outline name
('Rectangular', ...). The deck is a StageObject composite (filled 2D plan +
3D solid). One undo step. Returns the deck.
Example: dsc.ops.staging.place_deck((0, 0), width=4000, depth=2000)
