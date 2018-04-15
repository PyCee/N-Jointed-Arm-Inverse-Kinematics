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
        print("Attempting to get angles when arm cannot reach")
        return 0, 0
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
    pass
    
POINT = [4, 0]
L = [4, 1]
A = [0] * len(L)
A = two_arm_ik(L[0], L[1], POINT)

print("Output: ")
for a in A:
    print(a * 180 / 3.14159)
