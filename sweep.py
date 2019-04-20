from math import sin, cos, tan, fabs, acos, asin, pi
from vector import Vector, Angle_Vector
from circle import Circle
from arc import Arc, Translate_Arc, Rotate_Arc, Arc_Circle

def sweep_arc(arc, angle, length):
    result = Translate_Arc(arc, length)
    result = Rotate_Arc(result, angle)
    return result
def flip_arc(arc):
    flipped_limits = [arc.get_limits()[0] * -1.0,
                      arc.get_limits()[1] * -1.0]
    return Arc(arc.get_origin(), arc.get_radius(), flipped_limits)
        
def get_swept_arc_subdivisions(arc, index,
                               offset_length, sweep_radians):
    '''
    Breaks arc at bottom of a sweep in-place

    Base is the un-modified part of the arc
    arcs are the modified segments
    '''
    if index < 0 or index > 1:
        raise Exception("invalid index " + str(index))
    arcs = []
    limit_index = (0, 1)[index]

    extreme_radians = None
    possible_extreme_radians = (pi, 0.0, -1.0 * pi)
    filtered_rads = list(filter(lambda r: arc.is_valid_angle(r) and \
                                r > arc.get_limits()[index],
                                possible_extreme_radians))
    if len(filtered_rads) > 0:
        if index == 0:
            extreme_radians = min(filtered_rads)
        else:
            extreme_radians = max(filtered_rads)

    other_limit_radians = (arc.get_limits()[1],
                           arc.get_limits()[0])[index]
    
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

    if limit_radians > 0.0 and \
       fabs(arc.get_limits()[0]) > fabs(arc.get_limits()[1]):
        if index == 0:
            return Arc(arc.get_origin(), arc.get_radius(),
                       (-1.0 * pi, arc.get_limits()[1])), []
        else:
            return Arc(arc.get_origin(), arc.get_radius(),
                       (arc.get_limits()[0], 0.0)), []
    
    if arc.is_valid_angle(-1.0 * limit_radians) and \
       limit_radians not in (0.0, pi, -1.0 * pi):
        #if limit_radians != extreme_radians:
        cover_arc_limits = (limit_radians, extreme_radians)
        if index == 1:
            cover_arc_limits = cover_arc_limits[::-1]
        cover_arc = Arc(swept_arc.get_origin(),
                        swept_arc.get_radius(),
                        cover_arc_limits)
        arcs.append(cover_arc)
        #print(cover_arc_limits)
        # end if limit_radians != extreme_radians
        
        intersection = swept_arc.get_point(-1.0 * limit_radians)
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
    return base_arc, arcs
        
def get_sweeping_arc_bounds(arc, length, limits):
    sweep_radians = limits[1] - limits[0]
    
    #Calculate starting_bounds
    starting_bounds = []
    # Calculate subdivision based on 0th limit
    base, arcs = get_swept_arc_subdivisions(arc, 0, length,
                                            sweep_radians)
    starting_bounds += arcs
    # Calculate subdivision based on 1st limit
    base, arcs = get_swept_arc_subdivisions(base, 1, length,
                                            sweep_radians)
    starting_bounds += arcs
    # Sweep portion of arc that was not subdivided
    base = sweep_arc(base, 0.0, length)
    starting_bounds.append(base)
    # Rotate starting bounds by limits[0]
    for i in range(len(starting_bounds)):
        starting_bounds[i] = Rotate_Arc(starting_bounds[i],
                                        limits[0])

    '''
    # TODO: try flipping the arc, calculating arcs like above, then flipping back, then rotate final_bounds by limits[1]
    flipped_arc = flip_arc(arc)
    #Calculate starting_bounds
    final_bounds = []
    # Calculate subdivision based on 0th limit
    base, arcs = get_swept_arc_subdivisions(flipped_arc, 0, length,
                                            sweep_radians)
    final_bounds += arcs
    # Calculate subdivision based on 1st limit
    base, arcs = get_swept_arc_subdivisions(base, 1, length,
                                            sweep_radians)
    final_bounds += arcs
    # Sweep portion of arc that was not subdivided
    base = sweep_arc(base, 0.0, length)
    final_bounds.append(base)
    # Rotate starting bounds by limits[1]
    for i in range(len(final_bounds)):
        final_bounds[i] = flip_arc(final_bounds[i])
        final_bounds[i] = Rotate_Arc(final_bounds[i],
                                        limits[1])
    '''

    results = []
    results.extend(starting_bounds)
    #results.extend(final_bounds)
    return results
    
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

