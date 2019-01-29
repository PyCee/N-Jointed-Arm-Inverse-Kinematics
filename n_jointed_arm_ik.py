import math
import sys
from vector import Vector

class OutOfRange(Exception):
    pass
class LengthsWeightsNotMatch(Exception):
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
    r_1, r_2 = two_joint_range(length_1, length_2)
    
    # To help correct error
    r_1 *= 0.99999
    r_2 *= 1.00001
    
    distance = point.magnitude()
    
    return r_1 <= distance and distance <= r_2
    
def n_joint_range(L):
    '''
    return the lower and upper bounds of the n-jointed arm's range
    '''
    lengths = L[:]
    lengths.sort(reverse=True)
    index = 1
    for i in range(1, len(lengths)):
        r_1 = sum(lengths[:i])
        r_2 = sum(lengths[i:])
        if r_1 < r_2:
            index = i
            break
    r_1 = sum(lengths[:index])
    r_2 = sum(lengths[index:])
    lower = max(r_1 - r_2, 0.0)
    upper = sum(lengths)
    return lower, upper
    
def n_joint_validity(L, point):
    '''
    returns True if an N-jointed arm with lengths array L
    can reach point
    '''
    r_1, r_2 = n_joint_range(L)
    distance = point.magnitude()
    return r_1 <= distance and distance <= r_2

def recreate_point(lengths, angles):
    recreated_point = Vector(0.0, 0.0)
    for index in range(len(lengths)):
        # For each index in [0, N-1]

        # Get angle in world space (stored in local space)
        absolute_angle = sum(angles[:index+1])

        # Add the transformed length to the recreated_point
        offset = Vector(lengths[index] * math.cos(absolute_angle),
                        lengths[index] * math.sin(absolute_angle))
        recreated_point = recreated_point + offset
    return recreated_point

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
        raise OutOfRange
    distance = point.magnitude()
    x_neg = point.x < 0.0
    relative_angle = 0.0
    x_1 = 0.0
    
    if not distance == 0:
        relative_angle = math.asin(point.y / distance)
        # Calculate the x value of the intersection points
        x_1 = (distance**2 - length_2**2 + length_1**2) / (2 * distance)
        
    x_2 = distance - x_1
        
    #TODO look here for jump at -270 degrees in gui
    if point.x < 0.0:
        relative_angle = 3.14159 - relative_angle
    # We use the lengths with the x values to calculate the
    #   x value on the unit circle, and use acos to get the angle
    base_1 = x_1 / length_1
    base_2 = x_2 / length_2

    base_1 = max(-1.0, base_1)
    base_2 = max(-1.0, base_2)
    base_1 = min(1.0, base_1)
    base_2 = min(1.0, base_2)
    
    angle_1 = math.acos(base_1)
    angle_2 = -1.0 * math.acos(base_2)
        
    angle_1 += relative_angle
    angle_2 += relative_angle - angle_1
    return angle_1, angle_2

def n_jointed_arm_ik(lengths, weights, point):
    if not n_joint_validity(lengths, point):
        raise OutOfRange
    if len(lengths)-2 != len(weights):
        print("lengths: " + str(lengths))
        print("weights: " + str(weights))
        raise LengthsWeightsNotMatch
    
    resulting_angles = [0] * len(lengths)
    for index in range(len(lengths)-1):
        # Calculate multiplier based on weight
        mult = 1.0
        length_1 = lengths[index]
        length_2 = sum(lengths[index+1:])
        a_1 = 0.0
        a_2 = 0.0
        if not point.magnitude() == 0.0:
            if index < len(lengths)-2:
                low, upp = n_joint_range(lengths[index+1:])
                
                min_length_2 = max((0.00000000001, low,
                                  math.fabs(point.magnitude() - length_1)))
                max_length_2 = min(upp, point.magnitude() + length_1)
                length_2 = min_length_2 + weights[index] * \
                           (max_length_2 - min_length_2)
                if length_2 == 0.0:
                    length_2 = 0.0000000001
            # Run a two jointed arm ik to find the angle for this joint
            angles = two_jointed_arm_ik(length_1, length_2, point)
            
            if angles == None:
                return None
            a_1, a_2 = angles
        # Store relative angle values
        resulting_angles[index] += a_1
        if index >= 1:
            resulting_angles[index] -= sum(resulting_angles[:index])
        if index == len(lengths)-2:
            resulting_angles[index+1] = a_2
            
        # Subtract current progress to the point
        absolute_angle = sum(resulting_angles[:index+1])
        offset = Vector(lengths[index] * math.cos(absolute_angle),
                        lengths[index] * math.sin(absolute_angle))
        point = point - offset
    return resulting_angles

def n_jointed_arm_limit_validity(lengths, lower_limits, upper_limits):
    '''
    Defines a set of curves that makes an area
    '''
    pass

def n_jointed_arm_limit_valid_point(lengths, lower_limits, upper_limits,
                                    point):
    '''
    Checks if the point is in the area defined by n_jointed_arm_validity
    (Think perfect 3d model algorithm in 2d)
    '''
    pass

def n_jointed_arm_limit_ik(lengths, lower_limits, upper_limits,
                           weights, point):
    '''
    Calculates ik angles for joints with angle limits
    lower and upper limits are in radians
    limits must be in [180, -180]
    '''

    ###TODO: Validate joints: check that upper limit for a joint is > the lower limit for that joint

    ###TODO: change this to limit validity function
    if not n_joint_validity(lengths, point):
        raise OutOfRange
    
    if len(lengths)-2 != len(weights):
        print("lengths: " + str(lengths))
        print("weights: " + str(weights))
        raise LengthsWeightsNotMatch
    
    resulting_angles = [0] * len(lengths)
    for index in range(len(lengths)-1):
        # Calculate multiplier based on weight

        mult = 1.0
        length_1 = lengths[index]
        length_2 = sum(lengths[index+1:])
        a_1 = 0.0
        a_2 = 0.0
        if not point.magnitude() == 0.0:
            if index < len(lengths)-2:
                low, upp = n_joint_range(lengths[index+1:])
                
                lesser_angle = 0.0
                greater_angle = 0.0
                
                if (lower_limits[index] == None or
                    lower_limits[index] < 0.0) and \
                    (upper_limits[index] == None or
                     upper_limits[index] > 0.0):
                    lesser_angle = 0.0
                elif lower_limits[index] == None:
                    lesser_angle = upper_limits[index]
                elif upper_limits[index] == None:
                    lesser_angle = lower_limits[index]
                else:
                    lesser_angle = min(math.fabs(lower_limits[index]),
                                       math.fabs(upper_limits[index]))
                if lower_limits[index] == None:
                    greater_angle = upper_limits[index]
                elif upper_limits[index] == None:
                    greater_angle = lower_limits[index]
                else:
                    greater_angle = max(math.fabs(lower_limits[index]),
                                        math.fabs(upper_limits[index]))
                '''
                print("lesser: " + str(lesser_angle))
                print("greater: " + str(greater_angle))
                '''
                closer_point = Vector(math.cos(lesser_angle),
                                      math.sin(lesser_angle)).scale(length_1)
                further_point = Vector(math.cos(greater_angle),
                                       math.sin(greater_angle)).scale(length_1)
                lesser_dist = point.subtract(closer_point).magnitude()
                greater_dist = point.subtract(further_point).magnitude()
                
                min_length_2 = max((0.00000000001, low, lesser_dist))
                max_length_2 = min(upp, greater_dist)
                length_2 = min_length_2 + weights[index] * \
                           (max_length_2 - min_length_2)
                '''
                print("min: " + str(min_length_2))
                print("max: " + str(max_length_2))
                '''
                if length_2 == 0.0:
                    length_2 = 0.0000000001
            # Run a two jointed arm ik to find the angle for this joint
            angles = two_jointed_arm_ik(length_1, length_2, point)
            
            if angles == None:
                return None
            a_1, a_2 = angles
            
        # If a_1 must be negative due to limits
        if upper_limits[index] != None and a_1 > upper_limits[index] and \
           (lower_limits[index] == None or -1.0 * a_1 >= lower_limits[index]):
            a_1 *= -1.0
            a_2 *= -1.0
        
        # Store relative angle values
        resulting_angles[index] += a_1
        if index >= 1:
            resulting_angles[index] -= sum(resulting_angles[:index])
        if index == len(lengths)-2:
            resulting_angles[index+1] = a_2
            
        # Subtract current progress to the point
        absolute_angle = sum(resulting_angles[:index+1])
        offset = Vector(lengths[index] * math.cos(absolute_angle),
                        lengths[index] * math.sin(absolute_angle))
        point = point - offset
    return resulting_angles
