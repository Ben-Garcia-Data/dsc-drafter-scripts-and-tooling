# Build a 10 m truss run at 7 m, fly it on two hoists and hang six fixtures
# under it. Everything is addressed by member + distance, never by guessing
# plan coordinates, so it works wherever the run is and however it's rotated.
import dsc

rig = dsc.ops.rigging

# A face-connected run of standard pieces (4 + 4 + 2 m), centre line at 7 m.
run = rig.place_run((-5000, 4000), (5000, 4000), elevation=7000)
truss = run[0]  # any piece addresses the whole run with span=True

info = rig.member_info(truss)
print("run length", info["run_length"], "mm; pieces:",
      [round(p["length"]) for p in rig.span(truss)])

# Hoists 1 m in from each end, motor bodies at 10 m.
for off in (1000, info["run_length"] - 1000):
    rig.place_hoist(member=truss, offset=off, span=True, insert_height=10000)

# Six fixtures along the run, 500 mm clear of each end, on the left-hand
# bottom chord (chord 0, looking from the run's start).
hit = dsc.library.search("par", type="Lighting Device")[0]
fixtures = dsc.ops.lighting.place_fixtures_along(hit, truss, count=6, margin=500)

# Read the rig back: everything hanging on the run, in order.
for h in rig.hung_objects(truss, span=True):
    print(f'{h["object"].name:<24} {h["offset"]:8.0f} mm')

# Slide the last fixture 300 mm towards the middle, onto the other chord.
last = rig.host_of(fixtures[-1])
rig.hang(fixtures[-1], member=truss, span=True,
         offset=last["offset"] - 300, chord=1)
