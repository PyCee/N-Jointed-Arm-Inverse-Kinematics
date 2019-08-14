import unittest
from vector import Vector
from n_jointed_arm_ik import OutOfRangeException, LengthException
from limited_n_jointed_arm_ik import limited_n_jointed_arm_validity, limited_n_jointed_arm_range, overlapping_arc_with_bounded_area_range, limited_n_jointed_arm_ik, LimitsException
from recreate_point import recreate_point
from arc import Arc

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

class TestLimitedNJointValidityMethods(unittest.TestCase):
    def test_success(self):
        self.assertTrue(limited_n_jointed_arm_validity([1, 1], [-d_90, d_0],
                                                       [d_90, d_90],
                                                       Vector(1.75, 0.0)))
        self.assertTrue(limited_n_jointed_arm_validity([1, 1], [-d_90, d_0],
                                                       [d_90, d_90],
                                                       Vector(1.0, 1.25)))
        self.assertTrue(limited_n_jointed_arm_validity([1, 1], [-d_90, d_0],
                                                       [d_90, d_90],
                                                       Vector(0.0, 1.5)))
    def test_failure(self):
        self.assertFalse(limited_n_jointed_arm_validity([1, 1], [-d_90, d_0],
                                                        [d_90, d_90],
                                                        Vector(3.0, 0.0)))
        self.assertFalse(limited_n_jointed_arm_validity([1, 1], [-d_90, d_0],
                                                        [d_90, d_90],
                                                        Vector(1.25, 0.0)))
        self.assertFalse(limited_n_jointed_arm_validity([1, 1], [-d_90, d_0],
                                                        [d_90, d_90],
                                                        Vector(1.0, 1.75)))
        self.assertFalse(limited_n_jointed_arm_validity([1, 1], [-d_90, d_0],
                                                        [d_90, d_90],
                                                        Vector(0.0, 2.5)))
        self.assertFalse(limited_n_jointed_arm_validity([1, 1], [-d_90, d_0],
                                                        [d_90, d_90],
                                                        Vector(2.0, 1.0)))

class TestOverlappingArcWithBoundedAreaRange(unittest.TestCase):
    def test_fully_out_of_bounds(self):
        arc = Arc(Vector(0.0, 0.0), 1.0, (d_0, d_90))
        arc_bounded_area = limited_n_jointed_arm_range([1, 1],
                                                       [d_0, d_0],
                                                       [d_90, d_90])
        
        self.assertEqual(overlapping_arc_with_bounded_area_range(arc, arc_bounded_area),
                         None)
    def test_fully_within_bounds(self):
        arc = Arc(Vector(0.5, 1.25), 0.5, (d_0, d_90))
        arc_bounded_area = limited_n_jointed_arm_range([1, 1],
                                                       [d_0, d_0],
                                                       [d_90, d_90])
        
        self.assertEqual(overlapping_arc_with_bounded_area_range(arc, arc_bounded_area),
                        arc.get_limits())
    def test_one_intersection_end(self):
        arc = Arc(Vector(0.0, 1.0), 0.5, (d_0, d_90))
        arc_bounded_area = limited_n_jointed_arm_range([1, 1],
                                                       [d_0, d_0],
                                                       [d_90, d_90])
        
        self.assertEqual(overlapping_arc_with_bounded_area_range(arc, arc_bounded_area),
                         (0.8480620789814817, arc.get_limits()[1]))
    def test_one_intersection_start(self):
        arc = Arc(Vector(0.0, 1.0), 0.5, (d_90, d_180))
        arc_bounded_area = limited_n_jointed_arm_range([1, 1],
                                                       [d_0, d_0],
                                                       [d_90, d_90])
        
        self.assertEqual(overlapping_arc_with_bounded_area_range(arc, arc_bounded_area),
                         (arc.get_limits()[0], 2.2935305746083117))
    def test_two_intersections(self):
        arc = Arc(Vector(-1.0, 1.0), 1.0, (d_0, d_90))
        arc_bounded_area = limited_n_jointed_arm_range([1, 1],
                                                       [d_0, d_0],
                                                       [d_90, d_90])
        self.assertEqual(overlapping_arc_with_bounded_area_range(arc, arc_bounded_area),
                         (0.4240310394907399, 1.0471975511965979))
        

        
def limited_n_jointed_arm_test(lengths, lower_limits, upper_limits, point):
    try:
        for i in range(101):
            weight = i / 100.0
            angles = limited_n_jointed_arm_ik(lengths,
                                              lower_limits, upper_limits,
                                              [weight] * (len(lengths) - 2), point)
            for i in range(len(angles)):
                if angles[i] < lower_limits[i] or angles[i] > upper_limits[i]:
                    return False
            if point != recreate_point(lengths, angles):
                return False
        return True
    except OutOfRangeException as e:
        raise e

class TestLimitedNJointSolutionMethods(unittest.TestCase):
    def test_solution(self):
        '''
        self.assertTrue(limited_n_jointed_arm_test([1.0, 1.0],
                                                   [-d_90, -d_90], [d_90, d_90],
                                                   Vector(1.75, 0.0)))
        
        self.assertTrue(limited_n_jointed_arm_test([1.0, 1.0, 1.0],
                                                   [d_0, d_0, d_0],
                                                   [d_90, d_90, d_90],
                                                   Vector(-1.0, 1.0)))
        '''
    def test_failure(self):
        with self.assertRaises(OutOfRangeException):
            self.assertTrue(limited_n_jointed_arm_test([1.0, 1.0],
                                                       [-d_90, d_90], [d_90, d_180],
                                                       Vector(1.75, 0.0)))

