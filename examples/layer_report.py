"""Print how many objects of each type sit on each design layer.

Read-only: it changes nothing, so its undo step is empty and disappears.
Run it from Scripts > Run Script File... or copy it into the scripts folder.
"""
import collections

import dsc

doc = dsc.doc()
counts = collections.Counter()
for obj in doc.objects():
    layer = obj.layer
    counts[(layer.name if layer else "(no layer)", obj.type)] += 1

for (layer, type_name), n in sorted(counts.items()):
    print(f"{layer:30} {type_name:20} {n:6}")
print(f"{sum(counts.values())} objects on {len(doc.layers)} layers")
