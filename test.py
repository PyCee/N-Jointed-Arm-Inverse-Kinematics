
from n_jointed_arm_ik import *
import math
import sys

class Test:
    def __init__(self, T, L, P):
        self.title = T
        self.lengths = L
        self.point = P
    def test(self, funct, result_funct):
        if result_funct(self.lengths, self.point, funct(self.lengths, self.point)):
            print(self.title + ": Success")
        else:
            print(self.title + ": Failure")
            sys.exit()

two_joint_validity_test_1 = Test("Two Joint Validity Test #1", [10, 1], Vector(5.0, 0.0))
two_joint_validity_test_1.test(lambda L, P: two_joint_point_validity(L[0], L[1], P),
                               lambda L, P, result: result == False)

n_joint_validity_test_1 = Test("N Joint Validity Test #1", [2, 6, 5], Vector(0.5, 0.0))
n_joint_validity_test_1.test(lambda L, P: n_joint_point_validity(L, P),
                             lambda L, P, result: result == True)

two_joint_ik_test_1 = Test("Two Joint IK Test #1", [3, 4], Vector(7.0, 0.0))
two_joint_ik_test_1.test(lambda L, P: two_jointed_arm_ik(L[0], L[1], P),
                         lambda L, P, result: recreate_point(L, result).equals(P))

two_joint_ik_test_2 = Test("Two Joint IK Test #2", [1, 7], Vector(0, 6.5))
two_joint_ik_test_2.test(lambda L, P: two_jointed_arm_ik(L[0], L[1], P),
                         lambda L, P, result: recreate_point(L, result).equals(P))

two_joint_ik_test_3 = Test("Two Joint IK Test #3", [1, 7], Vector(-6.5, 0.0))
two_joint_ik_test_3.test(lambda L, P: two_jointed_arm_ik(L[0], L[1], P),
                         lambda L, P, result: recreate_point(L, result).equals(P))

two_joint_ik_test_4 = Test("Two Joint IK Test #4", [2, 2], Vector(0, -3))
two_joint_ik_test_4.test(lambda L, P: two_jointed_arm_ik(L[0], L[1], P),
                         lambda L, P, result: recreate_point(L, result).equals(P))

n_joint_ik_test_1 = Test("N Joint IK Test #1", [1, 3, 4], Vector(5.5, 0.0))
n_joint_ik_test_1.test(lambda L, P: n_jointed_arm_ik(L, 0.5, P),
                       lambda L, P, result: recreate_point(L, result).equals(P))

n_joint_ik_test_2 = Test("N Joint IK Test #2", [1, 1, 1, 1, 1, 4, 3, 1, 1],
                         Vector(6.0, 0.0))
n_joint_ik_test_2.test(lambda L, P: n_jointed_arm_ik(L, 0.5, P),
                       lambda L, P, result: recreate_point(L, result).equals(P))

n_joint_ik_test_3 = Test("N Joint IK Test #3", [1, 1, 1, 1, 1, 4, 3, 1, 1, 1, 1, 1],
                         Vector(6.0, 0.0))
n_joint_ik_test_3.test(lambda L, P: n_jointed_arm_ik(L, 0.5, P),
                       lambda L, P, result: recreate_point(L, result).equals(P))

n_joint_ik_test_4 = Test("N Joint IK Test #4",
                         [1, 1, 1, 1, 1, 1, 0.1, 0.01, 0.1, 2, 3, 4], Vector(6.0, 0.0))
n_joint_ik_test_4.test(lambda L, P: n_jointed_arm_ik(L, 0.5, P),
                       lambda L, P, result: recreate_point(L, result).equals(P))

n_joint_ik_test_5 = Test("N Joint IK Test #5", [1, 2, 3, 4, 2, 2], Vector(4.0, 0.0))
n_joint_ik_test_5.test(lambda L, P: n_jointed_arm_ik(L, 1.0, P),
                       lambda L, P, result: recreate_point(L, result).equals(P))

n_joint_ik_test_6 = Test("N Joint IK Test #6", [1, 1, 1], Vector(0.1, 0.0))
n_joint_ik_test_6.test(lambda L, P: n_jointed_arm_ik(L, 1.0, P),
                       lambda L, P, result: recreate_point(L, result).equals(P))
