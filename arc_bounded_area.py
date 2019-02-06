from math import sin, cos, tan, fabs, acos, asin
from vector import Vector

class InvalidArcRadiusException (Exception):
    pass
class InvalidArcLimitsException (Exception):
    pass
class Arc:
    def __init__(self, origin, radius, limits):
        '''
        Creates an arc based on a radius and angle range (in radians)

        limits[0] < limits[1]
        '''
        if radius <= 0.0:
            raise InvalidArcRadiusException("Radius: " + str(radius))
        if limits[0] >= limits[1]:
            raise InvalidArcLimitsException("Limits: " + str(limits))
            
        #TODO: check limits for valididty
        self.__origin = origin
        self.__radius = radius
        self.__limits = limits
        
    def __repr__(self):
        output = "Arc:\n"
        output += "origin: " + str(self.__origin) + "\n"
        output += "radius: " + str(round(self.__radius, 3)) + "\n"
        output += "limits: (" + str(round(self.__limits[0], 3)) + " - "
        output += str(round(self.__limits[1], 3)) + ")\n"
        output += "Extremes: " + str(self.get_point_by_progress(0.0)) + " - "
        output += str(self.get_point_by_progress(1.0))
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
    def get_point(self, angle):
        if angle > self.__limits[1] or angle < self.__limits[0]:
            raise Exception
        return self.__origin + Vector(cos(angle),
                                      sin(angle)).scale(self.__radius)
    def get_point_by_progress(self, place):
        if place < 0.0 or place > 1.0:
            raise Exception
        angle = self.__limits[0] + place * self.get_limit_range()
        return self.get_point(angle)
    
    def get_furthest_point(self):
        angle = None
        if self.__limits[0] < 0.0 and self.__limits[1] > 0.0:
            angle = 0.0
        elif cos(self.__limits[0]) > cos(self.__limits[1]):
            angle = self.__limits[0]
        else:
            angle = self.__limits[1]
        return self.get_point(angle)
    def get_closest_point(self):
        angle = None
        if cos(self.__limits[0]) < cos(self.__limits[1]):
            angle = self.__limits[0]
        else:
            angle = self.__limits[1]
        return self.get_point(angle)
    def get_extremes(self):
        '''
        Returns a list of angles of which are extremes of this arc 
        based on cosine
        '''
        extremes = []
        # Add endpoints to extremes
        extremes.append(self.get_point(self.__limits[0]))
        extremes.append(self.get_point(self.__limits[1]))
        #Add non-endpoint extremes (radians = 0, radians = pi) if applicable
        if self.__limits[0] < 0.0 and self.__limits[1] > 0.0:
            extremes.append(self.get_point(0.0))
        if self.__limits[0] < 3.14159 and self.__limits[1] > 3.14159:
            extremes.append(self.get_point(3.14159))
        return extremes
    def get_intersections(self, other_arc):
        '''
        Get angles of self that relate to intersections with other_arc
        '''
        intersection_radians = []

        # Intersection of 2 circles
        # Get radians relative to self

        return intersection_radians
    
    def get_intersection_points(self, x):
        '''
        Get any points on arc that have a specific x value
        '''
        points = []
        
        x_difference = x - self.get_origin().x
        desired_sin = x_difference / self.get_radius()
        try:
            angle = asin(desired_sin)
            #get angles (+-) that match angle and are within limits
            #set points
        except (ValueError):
            pass
        
        return points
        
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
        if inner_point.cross_z(Vector(1.0, 0.0)) > 0.0:
            inner_angle *= -1
        inner_arc = Arc(Vector(0.0, 0.0), inner_bound,
                        (inner_angle, inner_angle + sweep_range))

        outer_point = moded_arc1.get_furthest_point()
        outer_bound = outer_point.magnitude()
        outer_angle = acos(outer_point.dot(Vector(1.0, 0.0)) / outer_bound)
        if outer_point.cross_z(Vector(1.0, 0.0)) > 0.0:
            outer_angle *= -1
        outer_arc = Arc(Vector(0.0, 0.0), outer_bound,
                        (outer_angle, outer_angle + sweep_range))
        self.arcs = [moded_arc1,
                     moded_arc2,
                     inner_arc,
                     outer_arc]
def sweep(list_of_arcs, length, limits):
    #Turn into 2 lists of arcs, angled upwards or downwards
    #    (dividing arcs as needed)
    right_arcs = []
    left_arcs = []

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


