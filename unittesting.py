import unittest
from testing.test_vector import TestVectorMethods
from testing.test_circle import TestCircleMethods
from testing.test_two_jointed_arm import TestTwoJointValidityMethods, \
    TestTwoJointSolutionMethods
from testing.test_n_jointed_arm import TestNJointValidityMethods, \
    TestNJointSolutionMethods
from testing.test_limited_n_jointed_arm import TestLimitedNJointValidityMethods, \
    TestLimitedNJointSolutionMethods
from testing.test_arc import TestArcMethods
from testing.test_subdivision import TestSubdivisionMethods
from testing.test_swept_arc_bounds import TestSweptArcBoundsMethods
from testing.test_cull_arc_bounded_area import TestCullArcBoundedArea
from testing.test_sweep_area import TestSweepArea
from testing.test_arc_bounded_area_contains_point import TestArcXIntercept, \
    TestArcBoundedAreaContainsPoint

if __name__ == "__main__":
    unittest.main()
