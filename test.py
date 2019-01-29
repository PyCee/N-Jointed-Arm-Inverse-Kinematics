
from n_jointed_arm_ik import *
from vector import *
from arc_bounded_area import *
import math
import sys

class Test:
    def __init__(self, T):
        self.title = T
        self.succeeded = False
    def test(self):
        pass
    def succeed(self):
        self.succeeded = True
        print(self.title + ": Succeeded")
    def fail(self):
        self.succeeded = False
        print(self.title + ": Failed")
class Inverse_Kinematics_Test (Test):
    def __init__(self, T, L, P, V):
        super().__init__(T)
        self.lengths = L
        self.point = P
        self.is_valid = V
class Two_Joint_Validity_Test (Inverse_Kinematics_Test):
    def test(self):
        if two_joint_validity(self.lengths[0], self.lengths[1],
                              self.point) == self.is_valid:
            self.succeed()
        else:
            self.fail()
class N_Joint_Validity_Test (Inverse_Kinematics_Test):
    def test(self):
        if n_joint_validity(self.lengths, self.point) == self.is_valid:
            self.succeed()
        else:
            self.fail()
class Two_Joint_Test (Inverse_Kinematics_Test):
    def test(self):
        try:
            angles = two_jointed_arm_ik(self.lengths[0],
                                        self.lengths[1], self.point)
            if(self.point == recreate_point(self.lengths, angles)):
                self.succeed()
            else:
                self.fail()
        except:
            if self.is_valid:
                self.fail()
            else:
                self.succeed()
class N_Joint_Test (Inverse_Kinematics_Test):
    def test(self):
        for i in range(101):
            weight = i / 100.0
            angles = n_jointed_arm_ik(self.lengths,
                                      [weight] * (len(self.lengths) - 2),
                                      self.point)
            if (angles == None) or \
               not recreate_point(self.lengths,
                                  angles) == self.point:
                print("With weight: " + str(weight) + ",")
                self.fail()
                return
        self.succeed()
class N_Joint_Limit_Test (Test):
    def __init__(self, T, L, P, V, LOW_LIM, UPP_LIM):
        super().__init__(T, L, P, V)
        self.lower_limits = LOW_LIM
        self.upper_limits = UPP_LIM
    def test(self):
        
        angles = n_jointed_arm_limit_ik(self.lengths,
                                        self.lower_limits,
                                        self.upper_limits,
                                        [1.0] * (len(self.lengths) - 2),
                                        self.point)
        if (angles == None) or \
           not recreate_point(self.lengths,
                              angles) == self.point:
            print("With weight: " + str(weight) + ",")
            self.fail()
            return
        
        # Check that resulting angles are within limits
        for i in range(len(self.lengths)):
            if (self.upper_limits[i] != None and \
                angles[i] > self.upper_limits[i]) or \
                (self.lower_limits[i] != None and \
                 angles[i] < self.lower_limits[i]):
                self.fail()
                return
        self.succeed()
class Arc_Test (Test):
    def __init__(self):
        pass
        

two_joint_validity_test_1 = Two_Joint_Validity_Test("Two Joint Validity Test #1",
                                                    [10, 1], Vector(5.0, 0.0), False)
two_joint_validity_test_1.test()
two_joint_validity_test_2 = Two_Joint_Validity_Test("Two Joint Validity Test #2",
                                                    [1, 10], Vector(5.0, 0.0), False)
two_joint_validity_test_2.test()
two_joint_validity_test_3 = Two_Joint_Validity_Test("Two Joint Validity Test #3",
                                                    [10, 1], Vector(9.0, 0.0), True)
two_joint_validity_test_3.test()

two_joint_ik_test_1 = Two_Joint_Test("Two Joint IK Test #1", [3, 4], Vector(7.0, 0.0), True)
two_joint_ik_test_1.test()

two_joint_ik_test_2 = Two_Joint_Test("Two Joint IK Test #2", [1, 7], Vector(0, 6.5), True)
two_joint_ik_test_2.test()

two_joint_ik_test_3 = Two_Joint_Test("Two Joint IK Test #3", [1, 7], Vector(-6.5, 0.0), True)
two_joint_ik_test_3.test()

two_joint_ik_test_4 = Two_Joint_Test("Two Joint IK Test #4", [2, 2], Vector(0, -3), True)
two_joint_ik_test_4.test()
'''
two_joint_ik_test_5 = Two_Joint_Test("Two Joint IK Test #5", [2, 2], Vector(0, 5), True)
two_joint_ik_test_5.test()
'''
n_joint_validity_test_1 = N_Joint_Validity_Test("N Joint Validity Test #1",
                                                [2, 6, 5], Vector(0.5, 0.0), True)
n_joint_validity_test_1.test()


n_joint_ik_test_1 = N_Joint_Test("N Joint IK Test #1", [1, 3, 4], Vector(5.5, 0.0), True)
n_joint_ik_test_1.test()

n_joint_ik_test_2 = N_Joint_Test("N Joint IK Test #2", [1, 1, 1, 1, 1, 4, 3, 1, 1],
                                 Vector(6.0, 0.0), True)
n_joint_ik_test_2.test()

n_joint_ik_test_3 = N_Joint_Test("N Joint IK Test #3",
                                 [1, 1, 1, 1, 1, 4, 3, 1, 1, 1, 1, 1],
                                 Vector(6.0, 0.0), True)
n_joint_ik_test_3.test()

n_joint_ik_test_4 = N_Joint_Test("N Joint IK Test #4",
                                 [1, 1, 1, 1, 1, 1, 0.1, 0.01, 0.1, 2, 3, 4],
                                 Vector(6.0, 0.0), True)
n_joint_ik_test_4.test()

n_joint_ik_test_5 = N_Joint_Test("N Joint IK Test #5", [1, 2, 3, 4, 2, 2],
                                 Vector(4.0, 0.0), True)
n_joint_ik_test_5.test()

n_joint_ik_test_6 = N_Joint_Test("N Joint IK Test #6", [1, 1, 1], Vector(0.1, 0.0), True)
n_joint_ik_test_6.test()

n_joint_ik_test_7 = N_Joint_Test("N Joint IK Test #7", [1, 0.5, 3], Vector(1.51, 0.0), True)
n_joint_ik_test_7.test()

n_joint_ik_test_8 = N_Joint_Test("N Joint IK Test #8", [1, 1, 0.5, 3, 0.5, 4],
                                 Vector(1.5, 0.0), True)
n_joint_ik_test_8.test()


d_90 = 3.14159 / 2.0
d_45 = d_90 / 2.0

original_arc = Arc(Vector(0.0, 0.0), 1, (0, d_45))
rotated_arc = original_arc.get_transformed_arc(d_45, 0.0)

desired_arc = Arc(Vector(0.0, 0.0), 1, (d_45, d_90))

if desired_arc == rotated_arc:
    print("arc success!")

try:
    bad_arc = Arc(Vector(0.0, 0.0), -1, (0, d_45))
    print("failed bad arc test")
except (InvalidArcRadius):
    print("bad arc test success!")

'''
n_joint_limit_test_1 = N_Joint_Limit_Test("N Joint Limit Test #1",
                                          [1.0, 1.0, 0.5], Vector(1.0, 0.0),
                                          True, [-3.14159 / 4.0, None, None],
                                          [0.0, None, None])
n_joint_limit_test_1.test()
'''
area = DualArcBoundedArea(1, 1, (0, d_90), (0, d_45))
#area = DualArcBoundedArea([1, 1], [(0, d_90), (0, d_45)])
