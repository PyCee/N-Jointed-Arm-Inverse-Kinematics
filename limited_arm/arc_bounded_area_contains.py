from math import fabs, acos, sin
from vector import Vector, Angle_Vector
from arc import Arc

def get_x_intercepts(arc, x):
    '''
    Takes an arc and an x value
    
    returns the points where the arc intercept the x in the form of
    (Vector, Vector) with the first of the 2 vectors being the lower y
    '''
    x_difference = x - arc.get_origin().x
    if fabs(x_difference) > arc.get_radius():
        return (None, None)
    positive_angle = acos(x_difference / arc.get_radius())
    lower_y = None
    upper_y = None
    if arc.is_valid_angle(-1.0 * positive_angle):
        lower_y = arc.get_point(-1.0 * positive_angle).y
    if arc.is_valid_angle(positive_angle) and sin(positive_angle) > 0.000001:
        upper_y = arc.get_point(positive_angle).y
    return (lower_y, upper_y)

def arc_bounded_area_contains_point(arcs, point, __error=0):
    '''
    Takes an arc bounded area and a point
    Returns True if the point in enclosed in the arc bounded area

    __error is used for a recursive call to this function, with a purpose to fix
    a problem caused by floating point errors where there would be an odd number of 
    intercepts when placed on the same x as the extremes of two arcs
    '''
    intercepts = []
    for arc in arcs:
        individual_intercepts = get_x_intercepts(arc, point.x)
        for individual_inter in individual_intercepts:
            if individual_inter is not None:
                intercepts.append(individual_inter)

    if not len(intercepts) % 2 == 0:
        if not __error:
            return arc_bounded_area_contains_point(arcs, point + Vector(0.0001, 0.0),
                                                   __error=True)
        print("length of intercepts % 2 != 0")
        print(intercepts)
        return None
    below_counter = 0
    for intercept in intercepts:
        if point.y < intercept:
            below_counter += 1
    return below_counter % 2 == 1
