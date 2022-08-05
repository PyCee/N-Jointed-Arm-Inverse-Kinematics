import unittest
from vector import Vector
from arc import Arc
from limited_arm.sweep import sweep_area

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
        self.assertEqual(sweep_area([Arc(Vector(0.0, 0.0), 1.0,
                                         [-d_90, d_90])],
                                    1.0, (d_0, d_90)),
                         [Arc(Vector(0.0, 0.0), 2.0,
                              (0.0, 1.5707963)),
                          Arc(Vector(0.0, 1.0), 1.0,
                              (1.5707963, 3.1415926)),
                          Arc(Vector(0.0, 0.0), 1.4142135,
                              (0.7853981, 2.3561944)),
                          Arc(Vector(0.0, 0.0), 1.4142135,
                              (-0.785398, 0.7853981)),
                          Arc(Vector(1.0, 0.0), 1.0,
                              (-1.570796, 0.0))])
