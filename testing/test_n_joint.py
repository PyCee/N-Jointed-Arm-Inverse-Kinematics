import unittest
from vector import Vector
from n_jointed_arm_ik import n_joint_validity, n_jointed_arm_ik, recreate_point, OutOfRangeException, LengthException

def n_joint_test(lengths, point):
    try:
        for i in range(101):
            weight = i / 100.0
            angles = n_jointed_arm_ik(lengths, [weight] * (len(lengths) - 2), point)
            if point != recreate_point(lengths, angles):
                return False
        return True
    except OutOfRangeException as e:
        raise e

class TestNJointValidityMethods(unittest.TestCase):
    def test_basic_validity(self):
        self.assertTrue(n_joint_validity([3, 1, 1], Vector(4.0, 0.0)))
    def test_basic_invalidity(self):
        self.assertFalse(n_joint_validity([3, 1, 1], Vector(6.0, 0.0)))
    def test_edge_validity(self):
        self.assertTrue(n_joint_validity([3, 1, 1], Vector(5.0, 0.0)))
        self.assertTrue(n_joint_validity([3, 1, 1], Vector(1.0, 0.0)))
        self.assertFalse(n_joint_validity([3, 1, 1], Vector(5.0001, 0.0)))
        self.assertFalse(n_joint_validity([3, 1, 1], Vector(0.9999, 0.0)))
    def test_neg_length_validity(self):
        with self.assertRaises(LengthException):
            n_joint_validity([-3, 1, 1], Vector(4.0, 0.0))
        with self.assertRaises(LengthException):
            n_joint_validity([3, -1, 1], Vector(4.0, 0.0))
        with self.assertRaises(LengthException):
            n_joint_validity([-3, -1, 1], Vector(4.0, 0.0))
class TestNJointSolutionMethods(unittest.TestCase):
    def test_basic_solution(self):
        self.assertTrue(n_joint_test([3, 1, 1], Vector(1.0, 0.0)))
        self.assertTrue(n_joint_test([3, 1, 1], Vector(-2.0, 0.0)))
        self.assertTrue(n_joint_test([1] * 20, Vector(1.0, 0.0)))
        self.assertTrue(n_joint_test([1, 2, 3, 4], Vector(3.0, 3.0)))
    def test_basic_solution_failure(self):
        with self.assertRaises(OutOfRangeException):
            n_joint_test([3, 1, 1], Vector(6.0, 0.0))
        with self.assertRaises(OutOfRangeException):
            n_joint_test([3, 1, 1], Vector(0.5, 0.0))
        with self.assertRaises(OutOfRangeException):
            n_joint_test([3, 1, 1], Vector(-6.0, 0.0))
        with self.assertRaises(OutOfRangeException):
            n_joint_test([3, 1, 1], Vector(-0.5, 0.0))
    def test_basic_edge_solutions(self):
        self.assertTrue(n_joint_test([3, 1, 1], Vector(5.0, 0.0)))
        self.assertTrue(n_joint_test([3, 1, 1], Vector(1.0, 0.0)))
        with self.assertRaises(OutOfRangeException):
            n_joint_test([3, 1, 1], Vector(5.0001, 0.0))
        with self.assertRaises(OutOfRangeException):
            n_joint_test([3, 1, 1], Vector(0.9999, 0.0))
    def test_neg_length_exception(self):
        with self.assertRaises(LengthException):
            n_joint_test([-3, 1, 1], Vector(10.0, 0.0))
        with self.assertRaises(LengthException):
            n_joint_test([3, -1, 1], Vector(10.0, 0.0))
        with self.assertRaises(LengthException):
            n_joint_test([-3, 1, -1], Vector(10.0, 0.0))
    def test_error_correction(self):
        correction_lengths = [1, 1, 1, 1, 1, 1, 0.1, 0.01, 0.1, 2, 3, 4]
        self.assertTrue(n_joint_test(correction_lengths, Vector(6.0, 0.0)))
        
    
        
