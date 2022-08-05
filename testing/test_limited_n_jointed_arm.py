import unittest
from vector import Vector
from n_jointed_arm.n_jointed_arm_ik import OutOfRangeException, LengthException
from limited_arm.limited_n_jointed_arm_ik import limited_n_jointed_arm_validity, limited_n_jointed_arm_range, limited_n_jointed_arm_ik, LimitsException, valid_joint_range
from n_jointed_arm.recreate_point import recreate_point
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
        
def limited_n_jointed_arm_test(lengths, lower_limits, upper_limits, point):
    try:
        for i in range(11):
            weight = i / 10.0
            angles = limited_n_jointed_arm_ik(lengths,
                                              lower_limits, upper_limits,
                                              [weight] * (len(lengths) - 2),
                                              point)
            for i in range(1,len(angles)):
                if angles[i] < (lower_limits[i] - 0.000001) or \
                   angles[i] > (upper_limits[i] + 0.000001):
                    print("\nFailed to solve ik within limits")
                    print("Resulting Angles: " + str(angles))
                    print("Angle " + str(angles[i]) + \
                          " not in (" + str(lower_limits[i]) + \
                          ", " + str(upper_limits[i]) + ")")
                    return False 
            if point != recreate_point(lengths, angles):
                print("\nUnable to recreate point")
                print("Lengths: " + str(lengths))
                print("Angles: " + str(angles))
                print("Recreated: " + str(recreate_point(lengths, angles)))
                print("Should have recreated: " + str(point))
                return False
        return True
    except OutOfRangeException as e:
        raise e

class TestLimitedNJointSolutionMethods(unittest.TestCase):
    
    def test_two_jointed_solution(self):
        # Test two joint solution 
        self.assertTrue(limited_n_jointed_arm_test([1.0, 1.0],
                                                   [-d_90, -d_90],
                                                   [d_90, d_90],
                                                   Vector(1.5, -1.0)))
        self.assertTrue(limited_n_jointed_arm_test([1.0, 1.0],
                                                   [-3.14159, -3.1415],
                                                   [3.1, 3.14159],
                                                   Vector(1.9, 0.0)))
    def test_two_jointed_second_solution(self):
        # Test solution where the second two-jointed_solution
        #   must be used to comply with angle limits
        self.assertTrue(limited_n_jointed_arm_test([1.0, 1.0],
                                                   [d_0, d_0],
                                                   [d_90, d_90],
                                                   Vector(0.293, 1.384)))
            
    def test_solution(self):
        self.assertTrue(limited_n_jointed_arm_test([1.0, 1.0, 1.0],
                                                   [d_0, d_0, d_0],
                                                   [d_90, d_90, d_90],
                                                   Vector(-1.0, 1.0)))
        
        
        
        
    def test_failure(self):
        with self.assertRaises(OutOfRangeException):
            self.assertTrue(limited_n_jointed_arm_test([1.0, 1.0],
                                                       [-d_90, -d_90],
                                                       [d_90, d_90],
                                                       Vector(2.1, 0.0)))
        with self.assertRaises(OutOfRangeException):
            self.assertTrue(limited_n_jointed_arm_test([1.0, 1.0],
                                                       [-d_90, -d_90],
                                                       [d_90, d_90],
                                                       Vector(-1.75, 0.0)))
        with self.assertRaises(OutOfRangeException):
            self.assertTrue(limited_n_jointed_arm_test([1.0, 1.0],
                                                       [-d_90, -d_90],
                                                       [d_90, d_90],
                                                       Vector(-1.1, 1.1)))
        

