from math import sin, cos, tan, fabs, acos
from vector import Vector

class InvalidArcRadius (Exception):
    pass
class Arc:
    def __init__(self, origin, radius, limits):
        '''
        Creates an arc based on a radius and angle range (in radians)

        limits[0] < limits[1]
        '''
        if radius <= 0.0:
            raise InvalidArcRadius("Invalid Radius '" + str(radius) + "'")
        #TODO: check limits for valididty
        self.__origin = origin
        self.__radius = radius
        self.__limits = limits
        
    def __repr__(self):
        output = "Arc:\n"
        output += "origin: " + str(self.__origin) + "\n"
        output += "radians: " + str(self.__radius) + "\n"
        output += "limits: (" + str(round(self.__limits[0], 3)) + " - "
        output += str(round(self.__limits[1], 3)) + ")\n"
        output += "Extremes: " + str(self.get_point(0.0)) + " - "
        output += str(self.get_point(1.0))
        return output
    def __eq__(self, other):
        return other != None and \
                        (self.__origin == other.get_origin() and
                         self.__radius == other.get_radius() and
                         self.__limits[0] == other.get_limits()[0] and
                         self.__limits[1] == other.get_limits()[1])
    def get_origin(self):
        return self.__origin
    def get_radius(self):
        return self.__radius
    def get_limits(self):
        return self.__limits
    def get_limit_range(self):
        return self.__limits[1] - self.__limits[0]
    def get_point_at_angle(self, angle):
        return self.__origin + Vector(cos(angle),
                                      sin(angle)).scale(self.__radius)
    def get_point(self, place):
        if place < 0.0 or place > 1.0:
            raise Exception
        angle = self.__limits[0] + place * self.get_limit_range()
        return self.get_point_at_angle(angle)
    
    def get_furthest_point(self):
        angle = None
        if self.__limits[0] < 0.0 and self.__limits[1] > 0.0:
            angle = 0.0
        elif cos(self.__limits[0]) > cos(self.__limits[1]):
            angle = self.__limits[0]
        else:
            angle = self.__limits[1]
        return self.get_point_at_angle(angle)
    def get_closest_point(self):
        angle = None
        if cos(self.__limits[0]) < cos(self.__limits[1]):
            angle = self.__limits[0]
        else:
            angle = self.__limits[1]
        return self.get_point_at_angle(angle)
        
    def get_transformed_arc(self, angle, length):
        lower_limit = self.__limits[0] + angle
        upper_limit = self.__limits[1] + angle
        offset = Vector(cos(angle), sin(angle)).scale(length)
        new_origin = self.__origin + offset
        return Arc(new_origin, self.__radius, (lower_limit, upper_limit))
    
class DualArcBoundedArea:
    def __init__(self, length1, length2, limits1, limits2):
        sweep_range = limits2[1] - limits2[0]
        first_arc = Arc(Vector(0.0, 0.0), length1, limits1)

        moded_arc1 = first_arc.get_transformed_arc(limits2[0], length2)
        moded_arc2 = first_arc.get_transformed_arc(limits2[1], length2)
        
        inner_point = moded_arc1.get_closest_point()
        inner_bound = inner_point.magnitude()
        inner_angle = acos(inner_point.dot(Vector(1.0, 0.0)) / inner_bound)
        inner_arc = Arc(Vector(0.0, 0.0), inner_bound,
                        (inner_angle, inner_angle + sweep_range))

        outer_point = moded_arc1.get_furthest_point()
        outer_bound = outer_point.magnitude()
        outer_angle = acos(outer_point.dot(Vector(1.0, 0.0)) / outer_bound)
        outer_arc = Arc(Vector(0.0, 0.0), outer_bound,
                        (outer_angle, outer_angle + sweep_range))
        arcs = [moded_arc1,
                moded_arc2,
                inner_arc,
                outer_arc] 
def sweep(list_of_arcs, length, limits):
    pass
    #Find center line of area bounded by arcs (based on tangent to the arc
    #Turn into 2 lists of arcs (dividing arcs as needed)

    #Transform right half by length and limits[0]
    #Transform left half by length and limits[1]

    #Find furthest point of all arcs in right half
    #Extend arc to meet right half
    
    #Find closest point of all arcs in right half
    #Extend arc to meet right half

    #Find inflection points in right half
    #Extend left until they meet another right-arc and divide/remove the arc that was met so there is no arc in bounded area
    
    #Find inflection points in left half
    #Extend right until they meet another right-arc and divide/remove the arc that was met so there is no arc in bounded area

    
    
