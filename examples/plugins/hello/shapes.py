import math

import dsc


def ring_around(obj, margin_mm=100.0):
    """Draw a circle enclosing obj's plan bounds, plus a margin."""
    xmin, ymin, xmax, ymax = obj.bounds
    centre = ((xmin + xmax) / 2, (ymin + ymax) / 2)
    radius = math.hypot(xmax - xmin, ymax - ymin) / 2 + margin_mm
    return dsc.ops.draw.circle(centre, radius)
