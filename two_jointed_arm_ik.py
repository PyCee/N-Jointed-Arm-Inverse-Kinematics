
from vector import Vector
from circle import Circle

class TwoJointOutOfRangeException (Exception):
    pass
class TwoJointLengthException (Exception):
    pass
def two_joint_range(length_1, length_2):
    '''
    return the lower and upper ranges of motionthe two jointed arm
    '''
    lower = max([length_1, length_2]) - min([length_1, length_2])
    upper = length_1 + length_2
    return lower, upper
def two_joint_validity(length_1, length_2, point):
    '''
    return True if a two jointed arm with arms of lengths
    length_1 and length_2 can reach point

    The valid range is length_2 away from length_1
    '''
    if length_1 < 0.0 or length_2 < 0.0:
        raise TwoJointLengthException
    r_1, r_2 = two_joint_range(length_1, length_2)
    
    # To help correct floating-point error
    r_1 *= 0.99999
    r_2 *= 1.00001
    
    distance = point.magnitude()
    return r_1 <= distance and distance <= r_2

def two_jointed_arm_ik(length_1, length_2, point):
    '''
    returns angles for a two arm inverse kinematics solution,
    angle is relative to parent
    
    It works by using data of 2 circles. One centered at (0, 0) with radius
    length_1, and the second centered at (distance, 0) with radius length_2.
    The position of the second joint should be the upper intersection point
    of the circles. It finds the intersection point, and calculates
    the angles for each joint.
    '''
    if not two_joint_validity(length_1, length_2, point):
        raise TwoJointOutOfRangeException
    circle_1 = Circle(Vector(0.0, 0.0), length_1)
    circle_2 = Circle(point, length_2)
    intersections = circle_1.get_intersections(circle_2)
    if len(intersections) == 0:
        raise TwoJointOutOfRangeException
    angle_1 = Vector(0.0, 0.0).get_angle(intersections[0])
    angle_2 = 3.14159
    if intersections[0] != point:
        angle_2 = intersections[0].get_angle(point) - angle_1
    return angle_1, angle_2
