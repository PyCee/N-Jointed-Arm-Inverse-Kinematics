from math import sin, cos, tan, fabs, acos, asin, pi
from vector import Vector, Angle_Vector
from circle import Circle
from arc import Arc, Translate_Arc, Rotate_Arc, Arc_Circle
from cull_arc_bounded_area import cull_arc_bounded_area

def sweep_arc(arc, angle, length):
    result = Translate_Arc(arc, length)
    result = Rotate_Arc(result, angle)
    return result
def flip_arc(arc):
    flipped_limits = [arc.get_limits()[1] * -1.0,
                      arc.get_limits()[0] * -1.0]
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
       fabs(arc.get_limits()[0]) >= fabs(arc.get_limits()[1]):
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
    if base_arc_limits[0] != base_arc_limits[1]:
        if index == 1:
            base_arc_limits = base_arc_limits[::-1]
        base_arc = Arc(arc.get_origin(), swept_arc.get_radius(),
                       base_arc_limits)
    else:
        base_arc = None
    return base_arc, arcs

def get_swept_arc_bounds(arc, length, limits):
    '''
    Sweep an arc and return the upper and lower limits
    '''
    sweep_radians = limits[1] - limits[0]
    
    #Calculate starting_bounds
    starting_bounds = []
    # Calculate subdivision based on 0th limit
    base, arcs = get_swept_arc_subdivisions(arc, 0, length,
                                            sweep_radians)
    starting_bounds += arcs
    if base != None:
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
        
    flipped_arc = flip_arc(arc)
    #Calculate final_bounds
    final_bounds = []
    # Calculate subdivision based on 0th limit
    base, arcs = get_swept_arc_subdivisions(flipped_arc, 0, length,
                                            sweep_radians)
    final_bounds += arcs
    if base != None:
        # Calculate subdivision based on 1st limit
        base, arcs = get_swept_arc_subdivisions(base, 1, length,
                                                sweep_radians)
        final_bounds += arcs
        # Sweep portion of arc that was not subdivided
        base = sweep_arc(base, 0.0, length)
        final_bounds.append(base)
    # Rotate final bounds by limits[1]
    for i in range(len(final_bounds)):
        final_bounds[i] = flip_arc(final_bounds[i])
        final_bounds[i] = Rotate_Arc(final_bounds[i],
                                     limits[1])
        
    return starting_bounds, final_bounds
    
def sweep_area(list_of_arcs, length, limits):
    #Turn into 2 lists of arcs, angled upwards or downwards
    #    (dividing arcs as needed)
    results = []
    total_start_bounds = []
    total_final_bounds = []

    for arc in list_of_arcs:
        start_arcs, final_arcs = get_swept_arc_bounds(arc, length,
                                                      limits)
        total_start_bounds.extend(start_arcs)
        total_final_bounds.extend(final_arcs)
        
    furthest_start_extreme = None
    nearest_start_extreme = None
    for arc in total_start_bounds:
        for extreme in arc.get_extremes():
            mag = extreme.magnitude()
            if furthest_start_extreme == None or \
               mag > furthest_start_extreme.magnitude() or \
               (mag == furthest_start_extreme.magnitude() and 
                furthest_start_extreme.cross_z(extreme) > 0.0):
                furthest_start_extreme = extreme
            if nearest_start_extreme == None or \
               mag < nearest_start_extreme.magnitude() or \
               (mag == nearest_start_extreme.magnitude() and 
                nearest_start_extreme.cross_z(extreme) > 0.0):
                nearest_start_extreme = extreme
    furthest_final_extreme = None
    nearest_final_extreme = None
    for arc in total_final_bounds:
        for extreme in arc.get_extremes():
            mag = extreme.magnitude()
            if furthest_final_extreme == None or \
               mag > furthest_final_extreme.magnitude() or \
               (mag == furthest_final_extreme.magnitude() and 
                furthest_final_extreme.cross_z(extreme) < 0.0):
                furthest_final_extreme = extreme
            if nearest_final_extreme == None or \
               mag < nearest_final_extreme.magnitude() or \
               (mag == nearest_final_extreme.magnitude() and 
                nearest_final_extreme.cross_z(extreme) < 0.0):
                nearest_final_extreme = extreme

    if furthest_start_extreme != furthest_final_extreme:
        outer_arc = Arc(Vector(0.0, 0.0),
                        furthest_start_extreme.magnitude(),
                        (furthest_start_extreme.get_abs_angle(),
                         furthest_final_extreme.get_abs_angle()))
        results.append(outer_arc)
    
    if nearest_start_extreme != nearest_final_extreme:
        inner_arc = Arc(Vector(0.0, 0.0),
                        nearest_start_extreme.magnitude(),
                        (nearest_start_extreme.get_abs_angle(),
                         nearest_final_extreme.get_abs_angle()))
        results.append(inner_arc)

    results += total_start_bounds
    results += total_final_bounds

    results = cull_arc_bounded_area(results)
    
    return results
