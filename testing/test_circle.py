import unittest
import two_jointed_arm.circle as circle
from vector import Vector

class TestCircleMethods(unittest.TestCase):
    def test_neg_radius_exception(self):
        with self.assertRaises(circle.InvalidCircleRadiusException):
            circle.Circle(Vector(0.0, 0.0), -1.0)
    def test_basic_intersection(self):
        c1 = circle.Circle(Vector(0.0, 0.0), 1.0)
        c2 = circle.Circle(Vector(1.0, 0.0), 1.0)
        results = [Vector(0.5, 0.866), Vector(0.5, -0.866)]
        self.assertTrue(c1.get_intersections(c2) == results)
    def test_negative_positioning_intersection(self):
        c1 = circle.Circle(Vector(0.0, 0.0), 1.0)
        c2 = circle.Circle(Vector(1.0, -2.0), 2.0)
        results = [Vector(1.0, 0.0), Vector(-0.6, -0.8)]
        self.assertTrue(c1.get_intersections(c2) == results)
    def test_single_intersection(self):
        c1 = circle.Circle(Vector(0.0, 0.0), 1.0)
        c2 = circle.Circle(Vector(2.0, 0.0), 1.0)
        results = [Vector(1.0, 0.0)]
        self.assertTrue(c1.get_intersections(c2) == results)
    def test_no_intersection(self):
        c1 = circle.Circle(Vector(0.0, 0.0), 1.0)
        c2 = circle.Circle(Vector(5.0, 0.0), 1.0)
        results = []
        self.assertTrue(c1.get_intersections(c2) == results)
    def test_no_intersection_inside(self):
        c1 = circle.Circle(Vector(0.0, 0.0), 3.0)
        c2 = circle.Circle(Vector(1.5, 0.0), 1.0)
        results = []
        self.assertTrue(c1.get_intersections(c2) == results)
    def test_same_circle_intersection(self):
        c1 = circle.Circle(Vector(0.0, 0.0), 1.0)
        c2 = circle.Circle(Vector(0.0, 0.0), 1.0)
        results = [Vector(1.0, 0.0)]
        self.assertTrue(c1.get_intersections(c2) == results)
    def test_radius_zero_intersection(self):
        c1 = circle.Circle(Vector(0.0, 0.0), 0.0)
        c2 = circle.Circle(Vector(1.0, 0.0), 1.0)
        results = [Vector(0.0, 0.0)]
        self.assertTrue(c1.get_intersections(c2) == results)
