# Performance at 100k objects

Drawings can hold 100 000 objects. Python calls cost roughly a microsecond each;
a loop over every object that reads and writes a few attributes costs a
noticeable fraction of a second, and it blocks the app while it runs.

1. **Filter in C++.** `doc.objects(type=..., layer=..., cls=...)` filters without
   creating a Python object per drawing object. Filter by type first, then use
   `.filter(fn)` on the smaller set.
2. **Write in bulk.** `ObjectSet.set(attr, value)`, `.move(dx, dy)` and
   `.delete()` apply to the whole set in one call.
3. **Read in bulk.** `ObjectSet.get(attr)` returns one list.
4. **Don't iterate twice.** Keep an `ObjectSet` in a variable instead of calling
   `doc.objects()` in a loop.
5. **Long jobs** are stopped after the time budget (120 s) and can be cancelled
   with Esc; both undo the run.