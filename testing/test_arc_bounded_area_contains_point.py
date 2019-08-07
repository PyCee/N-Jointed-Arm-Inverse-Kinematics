import unittest
from vector import Vector
from arc import Arc
from sweep import sweep_area
from arc_bounded_area_contains import get_x_intercepts, arc_bounded_area_contains_point

from math import pi

d_0 = 0.0
d_180 = pi
d_360 = d_180 * 2.0
d_90 = d_180 / 2.0
d_45 = d_180 / 4.0
d_30 = d_180 / 6.0
d_15 = d_180 / 12.0
d_135 = d_45 * 3.0
d_270 = d_180 + d_90

class TestArcXIntercept(unittest.TestCase):
    def test_x_intercept(self):
        self.assertEqual(get_x_intercepts(Arc(Vector(0.0, 0.0), 1.0, (-d_90, d_90)),
                                          0.7071),
                         (-0.7071135623080638, 0.7071135623080638))
    def test_upper_only(self):
        self.assertEqual(get_x_intercepts(Arc(Vector(0.0, 0.0), 1.0, (d_0, d_90)),
                                          0.7071),
                         (None, 0.7071135623080638))
    def test_lower_only(self):
        self.assertEqual(get_x_intercepts(Arc(Vector(0.0, 0.0), 1.0, (-d_90, d_0)),
                                          0.7071),
                         (-0.7071135623080638, None))
    def test_extreme_intercepts(self):
        self.assertEqual(get_x_intercepts(Arc(Vector(0.0, 0.0), 1.0, (-d_90, d_90)),
                                          1.0),
                         (0.0, None))
        self.assertEqual(get_x_intercepts(Arc(Vector(0.0, 0.0), 1.0, (d_90, -d_90)),
                                          -1.0),
                         (-1.2246467991473532e-16, None))
        
TEST_AREA = sweep_area([Arc(Vector(0.0, 0.0), 1.0, (-d_90, d_90))], 1.0, (d_0, d_90))
class TestArcBoundedAreaContainsPoint(unittest.TestCase):
    def test_success(self):
        self.assertTrue(arc_bounded_area_contains_point(TEST_AREA, Vector(1.75, 0.0)))
        self.assertTrue(arc_bounded_area_contains_point(TEST_AREA, Vector(1.0, 1.25)))
        self.assertTrue(arc_bounded_area_contains_point(TEST_AREA, Vector(0.0, 1.5)))
    def test_failure(self):
        self.assertFalse(arc_bounded_area_contains_point(TEST_AREA, Vector(3.0, 0.0)))
        self.assertFalse(arc_bounded_area_contains_point(TEST_AREA, Vector(1.25, 0.0)))
        self.assertFalse(arc_bounded_area_contains_point(TEST_AREA, Vector(1.0, 1.75)))
        self.assertFalse(arc_bounded_area_contains_point(TEST_AREA, Vector(0.0, 2.5)))
        self.assertFalse(arc_bounded_area_contains_point(TEST_AREA, Vector(2.0, 1.0)))
