import math

# TODO: read input from terminal, and plug into function

''''if N_joint_point_validity(L, math.sqrt(POINT[0]**2 + POINT[1]**2)):
    print("POINT can be reached")

    A = two_arm_ik(L[0], L[1], POINT)
    if A == None:
        print("Could not find ik solution, strange because we already tested for one")
    else:
        print("Output: ")
        recreated_point = [0, 0]
        for index in range(len(L)):
            print(A[index] * 180 / 3.14159)
            absolute_angle = sum(A[:index+1])
            recreated_point[0] += L[index] * math.cos(absolute_angle)
            recreated_point[1] += L[index] * math.sin(absolute_angle)
            print("For error checking, these angles+lengths recreated: " + \
                  str(recreated_point))

else:
    print("POINT could not be reached")
'''
