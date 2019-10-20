import unittest
from vector import Vector
from two_jointed_arm_ik import two_joint_validity, two_jointed_arm_ik, TwoJointOutOfRangeException, TwoJointLengthException
from recreate_point import recreate_point

def two_joint_test(length1, length2, point):
    try:
        angles = two_jointed_arm_ik(length1,
                                    length2, point)
        if point != recreate_point([length1, length2], angles):
            print("Failed to recreate point from two joint solution: ")
            print("\tLengths: " + str((length_1), length_2))
            print("\tCalculated Angles: " + str(angles))
            print("\tRecreated Point: " + str(point))
            return False
        return True
    except TwoJointOutOfRangeException as e:
        raise e

class TestTwoJointValidityMethods(unittest.TestCase):
    def test_basic_validity(self):
        self.assertTrue(two_joint_validity(10, 1, Vector(10.0, 0.0)))
    def test_basic_invalidity(self):
        self.assertFalse(two_joint_validity(10, 1, Vector(5.0, 0.0)))
    def test_edge_validity(self):
        self.assertTrue(two_joint_validity(10, 1, Vector(9.0, 0.0)))
        self.assertTrue(two_joint_validity(10, 1, Vector(11.0, 0.0)))
        self.assertFalse(two_joint_validity(10, 1, Vector(8.9999, 0.0)))
        self.assertFalse(two_joint_validity(10, 1, Vector(11.001, 0.0)))
    def test_neg_validity(self):
        self.assertTrue(two_joint_validity(10, 1, Vector(-10.0, 0.0)))
        self.assertTrue(two_joint_validity(10, 1, Vector(-9.0, 0.0)))
        self.assertTrue(two_joint_validity(10, 1, Vector(-11.0, 0.0)))
        self.assertFalse(two_joint_validity(10, 1, Vector(-8.9999, 0.0)))
        self.assertFalse(two_joint_validity(10, 1, Vector(-11.001, 0.0)))
    def test_length_order_validity(self):
        self.assertTrue(two_joint_validity(1, 10, Vector(9.5, 0.0)))
        self.assertFalse(two_joint_validity(1, 10, Vector(8.0, 0.0)))
    def test_neg_length_validity(self):
        with self.assertRaises(TwoJointLengthException):
            two_joint_validity(-10, 1, Vector(10.0, 0.0))
        with self.assertRaises(TwoJointLengthException):
            two_joint_validity(10, -1, Vector(10.0, 0.0))
        with self.assertRaises(TwoJointLengthException):
            two_joint_validity(-10, -1, Vector(10.0, 0.0))

class TestTwoJointSolutionMethods(unittest.TestCase):
    def test_basic_solution(self):
        self.assertTrue(two_joint_test(10, 1, Vector(10.0, 0.0)))
        self.assertTrue(two_joint_test(10, 1, Vector(-10.0, 0.0)))
        self.assertTrue(two_joint_test(1, 1, Vector(-1.0, 0.0)))
    def test_basic_solution_failure(self):
        with self.assertRaises(TwoJointOutOfRangeException):
            two_joint_test(10, 1, Vector(12.0, 0.0))
        with self.assertRaises(TwoJointOutOfRangeException):
            two_joint_test(10, 1, Vector(-8.5, 0.0))
        with self.assertRaises(TwoJointOutOfRangeException):
            two_joint_test(10, 1, Vector(-11.5, 0.0))
    def test_basic_edge_solutions(self):
        self.assertTrue(two_joint_test(10, 1, Vector(9.0, 0.0)))
        self.assertTrue(two_joint_test(10, 1, Vector(11.0, 0.0)))
    def test_neg_length_exception(self):
        with self.assertRaises(TwoJointLengthException):
            two_joint_test(-10, 1, Vector(10.0, 0.0))
        with self.assertRaises(TwoJointLengthException):
            two_joint_test(10, -1, Vector(10.0, 0.0))
        with self.assertRaises(TwoJointLengthException):
            two_joint_test(-10, -1, Vector(10.0, 0.0))
