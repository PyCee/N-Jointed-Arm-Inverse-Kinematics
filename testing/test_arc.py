import unittest
from vector import Vector
from arc import Arc, Arc_Radian, InvalidArcRadiusException, InvalidArcLimitsException, InvalidArcRadianException

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

class TestArcMethods(unittest.TestCase):
    def test_arc_radian(self):
        self.assertEqual(Arc_Radian(d_90), d_90)
        self.assertNotEqual(Arc_Radian(d_180), Arc_Radian(-1.0 * d_180))
        self.assertEqual(Arc_Radian(d_45), Arc_Radian(d_360 + d_45))
    def test_invalid_arc_radius_exception(self):
        with self.assertRaises(InvalidArcRadiusException):
            Arc(Vector(0.0, 0.0), -1.0, (0.0, d_180))
    def test_invalid_arc_limits_exception(self):
        with self.assertRaises(InvalidArcLimitsException):
            Arc(Vector(0.0, 0.0), 1.0, (d_45, d_45))
    def test_arc_limit_range(self):
        o_vector = Vector(0.0, 0.0)
        self.assertEqual(Arc(o_vector, 1.0, (d_0, d_90)).get_limit_range(), d_90)
        self.assertEqual(Arc(o_vector, 1.0, (d_90, d_180)).get_limit_range(), d_90)
        self.assertEqual(Arc(o_vector, 1.0, (d_90, 0.0)).get_limit_range(), d_270)
    def test_is_valid_angle(self):
        valid_angle_arc = Arc(Vector(0.0, 0.0), 1.0, (d_90, d_0))
        self.assertTrue(valid_angle_arc.is_valid_angle(d_90))
        self.assertTrue(valid_angle_arc.is_valid_angle(d_0))
        self.assertTrue(valid_angle_arc.is_valid_angle(d_180))
        self.assertTrue(valid_angle_arc.is_valid_angle(-1.0 * d_180))
        self.assertFalse(valid_angle_arc.is_valid_angle(d_90 - 0.00001))
        self.assertFalse(valid_angle_arc.is_valid_angle(d_0 + 0.0001))
    def test_arc_point(self):
        point_arc = Arc(Vector(1.0, 1.0), 2.0, (0.0, d_270))
        self.assertEqual(point_arc.get_point(d_0), Vector(3.0, 1.0))
        self.assertEqual(point_arc.get_point(d_45), Vector(2.414, 2.414))
        self.assertEqual(point_arc.get_point(d_90), Vector(1.0, 3.0))
        with self.assertRaises(InvalidArcRadianException):
            point_arc.get_point(-d_45)
        self.assertEqual(point_arc.get_first_point(), point_arc.get_point(d_0))
        self.assertEqual(point_arc.get_last_point(), point_arc.get_point(d_270))
    def test_extremes(self):
        self.assertEqual(Arc(Vector(0.0, 0.0), 2.0, (d_0, d_90)).get_extremes(),
                             [Vector(2.0, 0.0), Vector(0.0, 2.0)])
        self.assertEqual(Arc(Vector(0.0, 0.0), 1.0, (d_45, d_180)).get_extremes(),
                             [Vector(0.7071, 0.7071), Vector(-1.0, 0.0)])
        self.assertEqual(Arc(Vector(0.0, 0.0), 1.0, (-d_45, d_90)).get_extremes(),
                             [Vector(0.7071, -0.7071), Vector(0.0, 1.0),
                              Vector(1.0, 0.0)])
        self.assertEqual(Arc(Vector(0.0, 0.0), 1.0, (d_90, -d_135)).get_extremes(),
                             [Vector(0.0, 1.0), Vector(-0.7071, -0.7071),
                              Vector(-1.0, 0.0)])
        self.assertEqual(Arc(Vector(0.0, 0.0), 1.0, (-d_45, -d_135)).get_extremes(),
                         [Vector(0.7071, -0.7071), Vector(-0.7071, -0.7071),
                          Vector(1.0, 0.0), Vector(-1.0, 0.0)])
    def test_arc_intersections(self):
        base_arc = Arc(Vector(0.0, 0.0), 1.0, (d_0, d_90))
        self.assertEqual(base_arc.get_arc_intersections(Arc(Vector(0.0, 1.0), 1.0, (-d_90, d_0))),
                         [Vector(0.866, 0.5)])
        self.assertEqual(base_arc.get_arc_intersections(Arc(Vector(0.5, 0.5), 0.5, (-d_90, d_180))),
                         [Vector(0.294, 0.956), Vector(0.956, 0.294)])
        
        self.assertEqual(base_arc.get_arc_intersections(Arc(Vector(0.0, 1.0), 1.0, (d_0, d_90))),
                         [])

    '''
    def test_break_range(self):
        # Is break range actually useful? I dont think its used
        self.assertEqual(Arc(Vector(0.0, 0.0), 1.0, (0.0, d_45)).get_break_range(),
                         (None, None))
        self.assertEqual(Arc(Vector(1.0, 0.0), 1.0, (-d_45, d_90)).get_break_range(),
                         (0.7853981633974484, None))
        self.assertEqual(Arc(Vector(1.0, 0.0), 1.0, (-d_90, d_45)).get_break_range(),
                         (None, 0.7853981633974484))
        self.assertEqual(Arc(Vector(2.0, 0.0), 1.0, (-d_45, d_90)).get_break_range(),
                         (0.510990747297044, None))
        self.assertEqual(Arc(Vector(5.0, 0.0), 0.5, (-d_45, d_90)).get_break_range(),
                         (0.13189024559966953, None))
        self.assertEqual(Arc(Vector(1.0, 0.0), 1.0, (-d_90, d_90)).get_break_range(),
                         (1.5707963267948966, 1.5707963267948966))
        self.assertEqual(Arc(Vector(0.0, -1.0), 1.0, (-d_45, d_90)).get_break_range(),
                         (None, None))
        self.assertEqual(Arc(Vector(-2.0, 0.0), 1.0, (-d_45, d_90)).get_break_range(),
                         (5.282237233628814, None))
        self.assertEqual(Arc(Vector(0.0, 0.0), 1.0, (-d_45, d_90)).get_break_range(),
                         (None, None))
    '''
