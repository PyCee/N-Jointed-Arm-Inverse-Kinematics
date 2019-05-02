
from n_jointed_arm_ik import *
from vector import *
from arc import Arc, Arc_Get_Break_Range
from sweep import get_swept_arc_subdivisions, get_swept_arc_bounds, sweep_area
from circle import Circle
from math import pi, fabs, trunc
from cull_arc_bounded_area import cull_arc_bounded_area
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
            break
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
            self.__succeed()
        else:
            self.__fail()
    def __succeed(self):
        self.succeeded = True
        if SUCCESS_OUTPUT:
            print(self.title + ": Succeeded")
    def __fail(self):
        self.succeeded = False
        print(self.title + ": Failed")
class Circle_Creation_Test (Test):
    def __init__(self, T, E, origin, radius):
        super().__init__(T, E)
        self.origin = origin
        self.radius = radius
    def test(self):
        try:
            Circle(self.origin, self.radius)
            self.end(True)
        except:
            self.end(False)
class Circle_Intersection_Test (Test):
    def __init__(self, T, E, circle1, circle2, expected_results):
        super().__init__(T, E)
        self.circle1 = circle1
        self.circle2 = circle2
        self.expected_results = expected_results
    def test(self):
        results = self.circle1.get_intersections(self.circle2)
        if len(results) != len(self.expected_results):
            self.end(False)
            return
        for result in results:
            if result not in self.expected_results:
                self.end(False)
                return
        self.end(True)
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
        success = True
        try:
            for i in range(101):
                weight = i / 100.0
                angles = n_jointed_arm_ik(self.lengths,
                                          [weight] * (len(self.lengths) - 2),
                                          self.point)
                if (angles == None) or \
                   not recreate_point(self.lengths,
                                      angles) == self.point:
                    print(self.point)
                    print(recreate_point(self.lengths, angles))
                    print(angles)
                    print("With weight: " + str(weight) + ",")
                    success = False
                    break
        except (Exception):
            success = False
        finally:
            self.end(success)
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
class Arc_Break_Range_Test (Test):
    def __init__(self, T, E, arc, break_range):
        super().__init__(T, E)
        self.arc = arc
        self.break_range = break_range
    def test(self):
        result = True
        resulting_ranges = Arc_Get_Break_Range(self.arc)
        if ((resulting_ranges[0] == None) != (self.break_range[0] == None)) or \
           (resulting_ranges[0] != None and \
            fabs(resulting_ranges[0] - self.break_range[0]) > 0.00001) or \
            ((resulting_ranges[1] == None) != (self.break_range[1] == None)) or \
            (resulting_ranges[1] != None and \
             fabs(resulting_ranges[1] - self.break_range[1]) > 0.00001):
            result = False
        self.end(result)
class Swept_Arc_Subdivision_Test (Test):
    def __init__(self, T, E, start_arc, index, offset_length, sweep_radians,
                 resulting_base, resulting_arcs):
        super().__init__(T, E)
        self.start_arc = start_arc
        self.index = index
        self.offset_length = offset_length
        self.sweep_radians = sweep_radians
        self.resulting_base = resulting_base
        self.resulting_arcs = resulting_arcs
    def test(self):
        result = True
        base, arcs = get_swept_arc_subdivisions(self.start_arc,
                                                self.index,
                                                self.offset_length,
                                                self.sweep_radians)
        if base != self.resulting_base:
            print("base differs")
            result = False
        elif len(arcs) != len(self.resulting_arcs):
            print("number of arcs differs")
            result = False
        else:
            for i in range(len(self.resulting_arcs)):
                if self.resulting_arcs[i] != arcs[i]:
                    print("arc index " + str(i) + " is incorrect")
                    result = False
                    break
        if not result:
            print("Calculated:")
            print((base, arcs))
            print("Expecting:")
            print((self.resulting_base, self.resulting_arcs))
            
        self.end(result)
class Swept_Arc_Bounds_Test (Test):
    def __init__(self, T, E, arc, length, limits, results):
        super().__init__(T, E)
        self.arc = arc
        self.length = length
        self.limits = limits
        self.results = results
    def test(self):
        result = True
        results = get_swept_arc_bounds(self.arc, self.length,
                                       self.limits)
        if results != self.results:
            result = False
        if not result:
            print("Expecting:")
            print(self.results)
            print("Calculated:")
            print(results)
            
        self.end(result)
        
class Cull_Arc_Bounded_Area_Test (Test):
    def __init__(self, T, E, arcs, results):
        super().__init__(T, E)
        self.arcs = arcs
        self.results = results
    def test(self):
        result = True
        results = cull_arc_bounded_area(self.arcs)
        if results != self.results:
            result = False
        if not result:
            print("Given:")
            print(self.arcs)
            print("Expecting:")
            for arc in self.results:
                print(arc)
            print("Calculated:")
            for arc in results:
                print(arc)
            
        self.end(result)
class Sweep_Area_Test (Test):
    def __init__(self, T, E, arcs, length, limits, results):
        super().__init__(T, E)
        self.arcs = arcs
        self.length = length
        self.limits = limits
        self.results = results
    def test(self):
        result = True
        results = sweep_area(self.arcs, self.length, self.limits)
        if results != self.results:
            result = False
        if not result:
            print("Expecting:")
            for arc in self.results:
                print(arc)
            print("Calculated:")
            for arc in results:
                print(arc)
            
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
Test Circle Creation
'''
Circle_Creation_Test("Circle Creation Test #1", True,
                     Vector(0.0, 0.0), 1.0)
Circle_Creation_Test("Circle Creation Test #2", True,
                     Vector(0.0, 0.0), 0.0)
Circle_Creation_Test("Circle Creation Test #3", False,
                     Vector(0.0, 0.0), -1.0)
'''
Test Circle Intersection
'''
Circle_Intersection_Test("Circle Intersection Test #1", True,
                         Circle(Vector(0.0, 0.0), 1.0),
                         Circle(Vector(1.0, 0.0), 1.0),
                         [Vector(0.5, 0.866), Vector(0.5, -0.866)])
Circle_Intersection_Test("Circle Intersection Test #2", True,
                         Circle(Vector(0.0, 0.0), 1.0),
                         Circle(Vector(1.0, 2.0), 2.0),
                         [Vector(-0.6, 0.8), Vector(1.0, 0.0)])
Circle_Intersection_Test("Circle Intersection Test #3", True,
                         Circle(Vector(0.0, 0.0), 1.0),
                         Circle(Vector(1.0, -2.0), 2.0),
                         [Vector(-0.6, -0.8), Vector(1.0, 0.0)])
Circle_Intersection_Test("Circle Intersection Test #4", True,
                         Circle(Vector(0.0, 0.0), 1.0),
                         Circle(Vector(2.0, 0.0), 1.0),
                         [Vector(1.0, 0.0)])
Circle_Intersection_Test("Circle Intersection Test #5", True,
                         Circle(Vector(0.0, 0.0), 1.0),
                         Circle(Vector(5.0, 0.0), 1.0),
                         [])
Circle_Intersection_Test("Circle Intersection Test #6", True,
                         Circle(Vector(0.0, 0.0), 3.0),
                         Circle(Vector(1.5, 0.0), 1.0),
                         [])
Circle_Intersection_Test("Circle Intersection Test #7", True,
                         Circle(Vector(0.0, 0.0), 1.0),
                         Circle(Vector(0.0, 0.0), 2.0),
                         [])
Circle_Intersection_Test("Circle Intersection Test #8", True,
                         Circle(Vector(0.0, 0.0), 1.0),
                         Circle(Vector(0.0, 0.0), 1.0),
                         [Vector(1.0, 0.0)])
Circle_Intersection_Test("Circle Intersection Test #9", True,
                         Circle(Vector(0.0, 0.0), 0.0),
                         Circle(Vector(1.0, 0.0), 1.0),
                         [Vector(0.0, 0.0)])
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
               [1, 1], Vector(1.0, 0.0))
Two_Joint_Test("Two Joint IK Test #2", False,
               [1, 1], Vector(3.0, 0.0))
Two_Joint_Test("Two Joint IK Test #3", True,
               [1, 1], Vector(2.0, 0.0))
Two_Joint_Test("Two Joint IK Test #4", True,
               [1, 1], Vector(0.0, 0.0))
Two_Joint_Test("Two Joint IK Test #5", True,
               [10.0, 1.0], Vector(11.0, 0.0))
Two_Joint_Test("Two Joint IK Test #6", True,
               [10.0, 1.0], Vector(-11.0, 0.0))
Two_Joint_Test("Two Joint IK Test #7", True,
               [10.0, 1.0], Vector(9.0, 0.0))
Two_Joint_Test("Two Joint IK Test #8", True,
               [10.0, 1.0], Vector(9.5, 0.0))
Two_Joint_Test("Two Joint IK Test #9", False,
               [10.0, 1.0], Vector(5.0, 0.0))
Two_Joint_Test("Two Joint IK Test #10", False,
               [1.0, -1.0], Vector(1.0, 0.0))

'''
Test N Joint Valididty
'''
#TODO: add n joint validity tests
N_Joint_Validity_Test("N Joint Validity Test #1", True,
                      [2, 6, 5], Vector(0.5, 0.0))
'''
Test N Joint IK
'''
N_Joint_Test("N Joint IK Test #1", True,
             [1, 1], Vector(1.0, 0.0))
N_Joint_Test("N Joint IK Test #2", True,
             [1, 1], Vector(-0.5, 0.5))
N_Joint_Test("N Joint IK Test #3", True,
             [1, 1, 1], Vector(1.0, 0.0))
N_Joint_Test("N Joint IK Test #4", True,
             [1, 1, 1], Vector(0.0, 0.0))
N_Joint_Test("N Joint IK Test #5", True,
             [1] * 20, Vector(10.0, 0.0))
N_Joint_Test("N Joint IK Test #6", True,
             [1, 2, 3, 4], Vector(5.5, 0.0))
N_Joint_Test("N Joint IK Test #7", True,
             [1, 0.5, 3], Vector(1.5, 0.0))
N_Joint_Test("N Joint IK Test #8", False,
             [10, 1], Vector(11.1, 0.0))
N_Joint_Test("N Joint IK Test #9", False,
             [10, 1], Vector(8.9, 0.0))
# Test for floating-point error correction
N_Joint_Test("N Joint IK Test #10", True,
             [1, 1, 1, 1, 1, 1, 0.1, 0.01, 0.1, 2, 3, 4], Vector(6.0, 0.0))


d_180 = pi
d_90 = d_180 / 2.0
d_45 = d_180 / 4.0
d_30 = d_180 / 6.0
d_15 = d_180 / 12.0
d_135 = d_45 * 3.0

'''
Test Arc Creation
'''
Arc_Creation_Test("Arc Creation Test #1", True,
                  Vector(0.0, 0.0), 1.0, (0.0, d_45))
Arc_Creation_Test("Arc Creation Test #2", False,
                  Vector(0.0, 0.0), -1.0, (0.0, d_45))
Arc_Creation_Test("Arc Creation Test #3", False,
                  Vector(0.0, 0.0), 1.0, (d_45, d_45))
'''
Test Arc Equality
'''
Arc_Equality_Test("Arc Equality Test #1", True,
                  Arc(Vector(0.0, 0.0), 1, (0, d_45)),
                  Arc(Vector(0.0, 0.0), 1, (0, d_45)))
Arc_Equality_Test("Arc Equality Test #2", True,
                  Arc(Vector(0.0, 0.0), 1, (0, -d_90)),
                  Arc(Vector(0.0, 0.0), 1, (0, d_180 + d_90)))
Arc_Equality_Test("Arc Equality Test #3", False,
                  Arc(Vector(0.0, 0.0), 1, (0, d_45)),
                  Arc(Vector(1.0, 0.0), 1, (0, d_45)))
Arc_Equality_Test("Arc Equality Test #4", False,
                  Arc(Vector(0.0, 0.0), 1, (0, d_45)),
                  Arc(Vector(0.0, 0.0), 2, (0, d_45)))
Arc_Equality_Test("Arc Equality Test #5", False,
                  Arc(Vector(0.0, 0.0), 1, (0, d_45)),
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
                  Arc(Vector(0.0, 0.0), 1, (d_90, -d_135)),
                  (Vector(-0.7071, -0.7071), Vector(0.0, 1.0),
                   Vector(-1.0, 0.0)))
Arc_Extremes_Test("Arc Extremes Test #7", True,
                  Arc(Vector(0.0, 0.0), 1, (-d_45, -d_135)),
                  (Vector(-0.7071, -0.7071), Vector(0.7071, -0.7071),
                   Vector(1.0, 0.0), Vector(-1.0, 0.0)))
'''
Test Arc Break Range
'''
Arc_Break_Range_Test("Arc Break Range Test #1", True,
                     Arc(Vector(0.0, 0.0), 1, (0.0, d_45)),
                     (None, None))
Arc_Break_Range_Test("Arc Break Range Test #2", True,
                     Arc(Vector(1.0, 0.0), 1, (-d_45, d_90)),
                     (0.7853981, None))
Arc_Break_Range_Test("Arc Break Range Test #3", True,
                     Arc(Vector(1.0, 0.0), 1, (-d_90, d_45)),
                     (None, 0.7853981))
Arc_Break_Range_Test("Arc Break Range Test #4", True,
                     Arc(Vector(2.0, 0.0), 1, (-d_45, d_90)),
                     (0.5109907, None))
Arc_Break_Range_Test("Arc Break Range Test #5", True,
                     Arc(Vector(5.0, 0.0), 0.5, (-d_45, d_90)),
                     (0.1318902, None))
Arc_Break_Range_Test("Arc Break Range Test #6", True,
                     Arc(Vector(1.0, .0), 1, (-d_90, d_90)),
                     (1.5707963, 1.5707963))
Arc_Break_Range_Test("Arc Break Range Test #7", True,
                     Arc(Vector(0.0, -1.0), 1, (-d_45, d_90)),
                     (None, None))
Arc_Break_Range_Test("Arc Break Range Test #8", True,
                     Arc(Vector(-2.0, 0.0), 1, (-d_45, d_90)),
                     (5.282237, None))
Arc_Break_Range_Test("Arc Break Range Test #9", True,
                     Arc(Vector(1.0, 0.0), 1, (d_90, -d_135)),
                     (None, 2.356194))
Arc_Break_Range_Test("Arc Break Range Test #10", True,
                     Arc(Vector(0.0, 0.0), 1, (-d_45, d_90)),
                     (None, None))

'''
Test Swept Arc Subdivision
'''
# Basic sweep with no subdivision
Swept_Arc_Subdivision_Test("Swept Arc Subdivision Test #1", True,
                         Arc(Vector(0.0, 0.0), 1.0, (0.0, d_180)),
                         0, 1, d_45,
                         Arc(Vector(0.0, 0.0), 1.0, (0.0, d_180)),
                         [])
# Sweep with no subdivision where limits are not same as
# potential extremes
Swept_Arc_Subdivision_Test("Swept Arc Subdivision Test #2", True,
                         Arc(Vector(0.0, 0.0), 1.0, (d_45, d_180)),
                         0, 1.0, d_45,
                         Arc(Vector(0.0, 0.0), 1.0, (d_45, d_180)),
                         [])
# Subdivision where sweep breaks arc
Swept_Arc_Subdivision_Test("Swept Arc Subdivision Test #3", True,
                           Arc(Vector(0.0, 0.0), 1.0,
                               (-d_45, d_180)),
                           0, 1.0, d_90,
                           Arc(Vector(0.0, 0.0), 1.0, (d_45, d_180)),
                           [Arc(Vector(1.0, 0.0), 1.0,
                                (-0.7853981634, 0.0)),
                            Arc(Vector(0.0, 0.0), 1.847759,
                                (-0.3926990817, 0.3926990817))])
# Subdivision where sweep breaks arc with second limit past extreme
Swept_Arc_Subdivision_Test("Swept Arc Subdivision Test #4", True,
                           Arc(Vector(0.0, 0.0), 1.0,
                               (-d_45, -d_135)),
                           0, 1.0, d_90,
                           Arc(Vector(0.0, 0.0), 1.0,
                               (d_45, -d_135)),
                           [Arc(Vector(1.0, 0.0), 1.0,
                                (-0.7853981634, 0.0)),
                            Arc(Vector(0.0, 0.0), 1.847759,
                                (-0.3926990817, 0.3926990817))])
# Subdivision where sweep does not break arc and aditional arc
Swept_Arc_Subdivision_Test("Swept Arc Subdivision Test #5", True,
                           Arc(Vector(0.0, 0.0), 1.0,
                               (-d_45, d_180)),
                           0, 1.0, d_15,
                           Arc(Vector(0.0, 0.0), 1.0,
                               (0.2617993878, d_180)),
                           [Arc(Vector(1.0, 0.0), 1.0,
                                (-0.7853981634, 0.0)),
                            Arc(Vector(0.0, 0.0), 1.847759,
                                (-0.3926990817, -0.1308996939)),
                            Arc(Vector(0.966, 0.259), 1.0,
                                (-0.5235987756, 0.0))])
# Subdivision where sweep does not break arc and adds an aditional arc, testing floating-point error
Swept_Arc_Subdivision_Test("Swept Arc Subdivision Test #6", True,
                           Arc(Vector(0.0, 0.0), 1.0,
                               (-d_45, d_180)),
                           0, 1.0, d_45,
                           Arc(Vector(0.0, 0.0), 1.0, (d_45, d_180)),
                           [Arc(Vector(1.0, 0.0), 1.0,
                                (-0.7853981634, 0.0)),
                            Arc(Vector(0.0, 0.0), 1.847759,
                                (-0.3926990817, 0.3926990817))])
# Subdivision with limit index [1], break arc
Swept_Arc_Subdivision_Test("Swept Arc Subdivision Test #7", True,
                           Arc(Vector(0.0, 0.0), 1.0,
                               (0.0, -d_90)),
                           1, 1.0, d_90,
                           Arc(Vector(0.0, 0.0), 1.0,
                               (0.0, d_90)),
                           [Arc(Vector(1.0, 0.0), 1.0,
                                (-3.1415926536, -1.5707963268)),
                            Arc(Vector(0.0, 0.0), 1.414214,
                                (-0.7853981634, 0.7853981634))])
# Subdivision with limit index [1], not breaking arc
Swept_Arc_Subdivision_Test("Swept Arc Subdivision Test #8", True,
                         Arc(Vector(0.0, 0.0), 1.0, (0.0, -d_90)),
                         1, 1.0, d_90,
                         Arc(Vector(0.0, 0.0), 1.0,
                             (0.0, 1.5707963268)),
                         [Arc(Vector(1.0, 0.0), 1.0,
                              (-3.1415926536, -1.5707963268)),
                          Arc(Vector(0.0, 0.0), 1.414214,
                              (-0.7853981634, 0.7853981634))])
# Subdivision where lower limit is overridden
Swept_Arc_Subdivision_Test("Swept Arc Subdivision Test #9", True,
                         Arc(Vector(0.0, 0.0), 1.0,
                             (d_135, 0.0)),
                         0, 1.0, d_90,
                         Arc(Vector(0.0, 0.0), 1.0,
                             (-3.1415926536, 0.0)),
                         [])
# Subdivision where upper limit is overridden
Swept_Arc_Subdivision_Test("Swept Arc Subdivision Test #10", True,
                         Arc(Vector(0.0, 0.0), 1.0,
                             (d_180, d_45)),
                         1, 1.0, d_90,
                         Arc(Vector(0.0, 0.0), 1.0,
                             (-3.1415926536, 0.0)),
                         [])
# Subdivision where limit[0] is equal to -1.0 * limit[1]
Swept_Arc_Subdivision_Test("Swept Arc Subdivision Test #11", True,
                         Arc(Vector(0.0, 0.0), 1.0,
                             (-d_45, d_45)),
                         0, 1.0, d_90,
                         None,
                         [Arc(Vector(1.0, 0.0), 1.0,
                              (-0.7853981634, 0.0)),
                          Arc(Vector(0.0, 0.0), 1.847759,
                              (-0.3926990817, 0.3926990817))])

'''
Test Swept Arc Bounds
'''
#Basic Swept Arc Bounds Test
Swept_Arc_Bounds_Test("Swept Arc Bounds Test #1", True,
                      Arc(Vector(0.0, 0.0), 1.0, (-d_90, d_45)),
                      1.0, (0.0, d_90),
                      ([Arc(Vector(1.0, 0.0), 1.0,
                            (-1.5707963268, 0.0))],
                       [Arc(Vector(0.0, 1.0), 1.0,
                            (1.5707963268, 2.3561944902)),
                        Arc(Vector(0.0, 0.0), 1.847759,
                            (1.1780972451, 1.9634954085)),
                        Arc(Vector(0.0, 1.0), 1.0,
                            (0.0, 0.7853981634))]))
'''
Test Area Arc Cull
'''
Cull_Arc_Bounded_Area_Test("Area Arc Cull Test #1", True,
                           [Arc(Vector(0.0, 0.0), 3.0, (0.0, 1.5707963)), Arc(Vector(0.0, 0.0), 1.0000000, (1.5707963, 3.1415926)), Arc(Vector(1.0, 0.0), 2.0, (0.0, 1.5707963)), Arc(Vector(2.0, 0.0), 1.0, (-1.570796, 0.0)), Arc(Vector(1.0, 0.0), 1.4142135, (-0.785398, 0.0)), Arc(Vector(0.0, 0.0), 2.2360679, (-0.463647, 0.4636476)), Arc(Vector(1.0, 1.0), 1.0, (1.5707963, 3.1415926)), Arc(Vector(1.0, 0.0), 1.4142135, (0.7853981, 2.3561944)), Arc(Vector(0.0, 1.0), 2.0, (1.5707963, 3.1415926)), Arc(Vector(0.0, 2.0), 1.0, (0.0, 1.5707963)), Arc(Vector(0.0, 1.0), 1.4142135, (1.5707963, 2.3561944)), Arc(Vector(0.0, 0.0), 2.2360679, (1.1071487, 2.0344439)), Arc(Vector(-1.0, 1.0), 1.0, (3.1415926, -1.570796)), Arc(Vector(0.0, 1.0), 1.4142135, (2.3561944, -2.356194))],
                           [Arc(Vector(0.0, 0.0), 3.0, (0.0, 1.5707963)), Arc(Vector(0.0, 0.0), 1.0000000, (1.5707963, 3.1415926)), Arc(Vector(2.0, 0.0), 1.0, (-1.570796, 0.0)), Arc(Vector(0.0, 0.0), 2.2360679, (-0.463647, 0.4636476)), Arc(Vector(1.0, 0.0), 1.4142135, (0.7853981, 2.3561944)), Arc(Vector(0.0, 1.0), 2.0, (1.5707963, 3.1415926)), Arc(Vector(-1.0, 1.0), 1.0, (3.1415926, -1.570796))])
'''
Test Sweep Area
'''
Sweep_Area_Test("Sweep Area Test #1", True,
                [Arc(Vector(0.0, 0.0), 1.0, [-d_90, d_90])],
                1.0, (0.0, d_90),
                [Arc(Vector(0.0, 0.0), 2.0,
                     (0.0, 1.5707963268)),
                 Arc(Vector(1.0, 0.0), 1.0,
                     (-1.5707963268, 0.0)),
                 Arc(Vector(0.0, 0.0), 1.414214,
                     (-0.7853981634, 0.7853981634)),
                 Arc(Vector(0.0, 1.0), 1.0,
                     (1.5707963268, 3.1415926536)),
                 Arc(Vector(0.0, 0.0), 1.414214,
                     (0.7853981634, 2.3561944902))])



Run_Tests()
