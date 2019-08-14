import math
import sys
from vector import Vector
from recreate_point import recreate_point
from arc_bounded_area_contains import arc_bounded_area_contains_point
from n_jointed_arm_ik import OutOfRangeException, LengthException, LengthsWeightsNotMatchException
from two_jointed_arm_ik import two_jointed_arm_ik
from sweep import sweep_area
from arc import Arc

class LimitsException (Exception):
    pass

def limited_n_jointed_arm_range(lengths, lower_limits, upper_limits):
    '''
    Defines a set of curves that makes an area
    '''
    if len(lengths) < 2:
        pass
    if len(lengths) != len(lower_limits) or len(lengths) != len(upper_limits):
        raise LimitsException
    arcs = [Arc(Vector(0.0, 0.0), lengths[0], (lower_limits[0], upper_limits[0]))]
    for i in range(1, len(lengths)):
        arcs = sweep_area(arcs, lengths[i], (lower_limits[i], upper_limits[i]))
    return arcs

def limited_n_jointed_arm_validity(lengths, lower_limits, upper_limits,
                                   point):
    '''
    Checks if the point is in the area defined by n_jointed_arm_validity
    (Think perfect 3d model algorithm in 2d)
    '''
    arcs = limited_n_jointed_arm_range(lengths, lower_limits, upper_limits)
    return arc_bounded_area_contains_point(arcs, point)
'''
def limited_n_jointed_arm_ik(lengths, lower_limits, upper_limits,
                             weights, point):
    ''
    Calculates ik angles for joints with angle limits
    lower and upper limits are in radians
    ''
    
    if not limited_n_jointed_arm_validity(lengths, lower_limits, upper_limits, point):
        raise OutOfRangeException
    
    if len(lengths)-2 != len(weights):
        print("lengths: " + str(lengths))
        print("weights: " + str(weights))
        raise LengthsWeightsNotMatchException
    
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
                ''
                print("lesser: " + str(lesser_angle))
                print("greater: " + str(greater_angle))
                ''
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
                ''
                print("min: " + str(min_length_2))
                print("max: " + str(max_length_2))
                ''
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
'''
def limited_n_jointed_arm_ik(lengths, lower_limits, upper_limits,
                             weights, point):
    '''
    Calculates ik angles for joints with angle limits
    lower and upper limits are in radians
    '''
    
    if not limited_n_jointed_arm_validity(lengths, lower_limits, upper_limits, point):
        raise OutOfRangeException
    
    if len(lengths)-2 != len(weights):
        print("lengths: " + str(lengths))
        print("weights: " + str(weights))
        raise LengthsWeightsNotMatchException
    
    resulting_angles = [0] * len(lengths)
    for index in range(len(lengths)-1):
        # Calculate multiplier based on weight
        mult = 1.0
        length_1 = lengths[index]
        length_2 = sum(lengths[index+1:])
        a_1 = 0.0
        a_2 = 0.0
        if index < len(lengths)-2:
            low, upp = n_jointed_arm_range(lengths[index+1:])
            min_length_2 = max(low,
                               math.fabs(point.magnitude() - length_1))
            max_length_2 = min(upp, point.magnitude() + length_1)
            length_range = max_length_2 - min_length_2
            weighted_range = weights[index] * length_range
            length_2 = min_length_2 + weighted_range
        # Run a two jointed arm ik to find the angle for this joint
        angles = two_jointed_arm_ik(length_1, length_2, point)
        if angles == None:
            return None
        a_1, a_2 = angles

        # End of "if not point.magnitude() == 0.0:"
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
