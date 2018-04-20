from N_jointed_arm_ik import n_joint_point_validity, n_jointed_arm_ik, two_jointed_arm_ik, recreate_point
import math

POINT = [5, 0]
L = [10, 1]
if n_joint_point_validity(L, math.sqrt(POINT[0]**2 + POINT[1]**2)) == False:
    print("Succeded on the 2 joint validity test")
else:
    print("Failed on the 2 joint validity test")

POINT = [0.5, 0]
L = [2, 6, 5]
if n_joint_point_validity(L, math.sqrt(POINT[0]**2 + POINT[1]**2)):
    print("Succeded on the 3 joint validity test")
else:
    print("Failed on the 3 joint validity test")

POINT = [7, 0]
L = [3, 4]
#A = two_jointed_arm_ik(L[0], L[1], POINT)

POINT = [5.5, 0]
L = [1, 3, 4]
A = n_jointed_arm_ik(L, 0.8, POINT)
for a in A:
    print(a * 180 / 3.14159)
print("recreated point: " + str(recreate_point(L, A)))
