
from n_jointed_arm_ik import *
from vector import *
from arc_bounded_area import *
import math
import sys

test_list = []
def Add_Test(test):
    test_list.append(test)
def Run_Tests():
    success = True
    for curr_test in test_list:
        curr_test.test()
        if not curr_test.succeeded:
            success = False
    if success:
        print("All Tests Succeeded")
    else:
        print("No Success")

SUCCESS_OUTPUT = False
class Test:
    def __init__(self, T, E):
        self.title = T
        self.expected_success = E
        self.succeeded = False
        Add_Test(self)
    def test(self):
        pass
    def end(self, success):
        if success == self.expected_success:
            self.succeed()
        else:
            self.fail()
    def succeed(self):
        self.succeeded = True
        if SUCCESS_OUTPUT:
            print(self.title + ": Succeeded")
    def fail(self):
        self.succeeded = False
        print(self.title + ": Failed")
class Inverse_Kinematics_Test (Test):
    def __init__(self, T, E, L, P):
        super().__init__(T, E)
        self.lengths = L
        self.point = P
class Two_Joint_Validity_Test (Inverse_Kinematics_Test):
    def test(self):
        if two_joint_validity(self.lengths[0], self.lengths[1],
                              self.point):
            self.end(True)
        else:
            self.end(False)
class N_Joint_Validity_Test (Inverse_Kinematics_Test):
    def test(self):
        if n_joint_validity(self.lengths, self.point):
            self.end(True)
        else:
            self.end(False)
class Two_Joint_Test (Inverse_Kinematics_Test):
    def test(self):
        try:
            angles = two_jointed_arm_ik(self.lengths[0],
                                        self.lengths[1], self.point)
            if(self.point == recreate_point(self.lengths, angles)):
                self.end(True)
            else:
                self.end(False)
        except:
            self.end(False)
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
                self.end(False)
                return
        self.end(True)
class Arc_Creation_Test (Test):
    def __init__(self, T, E, origin, radius, limits):
        super().__init__(T, E)
        self.origin = origin
        self.radius = radius
        self.limits = limits
    def test(self):
        try:
            Arc(self.origin, self.radius, self.limits)
            self.end(True)
        except:
            self.end(False)
class Arc_Equality_Test (Test):
    def __init__(self, T, E, arc1, arc2):
        super().__init__(T, E)
        self.arc1 = arc1
        self.arc2 = arc2
    def test(self):
        self.end(self.arc1 == self.arc2)
class Arc_Transformation_Test (Test):
    def __init__(self, T, E, start_arc, radians, length, resulting_arc):
        super().__init__(T, E)
        self.start_arc = start_arc
        self.radians = radians
        self.length = length
        self.resulting_arc = resulting_arc
    def test(self):
        resulting_arc = self.start_arc.get_transformed_arc(self.radians,
                                                           self.length)
        self.end(resulting_arc == self.resulting_arc)
class Arc_Extremes_Test (Test):
    def __init__(self, T, E, arc, extremes):
        super().__init__(T, E)
        self.arc = arc
        self.extremes = extremes
    def test(self):
        result = True
        resulting_extremes = self.arc.get_extremes()

        # Check that extremes match
        if len(resulting_extremes) != len(self.extremes):
            result = False
        for extreme in resulting_extremes:
            if extreme not in self.extremes:
                result = False
            
        self.end(result)
        
class N_Joint_Limit_Test (Test):
    def __init__(self, T, E, L, P, LOW_LIM, UPP_LIM):
        super().__init__(T, E, L, P)
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
            self.end(False)
            return
        
        # Check that resulting angles are within limits
        for i in range(len(self.lengths)):
            if (self.upper_limits[i] != None and \
                angles[i] > self.upper_limits[i]) or \
                (self.lower_limits[i] != None and \
                 angles[i] < self.lower_limits[i]):
                self.end(False)
                return
        self.end(True)
    

'''
Test Two Joint Validity
'''
Two_Joint_Validity_Test("Two Joint Validity Test #1", True,
                        [10, 1], Vector(9.0, 0.0))
Two_Joint_Validity_Test("Two Joint Validity Test #2", False,
                        [10, 1], Vector(5.0, 0.0))
Two_Joint_Validity_Test("Two Joint Validity Test #3", False, 
                        [1, 10], Vector(5.0, 0.0))
'''
Test Two Joint IK
'''
Two_Joint_Test("Two Joint IK Test #1", True,
               [3, 4], Vector(7.0, 0.0))
Two_Joint_Test("Two Joint IK Test #2", True,
               [1, 7], Vector(0, 6.5))
Two_Joint_Test("Two Joint IK Test #3", True,
               [1, 7], Vector(-6.5, 0.0))
Two_Joint_Test("Two Joint IK Test #4", True,
               [2, 2], Vector(0, -3))
Two_Joint_Test("Two Joint IK Test #5", False,
               [2, 2], Vector(0, 5))

'''
Test N Joint Valididty
'''
N_Joint_Validity_Test("N Joint Validity Test #1", True,
                      [2, 6, 5], Vector(0.5, 0.0))
'''
Test N Joint IK
'''
N_Joint_Test("N Joint IK Test #1", True,
             [1, 3, 4], Vector(5.5, 0.0))
N_Joint_Test("N Joint IK Test #2", True,
             [1, 1, 1, 1, 1, 4, 3, 1, 1], Vector(6.0, 0.0))
N_Joint_Test("N Joint IK Test #3", True,
             [1, 1, 1, 1, 1, 4, 3, 1, 1, 1, 1, 1], Vector(6.0, 0.0))
N_Joint_Test("N Joint IK Test #4", True,
             [1, 1, 1, 1, 1, 1, 0.1, 0.01, 0.1, 2, 3, 4], Vector(6.0, 0.0))
N_Joint_Test("N Joint IK Test #5", True,
             [1, 2, 3, 4, 2, 2], Vector(4.0, 0.0))
N_Joint_Test("N Joint IK Test #6", True,
             [1, 1, 1], Vector(0.1, 0.0))
N_Joint_Test("N Joint IK Test #7", True,
             [1, 0.5, 3], Vector(1.51, 0.0))
N_Joint_Test("N Joint IK Test #8", True,
             [1, 1, 0.5, 3, 0.5, 4], Vector(1.5, 0.0))

d_180 = 3.14159
d_90 = d_180 / 2.0
d_45 = d_180 / 4.0
d_30 = d_180 / 6.0
d_225 = d_180 + d_45

'''
Test Arc Creation
'''
Arc_Creation_Test("Arc Creation Test #1", True,
                  Vector(0.0, 0.0), 1.0, (0.0, d_45))
Arc_Creation_Test("Arc Creation Test #2", False,
                  Vector(0.0, 0.0), -1.0, (0.0, d_45))
Arc_Creation_Test("Arc Creation Test #3", False,
                  Vector(0.0, 0.0), 1.0, (d_45, d_45))
Arc_Creation_Test("Arc Creation Test #4", False,
                  Vector(0.0, 0.0), 1.0, (d_90, d_45))
'''
Test Arc Equality
'''
Arc_Equality_Test("Arc Equality Test #1", True,
                  Arc(Vector(0.0, 0.0), 1, (0, d_45)),
                  Arc(Vector(0.0, 0.0), 1, (0, d_45)))
Arc_Equality_Test("Arc Equality Test #2", False,
                  Arc(Vector(0.0, 0.0), 1, (0, d_45)),
                  Arc(Vector(1.0, 0.0), 1, (0, d_45)))
Arc_Equality_Test("Arc Equality Test #3", False,
                  Arc(Vector(0.0, 0.0), 1, (0, d_45)),
                  Arc(Vector(0.0, 0.0), 2, (0, d_45)))
Arc_Equality_Test("Arc Equality Test #4", False,
                  Arc(Vector(0.0, 0.0), 1, (0, d_45)),
                  Arc(Vector(0.0, 0.0), 1, (d_45, d_90)))

'''
Test Arc Transformation
'''
Arc_Transformation_Test("Arc Transformation Test #1", True,
                        Arc(Vector(0.0, 0.0), 1, (0.0, d_45)),
                        d_45, 0.0,
                        Arc(Vector(0.0, 0.0), 1, (d_45, d_90)))
Arc_Transformation_Test("Arc Transformation Test #2", True,
                        Arc(Vector(0.0, 0.0), 1, (-d_45, 0.0)),
                        d_90, 0.0,
                        Arc(Vector(0.0, 0.0), 1, (d_45, d_90)))
Arc_Transformation_Test("Arc Transformation Test #3", True,
                        Arc(Vector(0.0, 0.0), 1, (0.0, d_45)),
                        d_45, 1.0,
                        Arc(Vector(0.7071, 0.7071), 1, (d_45, d_90)))
Arc_Transformation_Test("Arc Transformation Test #4", False,
                        Arc(Vector(0.0, 0.0), 1, (0.0, d_45)),
                        d_90, 0.0,
                        Arc(Vector(0.0, 0.0), 1, (d_45, d_90)))
Arc_Transformation_Test("Arc Transformation Test #5", False,
                        Arc(Vector(0.0, 0.0), 1, (0.0, d_45)),
                        d_45, 1.0,
                        Arc(Vector(0.0, 0.0), 1, (d_45, d_90)))
Arc_Transformation_Test("Arc Transformation Test #6", False,
                        Arc(Vector(1.0, 0.0), 1, (0.0, d_45)),
                        d_45, 0.0,
                        Arc(Vector(0.0, 0.0), 1, (d_45, d_90)))
'''
Test Arc Extremes
'''
Arc_Extremes_Test("Arc Extremes Test #1", True,
                  Arc(Vector(0.0, 0.0), 1, (0.0, d_90)),
                  (Vector(1.0, 0.0), Vector(0.0, 1.0)))
Arc_Extremes_Test("Arc Extremes Test #2", True,
                  Arc(Vector(0.0, 0.0), 2, (0.0, d_90)),
                  (Vector(2.0, 0.0), Vector(0.0, 2.0)))
Arc_Extremes_Test("Arc Extremes Test #3", True,
                  Arc(Vector(0.0, 0.0), 1, (d_90, d_180)),
                  (Vector(-1.0, 0.0), Vector(0.0, 1.0)))
Arc_Extremes_Test("Arc Extremes Test #4", True,
                  Arc(Vector(0.0, 0.0), 1, (d_45, d_90)),
                  (Vector(0.7071, 0.7071), Vector(0.0, 1.0)))
Arc_Extremes_Test("Arc Extremes Test #5", True,
                  Arc(Vector(0.0, 0.0), 1, (-d_45, d_90)),
                  (Vector(1.0, 0.0), Vector(0.0, 1.0),
                   Vector(0.7071, -0.7071)))
Arc_Extremes_Test("Arc Extremes Test #6", True,
                  Arc(Vector(0.0, 0.0), 1, (d_90, d_225)),
                  (Vector(-0.7071, -0.7071), Vector(0.0, 1.0),
                   Vector(-1.0, 0.0)))
Arc_Extremes_Test("Arc Extremes Test #7", True,
                  Arc(Vector(0.0, 0.0), 1, (-d_45, d_225)),
                  (Vector(-0.7071, -0.7071), Vector(0.7071, -0.7071),
                   Vector(1.0, 0.0), Vector(-1.0, 0.0)))

'''
N_Joint_Limit_Test("N Joint Limit Test #1",
                   [1.0, 1.0, 0.5], Vector(1.0, 0.0),
                   True, [-3.14159 / 4.0, None, None],
                   [0.0, None, None])
'''

#area = DualArcBoundedArea([1, 1], [(0, d_90), (0, d_45)])


Run_Tests()
