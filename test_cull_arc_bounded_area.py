import unittest
from vector import Vector
from arc import Arc
from cull_arc_bounded_area import cull_arc_bounded_area

from math import pi

d_0 = 0.0
d_180 = pi
d_360 = d_180 * 2.0
d_90 = d_180 / 2.0
d_45 = d_180 / 4.0
d_30 = d_180 / 6.0
d_15 = d_180 / 12.0
d_135 = d_45 * 3.0

class TestCullArcBoundedArea(unittest.TestCase):
    def test_cull(self):
        self.assertEqual(cull_arc_bounded_area([Arc(Vector(0.0, 0.0), 3.0, (0.0, 1.5707963)), Arc(Vector(0.0, 0.0), 1.0000000, (1.5707963, 3.1415926)), Arc(Vector(1.0, 0.0), 2.0, (0.0, 1.5707963)), Arc(Vector(2.0, 0.0), 1.0, (-1.570796, 0.0)), Arc(Vector(1.0, 0.0), 1.4142135, (-0.785398, 0.0)), Arc(Vector(0.0, 0.0), 2.2360679, (-0.463647, 0.4636476)), Arc(Vector(1.0, 1.0), 1.0, (1.5707963, 3.1415926)), Arc(Vector(1.0, 0.0), 1.4142135, (0.7853981, 2.3561944)), Arc(Vector(0.0, 1.0), 2.0, (1.5707963, 3.1415926)), Arc(Vector(0.0, 2.0), 1.0, (0.0, 1.5707963)), Arc(Vector(0.0, 1.0), 1.4142135, (1.5707963, 2.3561944)), Arc(Vector(0.0, 0.0), 2.2360679, (1.1071487, 2.0344439)), Arc(Vector(-1.0, 1.0), 1.0, (3.1415926, -1.570796)), Arc(Vector(0.0, 1.0), 1.4142135, (2.3561944, -2.356194))]),
                           [Arc(Vector(0.0, 0.0), 3.0, (0.0, 1.5707963)), Arc(Vector(0.0, 0.0), 1.0000000, (1.5707963, 3.1415926)), Arc(Vector(2.0, 0.0), 1.0, (-1.570796, 0.0)), Arc(Vector(0.0, 0.0), 2.2360679, (-0.463647, 0.4636476)), Arc(Vector(1.0, 0.0), 1.4142135, (0.7853981, 2.3561944)), Arc(Vector(0.0, 1.0), 2.0, (1.5707963, 3.1415926)), Arc(Vector(-1.0, 1.0), 1.0, (3.1415926, -1.570796))])
