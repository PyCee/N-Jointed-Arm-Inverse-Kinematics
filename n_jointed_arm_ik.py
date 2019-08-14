import math
import sys
from vector import Vector
from circle import Circle
from recreate_point import recreate_point
from two_jointed_arm_ik import two_jointed_arm_ik

class OutOfRangeException (Exception):
    pass
class LengthException (Exception):
    pass
class LengthsWeightsNotMatchException (Exception):
    pass
    
def n_jointed_arm_range(L):
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
    
def n_jointed_arm_validity(L, point):
    '''
    returns True if an N-jointed arm with lengths array L
    can reach point
    '''
    for length in L:
        if length < 0.0:
            raise LengthException
    r_1, r_2 = n_jointed_arm_range(L)
    distance = point.magnitude()
    return r_1 <= distance and distance <= r_2

def n_jointed_arm_ik(lengths, weights, point):
    if not n_jointed_arm_validity(lengths, point):
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
