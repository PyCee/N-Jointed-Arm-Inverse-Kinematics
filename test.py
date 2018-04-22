from N_jointed_arm_ik import n_joint_point_validity, n_jointed_arm_ik, two_jointed_arm_ik, recreate_point, Vector
import math
import sys

print("2 Joint Validity Test:")
POINT = Vector(5.0, 0)
L = [10, 1]
if n_joint_point_validity(L, POINT) == False:
    print("Success")
else:
    print("Failure")
    sys.exit()

print("N Joint Validity Test:")
POINT = Vector(0.5, 0)
L = [2, 6, 5]
if n_joint_point_validity(L, POINT):
    print("Success")
else:
    print("Failure")
    sys.exit()

print("2 Jointed Arm IK Solution #1:")
POINT = Vector(7, 0)
L = [3, 4]
A = two_jointed_arm_ik(L[0], L[1], POINT)
if POINT.equals(recreate_point(L, A)):
    print("Success")
else:
    print("Failure")
    print(str(recreate_point(L, A)))
    sys.exit()

print("2 Jointed Arm IK Solution #2:")
POINT = Vector(0, 6.5)
L = [1, 7]
A = two_jointed_arm_ik(L[0], L[1], POINT)
if POINT.equals(recreate_point(L, A)):
    print("Success")
else:
    print("Failure")
    print(str(recreate_point(L, A)))
    sys.exit()

print("2 Jointed Arm IK Solution #3:")
POINT = Vector(-6.5, 0)
L = [1, 7]
A = two_jointed_arm_ik(L[0], L[1], POINT)
if POINT.equals(recreate_point(L, A)):
    print("Success")
else:
    print("Failure")
    print(str(recreate_point(L, A)))
    sys.exit()
    
print("2 Jointed Arm IK Solution #4:")
POINT = Vector(0, -3)
L = [2, 2]
A = two_jointed_arm_ik(L[0], L[1], POINT)
if POINT.equals(recreate_point(L, A)):
    print("Success")
else:
    print("Failure")
    print(str(recreate_point(L, A)))
    sys.exit()

print("N Jointed Arm Solution #1:")
POINT = Vector(5.5, 0.0)
L = [1, 3, 4]
A = n_jointed_arm_ik(L, 0.5, POINT)
if POINT.equals(recreate_point(L, A)):
    print("Success")
else:
    print("Failure")
    sys.exit()

print("N Jointed Arm Solution #2:")
POINT = Vector(6.0, 0)
L = [1, 1, 1, 1, 1, 4, 3, 1, 1]
A = n_jointed_arm_ik(L, 0.5, POINT)
if POINT.equals(recreate_point(L, A)):
    print("Success")
else:
    print("Failure")
    print(str(recreate_point(L, A)))
    sys.exit()

print("N Jointed Arm Solution #3:")
POINT = Vector(6.0, 0)
L = [1, 1, 1, 1, 1, 4, 3, 1, 1, 1, 1, 1]
A = n_jointed_arm_ik(L, 0.5, POINT)
if POINT.equals(recreate_point(L, A)):
    print("Success")
else:
    print("Failure")
    print(str(recreate_point(L, A)))
    sys.exit()

print("N Jointed Arm Solution #4:")
POINT = Vector(6.0, 0)
L = [1, 1, 1, 1, 1, 1, 0.1, 0.01, 0.1, 2, 3, 4]
A = n_jointed_arm_ik(L, 0.0, POINT)
if POINT.equals(recreate_point(L, A)):
    print("Success")
else:
    print("Failure")
    print(str(recreate_point(L, A)))
    sys.exit()

print("N Jointed Arm Solution #5:")
POINT = Vector(4.0, 0)
L = [1, 2, 3, 4, 2, 2]
A = n_jointed_arm_ik(L, 1.0, POINT)
if POINT.equals(recreate_point(L, A)):
    print("Success")
else:
    print("Failure")
    print(str(recreate_point(L, A)))
    sys.exit()

print("N Jointed Arm Solution #6:")
POINT = Vector(0.1, 0)
L = [1, 1, 1]
A = n_jointed_arm_ik(L, 1.0, POINT)
if POINT.equals(recreate_point(L, A)):
    print("Success")
else:
    print("Failure")
    print(str(recreate_point(L, A)))
    sys.exit()
