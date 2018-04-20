import math

def magnitude(point):
    return math.sqrt(point[0]**2 + point[1]**2)

def two_joint_point_validity(l_1, l_2, d):
    '''
    return True if a two jointed arm with arms of lengths l_1 and l_2 could
    potentially reach a point at distance d

    l_1 is expected to be a lengths made up of larger individual components
    '''
    r_1 = l_1 + l_2
    r_2 = l_1 - l_2
    if min([r_1, r_2]) <= d and d <= max([r_1, r_2]):
        # If distance parameter d is within range
        return True
    else:
        return False
def n_joint_point_validity(L, d):
    '''
    returns True if an N-jointed arm with lengths array L
    can reach a point at distance d
    '''
    lengths = L[:]
    lengths.sort(reverse=True)
    for i in range(1, len(lengths)-1):
        large = sum(lengths[:i])
        small = sum(lengths[i:])
        if two_joint_point_validity(large, small, d):
            return True
    return False

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
    distance = magnitude(point) - 0.0000000000000005
    relative_angle = math.asin(point[1] / distance)

    if distance > length_1 + length_2:
        print("distance (" + str(distance) + ") < length_1 (" + str(length_1) + \
              ") + length_2 (" + str(length_2) + ")")
        return None
    # Calculate the x value of the intersection points
    x1 = (length_1 ** 2 - length_2 ** 2 + distance ** 2) / (distance * 2)
    x2 = distance - x1
    # We use the lengths with the x values to calculate the
    #   x value on the unit circle, and use acos to get the angle
    base_1 = x1 / length_1
    base_2 = x2 / length_2
    if base_1 < -1.0:
        base_1 = -base_1 - 2.0
        base_2 = -base_2 + 2.0
    angle_1 = math.acos(base_1)
    angle_2 = -1.0 * math.acos(base_2)
    
    angle_1 += relative_angle
    angle_2 += relative_angle - angle_1
    return angle_1, angle_2

def n_jointed_arm_ik(lengths, weight, point):
    if not n_joint_point_validity(lengths, magnitude(point)):
        print("Attempting to find joint solution where none exists")
        return None
    resulting_angles = [0] * len(lengths)
    for index in range(len(lengths)-1):

        # calculate multiplier based on weight
        mult = 1.0
        if index < len(lengths)-2:
            hi = magnitude(point) / sum(lengths[index:])
            lo = (magnitude(point) + lengths[index]) / sum(lengths[index+1:])
            mult = lo + weight * (hi - lo)
        
        a_1, a_2 = two_jointed_arm_ik(lengths[index] * mult,
                                      sum(lengths[index+1:]) * mult,
                                      point)
        
        # store angle values
        resulting_angles[index] += a_1
        if index >= 1:
            resulting_angles[index] -= resulting_angles[index-1]
        if index == len(lengths)-2:
            resulting_angles[index+1] = a_2
            
            
        # Subtract current progress to the point
        absolute_angle = sum(resulting_angles[:index+1])
        point[0] -= lengths[index] * math.cos(absolute_angle)
        point[1] -= lengths[index] * math.sin(absolute_angle)
    
    return resulting_angles

def recreate_point(lengths, angles):
    recreated_point = [0, 0]
    for index in range(len(lengths)):
        # For each index in [0, N-1]

        # Get angle in world space (stored in local space)
        absolute_angle = sum(angles[:index+1])

        # Add the transformed length to the recreated_point
        recreated_point[0] += lengths[index] * math.cos(absolute_angle)
        recreated_point[1] += lengths[index] * math.sin(absolute_angle)
    return recreated_point
