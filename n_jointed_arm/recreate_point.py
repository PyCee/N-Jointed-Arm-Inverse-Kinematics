import math
from vector import Vector

def recreate_point(lengths, angles):
    recreated_point = Vector(0.0, 0.0)
    for index in range(len(lengths)):
        # For each index in [0, N-1]

        # Get angle in world space (stored in local space)
        absolute_angle = sum(angles[:index+1])

        # Add the transformed length to the recreated_point
        offset = Vector(lengths[index] * math.cos(absolute_angle),
                        lengths[index] * math.sin(absolute_angle))
        recreated_point = recreated_point + offset
    return recreated_point
