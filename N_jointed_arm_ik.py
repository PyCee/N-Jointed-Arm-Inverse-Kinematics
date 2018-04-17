import math

def two_arm_ik(length_1, length_2, point):
    '''
    returns angles for a two arm inverse kinematics solution,
    angle is relative to parent
    
    It works by using data of 2 circles. One centered at (0, 0) with radius
    length_1, and the second centered at (distance, 0) with radius length_2.
    The position of the second joint should be the upper intersection point
    of the circles. It finds the intersection point, and calculates
    the angles for each joint.
    '''
    distance = math.sqrt(point[0]**2 + point[1]**2)
    relative_angle = math.asin(point[1] / distance)

    if distance > length_1 + length_2:
        return None
    # Calculate the x value of the intersection points
    x1 = (length_1 ** 2 - length_2 ** 2 + distance ** 2) / (distance * 2)
    x2 = distance - x1
    # We use the lengths with the x values to calculate the
    #   x value on the unit circle, and use acos to get the angle
    angle_1 = math.acos(x1 / length_1)
    angle_2 = -1.0 * math.acos(x2 / length_2)
    
    angle_1 += relative_angle
    angle_2 += relative_angle - angle_1
    return angle_1, angle_2

def n_jointed_arm_ik(lengths, angles, index, point):
    if index >= len(lengths) - 1:
        print("This should never run")
    
    resulting_angles = [0] * len(lengths)
    '''
    for i in range(index-1):
    pass
    '''
    return resulting_angles


def two_joint_point_validity(l_1, l_2, d):
    '''
    return True if a two jointed arm with arms of lengths l_1 and l_2 could
    potentially reach a point that is distance d away
    '''
    r_1 = l_1 + l_2
    r_2 = l_1 - l_2
    if min([r_1, r_2]) <= d and d <= max([r_1, r_2]):
        # If distance parameter d is within range
        return True
    else:
        return False
def N_joint_point_validity(L, d):
    '''
    returns True if an N-jointed arm with lengths parameter array L
    can reach a point at distance parameter d
    '''
    for binary_tracker in range(2**len(L)):
        lengths = L[:]
        for i in range(len(L)):
            if binary_tracker & (1 << i):
                lengths[i] *= -1
        lengths.sort(reverse=True)
        for i in range(1, len(lengths)-1):
            large = sum(lengths[:i])
            small = sum(lengths[i:])
            if two_joint_point_validity(large, small, d):
                return True
    return False
