from vector import Vector, Angle_Vector
from math import fabs, acos, sin, cos

class InvalidCircleRadiusException (Exception):
    pass

class Circle:
    def __init__(self, origin, radius):
        if radius < 0.0:
            raise InvalidCircleRadiusException("Radius: " + str(radius))
        self.__origin = origin
        self.__radius = radius
    def __repr__(self):
        output = "(origin: " + str(self.__origin) + "\n"
        output += "radius: " + str(self.__radius) + ")"
        return output
    def get_origin(self):
        return self.__origin
    def get_radius(self):
        return self.__radius
    def get_intersections(self, other):
        intersections = []
        difference = other.get_origin() - self.__origin
        distance = fabs(difference.magnitude())
        outer_reach = other.get_radius() + self.__radius
        inner_reach = fabs(self.__radius - other.get_radius())

        # Adjust for floating-point error
        outer_reach *= 1.000000001
        inner_reach *= 0.99999999

        if self.__radius == 0.0 and distance == other.get_radius():
            intersections.append(self.__origin)
        elif other.get_radius() == 0.0 and distance == self.__radius:
            intersections.append(other.get_origin())
        elif distance == 0.0 and inner_reach == 0.0:
            intersections.append(Vector(self.__radius, 0.0))
        elif distance <= outer_reach and distance >= inner_reach:
            dist_sq = distance ** 2
            other_radius_sq = other.get_radius() ** 2
            self_radius_sq = self.__radius ** 2
            x_value = (dist_sq-other_radius_sq+self_radius_sq) / (2*distance)
            normalized_x_value = x_value / self.__radius
            # Adjust due to error caused by floating-point
            normalized_x_value = min(1.0, max(-1.0, normalized_x_value))
            flat_angle = acos(normalized_x_value)
            angle_offset = self.__origin.get_angle(other.get_origin())
            angle = flat_angle + angle_offset
            intersection = Angle_Vector(angle, self.__radius)
            intersection += self.__origin
            intersections.append(intersection)

            second_angle = -1.0 * flat_angle + angle_offset
            second_intersection = Angle_Vector(second_angle,
                                               self.__radius)
            second_intersection += self.__origin
            if not second_intersection == intersection:
                intersections.append(second_intersection)
        return intersections
