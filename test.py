from N_jointed_arm_ik import N_joint_point_validity
import math

POINT = [5, 0]
L = [10, 1]
if N_joint_point_validity(L, math.fabs(POINT[0]**2 + POINT[1]**2)) == False:
    print("Succeded on the 2 joint validity test")
else:
    print("Failed on the 2 joint validity test")

POINT = [0.5, 0]
L = [2, 6, 5]
if N_joint_point_validity(L, math.fabs(POINT[0]**2 + POINT[1]**2)):
    print("Succeded on the 3 joint validity test")
else:
    print("Failed on the 3 joint validity test")
