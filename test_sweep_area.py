import unittest
from vector import Vector
from arc import Arc
from sweep import sweep_area

from math import pi

d_0 = 0.0
d_180 = pi
d_360 = d_180 * 2.0
d_90 = d_180 / 2.0
d_45 = d_180 / 4.0
d_30 = d_180 / 6.0
d_15 = d_180 / 12.0
d_135 = d_45 * 3.0

class TestSweepArea(unittest.TestCase):
    def test_sweep(self):
        self.assertEqual(sweep_area([Arc(Vector(0.0, 0.0), 1.0, [-d_90, d_90])],
                                    1.0, (d_0, d_90)),
                         [Arc(Vector(0.0, 0.0), 2.0,
                              (0.0, 1.5707963268)),
                          Arc(Vector(1.0, 0.0), 1.0,
                              (-1.5707963268, 0.0)),
                          Arc(Vector(0.0, 0.0), 1.414214,
                              (-0.7853981634, 0.7853981634)),
                          Arc(Vector(0.0, 1.0), 1.0,
                              (1.5707963268, 3.1415926536)),
                          Arc(Vector(0.0, 0.0), 1.414214,
                              (0.7853981634, 2.3561944902))])
