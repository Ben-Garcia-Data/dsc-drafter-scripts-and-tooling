"""Draw a 10 x 10 m setting-out grid at 1 m spacing, on its own layer.

Shows: layers, dsc.ops.draw, bulk set, and a named undo step.
"""
import dsc

SIZE_MM = 10_000
STEP_MM = 1_000

doc = dsc.doc()
layer = doc.add_layer("Setting-out grid")

with doc.transaction("Draw setting-out grid"):
    doc.active_layer = layer
    lines = []
    for i in range(0, SIZE_MM + 1, STEP_MM):
        lines.append(dsc.ops.draw.line((i, 0), (i, SIZE_MM)))   # verticals
        lines.append(dsc.ops.draw.line((0, i), (SIZE_MM, i)))   # horizontals
    # One bulk call instead of a loop: colour every grid line.
    doc.objects(layer=layer).set("StrokeColor", "#40808080")

print(f"drew {len(lines)} grid lines on layer '{layer.name}'")
