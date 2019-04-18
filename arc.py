from math import pi, sin, cos, fabs
from vector import Vector, Angle_Vector
from circle import Circle

class InvalidArcRadiusException (Exception):
    pass
class InvalidArcLimitsException (Exception):
    pass
class InvalidArcRadianException (Exception):
    pass
ARC_RADIAN_RANGE = (-1.0 * pi, pi)

def Arc_Radian(radian):
    while radian <= ARC_RADIAN_RANGE[0]:
        radian += 2.0 * pi
    while radian > ARC_RADIAN_RANGE[1]:
        radian -= 2.0 * pi
    return radian

class Arc:
    def __init__(self, origin, radius, limits):
        '''
        Creates an arc based on a radius and angle range (in radians)
        '''
        if radius <= 0.0:
            raise InvalidArcRadiusException("Radius: " + str(radius))
        self.__origin = origin
        self.__radius = radius
        self.__limits = (Arc_Radian(limits[0]),
                         Arc_Radian(limits[1]))
        if self.__limits[0] == self.__limits[1]:
            raise InvalidArcLimitsException("Limits: " + str(limits))
        
    def __repr__(self):
        output = "Arc(Vector"
        output += str(self.__origin) + ", "
        output += str(round(self.__radius, 6)) + ", ("
        output += str(round(self.__limits[0], 10)) + ", "
        output += str(round(self.__limits[1], 10)) + "))"
        return output
    def __eq__(self, other):
        if other == None:
            return False
        radius_diff = fabs(self.__radius - other.get_radius())
        limit_0_diff = fabs(self.__limits[0] -
                            other.get_limits()[0])
        limit_1_diff = fabs(self.__limits[1] -
                            other.get_limits()[1])
        return (self.__origin == other.get_origin() and
                radius_diff < 0.000001 and
                limit_0_diff < 0.000001 and
                limit_1_diff < 0.000001)
    def get_origin(self):
        return self.__origin
    def get_radius(self):
        return self.__radius
    def get_limits(self):
        return self.__limits
    def get_limit_range(self):
        result = self.__limits[1] - self.__limits[0]
        return result % (2.0 * pi)
        
    def is_valid_angle(self, radians):
        limits_range = self.get_limit_range() * 1.0000001
        moded_radians = (radians - self.__limits[0])
        if fabs(moded_radians) < 0.0000001:
            return True
        return moded_radians % (2.0 * pi) < limits_range
        
    def get_point(self, angle):
        if not self.is_valid_angle(angle):
            raise InvalidArcRadianException
        return self.__origin + Angle_Vector(angle, self.__radius)
    def get_first_point(self):
        return self.get_point(self.__limits[0])
    def get_last_point(self):
        return self.get_point(self.__limits[1])
    def get_extremes(self):
        '''
        Returns a list of angles of which are extremes of this arc 
        based on cosine
        '''
        extremes = []
        # Add endpoints to extremes
        extremes.append(self.get_point(self.__limits[0]))
        extremes.append(self.get_point(self.__limits[1]))
        #Add non-endpoint extremes (radians = 0, radians = pi)
        #  if applicable
        if 0.0 not in self.__limits:
            try:
                extremes.append(self.get_point(0.0))
            except (InvalidArcRadianException):
                pass
        if pi not in self.__limits:
            try:
                extremes.append(self.get_point(pi))
            except (InvalidArcRadianException):
                pass
        return extremes
    
def Translate_Arc(arc, length):
    '''
    Translates an arc and returns the results
    '''
    return Arc(arc.get_origin() + Vector(length, 0.0),
               arc.get_radius(), arc.get_limits())

def Rotate_Arc(arc, radians):
    '''
    Preforms an absolute rotation on an arc and returns the result
    '''
    new_origin = None
    if arc.get_origin().magnitude() != 0.0:
        prev_origin_mag = arc.get_origin().magnitude()
        prev_origin_angle = Vector(0.0, 0.0).get_angle(arc.get_origin())
        new_origin_angle = prev_origin_angle + radians
        new_origin = Angle_Vector(new_origin_angle, prev_origin_mag)
    else:
        new_origin = arc.get_origin()
    new_limits = (arc.get_limits()[0] + radians,
                  arc.get_limits()[1] + radians)
    return Arc(new_origin, arc.get_radius(), new_limits)
def Is_Point_In_Arc(point, arc):
    return arc.is_valid_angle(arc.get_origin().get_angle(point))

def Arc_Circle(arc):
    return Circle(arc.get_origin(), arc.get_radius())

def Arc_Get_Break_Range(arc):
    '''
    Calculates angle difference from origin (0, 0) for each extreme needed 
    to break the other side of the arc (counter-clockwise)
    If there is no angle that will break the arc, the value is 
    None.

    returns in format:
    (angle for 0-nth extreme break, angle for 1-nth extreme break)
    '''
    if arc.get_origin().magnitude() == 0.0:
        return (None, None)
    angles = []
    arc_circle = Arc_Circle(arc)
    for i in range(2):
        limit_point = arc.get_point(arc.get_limits()[i])
        point_mag = limit_point.magnitude()
        base_circle = Circle(Vector(0.0, 0.0), point_mag)
        intersections = base_circle.get_intersections(arc_circle)
        if len(intersections) < 2 or \
           (not Is_Point_In_Arc(intersections[0], arc)) or \
           (not Is_Point_In_Arc(intersections[1], arc)):
            '''
            If there are not 2 intersections or
            one of the intersections is not on the arc
            '''
            angles.append(None)
        else:
            angle1 = Vector(0.0, 0.0).get_angle(intersections[0])
            angle2 = Vector(0.0, 0.0).get_angle(intersections[1])
            angle = fabs(angle1 - angle2)
            if angle <= 0.0:
                angle = None
            angles.append(angle)
    return (angles[0], angles[1])
