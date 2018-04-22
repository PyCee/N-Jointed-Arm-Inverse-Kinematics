import math
import sys

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return "(" + str(round(self.x, 3)) + ", " + str(round(self.y, 3)) + ")"
    def scale(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    def add(self, vec):
        return Vector(self.x + vec.x, self.y + vec.y)
    def subtract(self, vec):
        return self.add(vec.scale(-1.0))
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
    def equals(self, vec):
        return math.fabs(self.x - vec.x) < 0.01 and \
            math.fabs(self.y - vec.y) < 0.01
    

def two_joint_point_validity(length_1, length_2, point):
    '''
    return True if a two jointed arm with arms of lengths
    length_1 and length_2 can reach point

    The valid range is length_2 away from length_1
    '''

    # To help correct error
    length_2 *= 1.000000001
    r_1 = length_1 + length_2
    r_2 = length_1 - length_2
    distance = point.magnitude()
    if min([r_1, r_2]) <= distance and distance <= max([r_1, r_2]):
        # If distance is within our valid range
        return True
    else:
        return False
def n_joint_point_validity(L, point):
    '''
    returns True if an N-jointed arm with lengths array L
    can reach point
    '''
    lengths = L[:]
    lengths.sort(reverse=True)
    for i in range(1, len(lengths)):
        large = sum(lengths[:i])
        small = sum(lengths[i:])
        if two_joint_point_validity(large, small, point):
            return True
    return False
def recreate_point(lengths, angles):
    recreated_point = Vector(0.0, 0.0)
    for index in range(len(lengths)):
        # For each index in [0, N-1]

        # Get angle in world space (stored in local space)
        absolute_angle = sum(angles[:index+1])

        # Add the transformed length to the recreated_point
        offset = Vector(lengths[index] * math.cos(absolute_angle),
                        lengths[index] * math.sin(absolute_angle))
        recreated_point = recreated_point.add(offset)
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
    distance = point.magnitude()

    if not two_joint_point_validity(max(length_1, length_2),
                                    min(length_1, length_2), point):
        print("ERROR::Two joint IK not valid::\n" + \
              "\tlength_1, length_2: " + str(length_1) + ", " + str(length_2) + "\n" \
              "\tdistance: " + str(distance))
        sys.exit()
        
    x_neg = point.x < 0.0
    relative_angle = 0.0
    x_1 = 0.0
    
    if not distance == 0:
        relative_angle = math.asin(point.y / distance)
        # Calculate the x value of the intersection points
        x_1 = (distance**2 - length_2**2 + length_1**2) / (2 * distance)
        
    x_2 = distance - x_1
        
        
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

def n_jointed_arm_ik(lengths, weight, point):
    if not n_joint_point_validity(lengths, point):
        print("Attempting to find joint solution where none exists")
        return None
    
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
                minimum_mult = point.magnitude() / (length_1 + length_2)
                minimum_mult = min(minimum_mult, 1.0)
                
                maximum_mult = 1.0
                difference = length_2 - length_1
                if difference > point.magnitude():
                    maximum_mult = point.magnitude() / (length_2 - length_1)
                    maximum_mult = min(maximum_mult, 1.0)
                    
                    mult = minimum_mult + weight * (maximum_mult - minimum_mult)
                    mult = min(mult, 1.0)
                    
            # Run a two jointed arm ik to find the angle for this joint
            a_1, a_2 = two_jointed_arm_ik(length_1 * mult,
                                          length_2 * mult,
                                          point)

        # Store relative angle values
        resulting_angles[index] += a_1
        if index >= 1:
            resulting_angles[index] -= sum(resulting_angles[:index])
            #resulting_angles[index] -= resulting_angles[index-1]
        if index == len(lengths)-2:
            resulting_angles[index+1] = a_2
            
        # Subtract current progress to the point
        absolute_angle = sum(resulting_angles[:index+1])
        offset = Vector(lengths[index] * math.cos(absolute_angle),
                        lengths[index] * math.sin(absolute_angle))
        point = point.subtract(offset)
        point = point.scale(0.999999999)
    
    return resulting_angles