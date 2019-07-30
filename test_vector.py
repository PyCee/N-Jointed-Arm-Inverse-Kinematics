import unittest
import math
from vector import Vector, Angle_Vector

class TestVectorMethods(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(Vector(1.0, 0.0) + Vector(0.0, 1.0), Vector(1.0, 1.0))
        self.assertEqual(Vector(-1.0, 0.0) + Vector(1.0, 0.0), Vector(0.0, 0.0))
    def test_scale(self):
        self.assertEqual(Vector(1.0, 0.0).scale(2.0), Vector(2.0, 0.0))
        self.assertEqual(Vector(0.0, 1.0).scale(-1.0), Vector(0.0, -1.0))
        self.assertEqual(Vector(1.0, 1.0).scale(0.0), Vector(0.0, 0.0))
    def test_subtraction(self):
        self.assertEqual(Vector(1.0, 0.0) - Vector(0.0, 1.0), Vector(1.0, -1.0))
        self.assertEqual(Vector(2.0, 0.0) - Vector(1.0, 0.0), Vector(1.0, 0.0))
    def test_magnitude(self):
        self.assertAlmostEqual(Vector(1.0, 0.0).magnitude(), 1.0)
        self.assertAlmostEqual(Vector(2.0, 0.0).magnitude(), 2.0)
        self.assertAlmostEqual(Vector(1.0, 1.0).magnitude(), 1.41421356)
    def test_normalize(self):
        self.assertEqual(Vector(1.0, 0.0).normalize(), Vector(1.0, 0.0))
        self.assertEqual(Vector(2.0, 0.0).normalize(), Vector(1.0, 0.0))
        self.assertEqual(Vector(1.0, 1.0).normalize(), Vector(0.7071, 0.7071))
        self.assertEqual(Vector(3.0, 4.0).normalize(), Vector(0.6, 0.8))
        self.assertEqual(Vector(-1.0, 0.0).normalize(), Vector(-1.0, 0.0))
    def test_dot(self):
        self.assertAlmostEqual(Vector(1.0, 0.0).dot(Vector(1.0, 0.0)), 1.0)
        self.assertAlmostEqual(Vector(1.0, 0.0).dot(Vector(-1.0, 0.0)), -1.0)
        self.assertAlmostEqual(Vector(1.0, 0.0).dot(Vector(0.0, 1.0)), 0.0)
        self.assertAlmostEqual(Vector(0.0, 1.0).dot(Vector(1.0, 0.0)), 0.0)
        self.assertAlmostEqual(Vector(1.0, 0.0).dot(Vector(0.7071, 0.7071)), 0.7071)
        self.assertAlmostEqual(Vector(1.0, 0.0).dot(Vector(0.6, 0.8)),0.6)
    def test_cross_z(self):
        self.assertAlmostEqual(Vector(1.0, 0.0).cross_z(Vector(1.0, 0.0)), 0.0)
        self.assertAlmostEqual(Vector(1.0, 0.0).cross_z(Vector(-1.0, 0.0)), 0.0)
        self.assertAlmostEqual(Vector(1.0, 0.0).cross_z(Vector(0.0, 1.0)), 1.0)
        self.assertAlmostEqual(Vector(0.0, 1.0).cross_z(Vector(1.0, 0.0)), -1.0)
        self.assertAlmostEqual(Vector(1.0, 0.0).cross_z(Vector(0.7071, 0.7071)),0.7071)
        self.assertAlmostEqual(Vector(1.0, 0.0).cross_z(Vector(0.6, 0.8)), 0.8)
    def test_angle(self):
        self.assertAlmostEqual(Vector(0.0, 0.0).get_angle(Vector(1.0, 0.0)), 0.0)
        self.assertAlmostEqual(Vector(0.0, 0.0).get_angle(Vector(0.0, 1.0)),math.pi/2)
        self.assertAlmostEqual(Vector(1.0, 0.0).get_angle(Vector(1.0, 1.0)),math.pi/2)
        self.assertAlmostEqual(Vector(0.0, 1.0).get_angle(Vector(0.0, 0.0)),-math.pi/2)
    def test_abs_angle(self):
        self.assertAlmostEqual(Vector(0.0, 0.0).get_abs_angle(), 0.0)
        self.assertAlmostEqual(Vector(1.0, 0.0).get_abs_angle(), 0.0)
        self.assertAlmostEqual(Vector(1.0, 1.0).get_abs_angle(), math.pi / 4.0)
        self.assertAlmostEqual(Vector(0.0, -1.0).get_abs_angle(), -math.pi / 2.0)
    def test_angle_vector(self):
        self.assertEqual(Angle_Vector(0.0, 0.0), Vector(0.0, 0.0))
        self.assertEqual(Angle_Vector(math.pi / 2.0, 1.0), Vector(0.0, 1.0))
        self.assertEqual(Angle_Vector(math.pi, 1.0), Vector(-1.0, 0.0))
        self.assertEqual(Angle_Vector(math.pi / 4.0, 1.0), Vector(0.7071, 0.7071))
        self.assertEqual(Angle_Vector(math.pi / 4.0, 2.0), Vector(1.4142, 1.4142))
