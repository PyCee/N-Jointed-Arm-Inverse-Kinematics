from math import sin, cos, tan, fabs, acos, asin
from vector import Vector, Angle_Vector
from circle import Circle
from arc import Arc, Translate_Arc, Rotate_Arc, Arc_Circle

def sweep_arc(arc, angle, length):
    result = Translate_Arc(arc, length)
    result = Rotate_Arc(result, angle)
    return result
        
def subdivide_swept_arc(arc, index, offset_length, sweep_radians):
    '''
    Breaks arc at bottom of a sweep in-place

    Base is the un-modified part of the arc
    arcs are the modified segments
    '''
    if index < 0 or index > 1:
        raise Exception("invalid index " + str(index))
    arcs = []
    limit_index = (0, 1)[index]
    extreme_radians = (0.0, 3.14159)[index]
    other_limit_radians = (arc.get_limits()[1], arc.get_limits()[0])[index]
    
    swept_arc = Translate_Arc(arc, offset_length)
    swept_arc_circle = Arc_Circle(swept_arc)
    
    limit_radians = swept_arc.get_limits()[limit_index]
    limit_point = swept_arc.get_point(limit_radians)
    abs_limit_radians = Vector(0.0, 0.0).get_angle(limit_point)

    
    base_circle = Circle(Vector(0.0, 0.0),
                         limit_point.magnitude())
    base_arc_start_radians = arc.get_limits()[limit_index]
    intersections = base_circle.get_intersections(swept_arc_circle)
    intersection = None
    swept_origin = swept_arc.get_origin()
    if len(intersections) == 2 and \
       swept_arc.is_valid_angle(swept_origin.get_angle(intersections[0])) and \
       swept_arc.is_valid_angle(swept_origin.get_angle(intersections[1])):
        # If there both intersections are in the swept arc
        
        if limit_radians != extreme_radians:
            cover_arc_limits = (limit_radians, extreme_radians)
            if index == 1:
                cover_arc_limits = cover_arc_limits[::-1]
            cover_arc = Arc(swept_arc.get_origin(),
                            swept_arc.get_radius(),
                            cover_arc_limits)
            arcs.append(cover_arc)
        if intersections[0] == limit_point:
            intersection = intersections[1]
        else:
            intersection = intersections[0]
            
        abs_intersection_radians = Vector(0.0, 0.0).get_angle(intersection)
        if (sweep_radians + 0.000001) >= fabs(abs_intersection_radians - abs_limit_radians):
            # Start break code
            break_arc_limits = (abs_limit_radians,
                                abs_intersection_radians)
            break_arc = Arc(Vector(0.0, 0.0),
                            limit_point.magnitude(),
                            break_arc_limits)
            arcs.append(break_arc)
        else:
            # Start no-break code
            floating_arc_limits = (abs_limit_radians,
                                   abs_limit_radians +
                                   sweep_radians)
            floating_arc = Arc(Vector(0.0, 0.0),
                               limit_point.magnitude(),
                               floating_arc_limits)
            arcs.append(floating_arc)
            
            offset_arc = Rotate_Arc(swept_arc, sweep_radians)
            offset_circle = Arc_Circle(offset_arc)
            intersections = offset_circle.get_intersections(swept_arc_circle)
            intersection = None
            if index == 0:
                if (intersections[0].magnitude() >
                    intersections[1].magnitude()):
                    intersection = intersections[0]
                else:
                    intersection = intersections[1]
            else:
                if (intersections[0].magnitude() >
                    intersections[1].magnitude()):
                    intersection = intersections[1]
                else:
                    intersection = intersections[0]

            offset_point = offset_arc.get_origin()
            offset_i_radians = offset_point.get_angle(intersection)
            
            floating_point = floating_arc.get_last_point()
            offset_fp_radians = offset_point.get_angle(floating_point)
            intersection_arc_limits = [offset_fp_radians,
                                       offset_i_radians]
            if index == 1:
                intersection_arc_limits = intersection_arc_limits[::-1]
            intersection_arc = Arc(offset_point,
                                   offset_circle.get_radius(),
                                   intersection_arc_limits)
            arcs.append(intersection_arc)
        
    if intersection != None:
        base_arc_start_radians = swept_arc.get_origin().get_angle(intersection)
    base_arc_limits = [base_arc_start_radians, other_limit_radians]
    if index == 1:
        base_arc_limits = base_arc_limits[::-1]
    base_arc = Arc(arc.get_origin(), swept_arc.get_radius(),
                   base_arc_limits)
    
    for i in range(len(arcs)):
        arcs[i] = Rotate_Arc(arcs[i], sweep_radians)
        
    return base_arc, arcs
        
def get_swept_arcs(arc, length, limits):
    extremes = (0.0, 3.14159)
    arcs = []
    sweep_radians = limits[1] - limits[0]
    
    bottom_arcs = []
    #Calculate lower_limit
    if arc.get_limits()[0] < extremes[0]:
        # If arc is broken
        arc, broken_arcs = arc.subdivide_swept_arc(0, length,
                                                   sweep_radians)
        bottom_arcs.extend(broken_arcs)
    if arc.get_limits()[1] > extremes[1]:
        # If arc is broken
        arc, broken_arcs = arc.subdivide_swept_arc(1, length,
                                                   sweep_radians)
        bottom_arcs.extend(broken_arcs)
    bottom_arcs.append(arc)
    for index in range(len(bottom_arcs)):
        bottom_arcs[index] = bottom_arcs[index].sweep(limits[0], length)
        
    # TMP comment out for clear testing of below code
    arcs.extend(bottom_arcs)
    
    # TODO: try flipping the arc, calculating arcs like above, then flipping back
    top_arcs = []
    second_arc = arc.sweep(limits[1], length)
    #arcs.append(second_arc)
    
    arcs.extend(top_arcs)
    return arcs
    
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

