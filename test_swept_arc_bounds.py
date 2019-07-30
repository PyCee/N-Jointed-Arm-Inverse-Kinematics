import unittest
from vector import Vector
from arc import Arc
from sweep import get_swept_arc_bounds

from math import pi

d_0 = 0.0
d_180 = pi
d_360 = d_180 * 2.0
d_90 = d_180 / 2.0
d_45 = d_180 / 4.0
d_30 = d_180 / 6.0
d_15 = d_180 / 12.0
d_135 = d_45 * 3.0

class TestSweptArcBoundsMethods(unittest.TestCase):
    def test_basic_arc_bounds(self):
        self.assertEqual(get_swept_arc_bounds(Arc(Vector(0.0, 0.0), 1.0,
                                                  (-d_90, d_45)),
                                              1.0, (0.0, d_90)),
                         ([Arc(Vector(1.0, 0.0), 1.0,
                               (-1.5707963268, 0.0))],
                          [Arc(Vector(0.0, 1.0), 1.0,
                               (1.5707963268, 2.3561944902)),
                           Arc(Vector(0.0, 0.0), 1.847759,
                               (1.1780972451, 1.9634954085)),
                           Arc(Vector(0.0, 1.0), 1.0,
                               (0.0, 0.7853981634))]))
