
from n_jointed_arm_ik import *
import math
import sys

class Test:
    def __init__(self, T, L, P):
        self.title = T
        self.lengths = L
        self.point = P
    def test(self):
        pass
    def succeed(self):
            print(self.title + ": Succeeded")
    def fail(self):
            print(self.title + ": Failed")
class Validity_Test (Test):
    def __init__(self, T, L, P, V):
        super().__init__(T, L, P)
        self.is_valid = V
class Two_Joint_Validity_Test (Validity_Test):
    def test(self):
        if len(self.lengths) < 2:
            print(self.title + " has too few lengths for a two joint test")
            self.fail()
        elif len(self.lengths) > 2:
            print(self.title + " has too many lengths for a two joint test")
            self.fail()
        elif two_joint_validity(self.lengths[0], self.lengths[1],
                                      self.point) == self.is_valid:
            self.succeed()
        else:
            self.fail()
class Two_Joint_Test (Test):
    def test(self):
        if len(self.lengths) < 2:
            print(self.title + " has too few lengths for a two joint test")
            self.fail()
        elif len(self.lengths) > 2:
            print(self.title + " has too many lengths for a two joint test")
            self.fail()
        elif two_jointed_arm_ik(self.lengths[0], self.lengths[1], self.point) != None:
            self.succeed()
        else:
            self.fail()
class N_Joint_Validity_Test (Validity_Test):
    def test(self):
        if n_joint_validity(self.lengths, self.point) == self.is_valid:
            self.succeed()
        else:
            self.fail()
class N_Joint_Test (Test):
    def test(self):
        # TODO: loop through weights
        success = True
        for i in range(101):
            weight = i / 100.0
            angles = n_jointed_arm_ik(self.lengths, weight, self.point)
            if (angles == None) or not recreate_point(self.lengths,
                                                      angles).equals(self.point):
                print("With weight: " + str(weight) + ",")
                success = False
                break
        if success:
            self.succeed()
        else:
            self.fail()

two_joint_validity_test_1 = Two_Joint_Validity_Test("Two Joint Validity Test #1",
                                                    [10, 1], Vector(5.0, 0.0), False)
two_joint_validity_test_1.test()
two_joint_validity_test_2 = Two_Joint_Validity_Test("Two Joint Validity Test #2",
                                                    [1, 10], Vector(5.0, 0.0), False)
two_joint_validity_test_2.test()
two_joint_validity_test_3 = Two_Joint_Validity_Test("Two Joint Validity Test #3",
                                                    [10, 1], Vector(9.0, 0.0), True)
two_joint_validity_test_3.test()

two_joint_ik_test_1 = Two_Joint_Test("Two Joint IK Test #1", [3, 4], Vector(7.0, 0.0))
two_joint_ik_test_1.test()

two_joint_ik_test_2 = Two_Joint_Test("Two Joint IK Test #2", [1, 7], Vector(0, 6.5))
two_joint_ik_test_2.test()

two_joint_ik_test_3 = Two_Joint_Test("Two Joint IK Test #3", [1, 7], Vector(-6.5, 0.0))
two_joint_ik_test_3.test()

two_joint_ik_test_4 = Two_Joint_Test("Two Joint IK Test #4", [2, 2], Vector(0, -3))
two_joint_ik_test_4.test()


n_joint_validity_test_1 = N_Joint_Validity_Test("N Joint Validity Test #1",
                                                [2, 6, 5], Vector(0.5, 0.0), True)
n_joint_validity_test_1.test()


n_joint_ik_test_1 = N_Joint_Test("N Joint IK Test #1", [1, 3, 4], Vector(5.5, 0.0))
n_joint_ik_test_1.test()

n_joint_ik_test_2 = N_Joint_Test("N Joint IK Test #2", [1, 1, 1, 1, 1, 4, 3, 1, 1],
                                 Vector(6.0, 0.0))
n_joint_ik_test_2.test()

n_joint_ik_test_3 = N_Joint_Test("N Joint IK Test #3",
                                 [1, 1, 1, 1, 1, 4, 3, 1, 1, 1, 1, 1],
                                 Vector(6.0, 0.0))
n_joint_ik_test_3.test()

n_joint_ik_test_4 = N_Joint_Test("N Joint IK Test #4",
                                 [1, 1, 1, 1, 1, 1, 0.1, 0.01, 0.1, 2, 3, 4],
                                 Vector(6.0, 0.0))
n_joint_ik_test_4.test()

n_joint_ik_test_5 = N_Joint_Test("N Joint IK Test #5", [1, 2, 3, 4, 2, 2],
                                 Vector(4.0, 0.0))
n_joint_ik_test_5.test()

n_joint_ik_test_6 = N_Joint_Test("N Joint IK Test #6", [1, 1, 1], Vector(0.1, 0.0))
n_joint_ik_test_6.test()

n_joint_ik_test_7 = N_Joint_Test("N Joint IK Test #7", [1, 0.5, 3], Vector(1.51, 0.0))
n_joint_ik_test_7.test()

print("TODO: fix problem with lower multiplier bound in n-joint solutions")
