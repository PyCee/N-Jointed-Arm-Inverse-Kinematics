import math
import sys
from vector import Vector, Angle_Vector
from circle import Circle
from recreate_point import recreate_point
from arc_bounded_area_contains import arc_bounded_area_contains_point
from n_jointed_arm_ik import OutOfRangeException, LengthException, LengthsWeightsNotMatchException
from two_jointed_arm_ik import two_jointed_arm_ik
from sweep import sweep_area, sweep_arc
from arc import Arc, Arc_Circle, Is_Point_In_Arc, Arc_Radian

class LimitsException (Exception):
    pass

def limited_n_jointed_arm_range(lengths, lower_limits, upper_limits):
    '''
    Defines a set of curves that makes an area
    '''
    if len(lengths) < 2:
        pass
    if len(lengths) != len(lower_limits) or \
       len(lengths) != len(upper_limits):
        raise LimitsException
    arcs = [Arc(Vector(0.0, 0.0), lengths[0],
                (lower_limits[0], upper_limits[0]))]
    for i in range(1, len(lengths)):
        arcs = sweep_area(arcs, lengths[i],
                          (lower_limits[i], upper_limits[i]))
    return arcs

def limited_n_jointed_arm_validity(lengths, lower_limits, upper_limits,
                                   point):
    '''
    Checks if the point is in the area defined by n_jointed_arm_validity
    (Think perfect 3d model algorithm in 2d)
    '''
    arcs = limited_n_jointed_arm_range(lengths, lower_limits, upper_limits)
    return arc_bounded_area_contains_point(arcs, point)


'''
def overlapping_arc_with_bounded_area_range(overlap_arc, arc_bounded_area):
    total_intersections = []
    for arc in arc_bounded_area:
        intersections = overlap_arc.get_arc_intersections(arc)
        if len(intersections) > 0:
            total_intersections.extend(intersections)

    results = None
    if len(total_intersections) == 0:
        #Determine if the arc is completely inside or outside the area
        if arc_bounded_area_contains_point(arc_bounded_area,
                                           overlap_arc.get_first_point()):
            #If a point on the arc is inside the area
            # The entire arc range is inside the area
            results = overlap_arc.get_limits()
        else:
            results = None
    elif len(total_intersections) == 1:
        intersection_radians = overlap_arc.get_origin().get_angle(total_intersections[0])
        #Determine which extreme is inside the arc
        if arc_bounded_area_contains_point(arc_bounded_area,
                                           overlap_arc.get_first_point()):
            results = (overlap_arc.get_limits()[0], intersection_radians)
        elif arc_bounded_area_contains_point(arc_bounded_area,
                                             overlap_arc.get_last_point()):
            results = (intersection_radians, overlap_arc.get_limits()[1])
    elif len(total_intersections) == 2:
        intersection_radians_1 = overlap_arc.get_origin().get_angle(total_intersections[0])
        intersection_radians_2 = overlap_arc.get_origin().get_angle(total_intersections[1])
        #TODO test for wrong order when 2 intersections
        results = (intersection_radians_2, intersection_radians_1)
        #TODO handle case for an arc where both limits are inside the area, and go the long way around (leaving and entering the area)
    else:
        #No other valid cases
        raise Exception("Invalid number of intersections")
    return results
'''
def valid_joint_range(point, length, limits, arc_bounded_area):
    '''
    returns a tuple, where 
      index 0 is the minimum angle in radians required to 
        achieve the point with the specified limits.
      index 1 is the maximum
    '''
    point_arc = Arc(Vector(0.0, 0.0), point.magnitude(),
                    (-math.pi + 0.0001, math.pi))
    
    transformed_area = [sweep_arc(arc, limits[0], length)
                        for arc in arc_bounded_area]

    intersections = []
    for arc in transformed_area:
        arc_intersections = point_arc.get_arc_intersections(arc)
        if len(arc_intersections) > 0:
            intersections.extend(arc_intersections)

    assert(len(intersections) == 2)
    point_rad = Vector(0.0, 0.0).get_angle(point)
    intersection_rads = [Vector(0.0, 0.0).get_angle(inter)
                         for inter in intersections]
    rads_to_point = [point_rad - rad for rad in intersection_rads]
    rads_to_point.sort()

    limits_range = limits[1] - limits[0]
    if rads_to_point[1] > limits_range:
        rads_to_point[1] = limits_range
    
    return rads_to_point
    
def limited_n_jointed_arm_ik(lengths, lower_limits, upper_limits,
                             weights, point):
    '''
    Calculates ik angles for joints with angle limits
    lower and upper limits are in radians
    '''
    
    if not limited_n_jointed_arm_validity(lengths, lower_limits,
                                          upper_limits, point):
        raise OutOfRangeException
    
    if len(lengths)-2 != len(weights):
        print("lengths: " + str(lengths))
        print("weights: " + str(weights))
        raise LengthsWeightsNotMatchException
    
    resulting_angles = [0] * len(lengths)
    for index in range(len(lengths)-1):
        length_1 = lengths[index]
        length_2 = sum(lengths[index+1:])
        a_1 = 0.0
        a_2 = 0.0
        if index < len(lengths)-2:
            
            bounded_area = limited_n_jointed_arm_range(lengths[index+1:],
                                                       lower_limits[index+1:],
                                                       upper_limits[index+1:])
            arc = Arc(point, length_1,
                      (lower_limits[index], upper_limits[index]))
            angle_tuple = valid_joint_range(point, length_1, (lower_limits[index], upper_limits[index]), bounded_area)
            #end tmp
            #FIX above TODO angle of first joint needs to be 0.99400 with weight of 0
            # this is currently obtained with a weight of 0.488605
            print("\nangle tuple: " + str(angle_tuple))
            angle_range = angle_tuple[1] - angle_tuple[0]
            #TODO work with cases where [0] > [1]
            
            weighted_range = weights[index] * angle_range
            weighted_angle = angle_tuple[0] + weighted_range
            print("weighted_angle: " + str(weighted_angle))
            angles = (weighted_angle, None)
        else:
            # Run a two jointed arm ik to find the angle for this joint
            print("two joint stuff")
            print("point: " + str(point))
            print("lengths: " + str((length_1, length_2)))
            angles = two_jointed_arm_ik(length_1, length_2, point)
            if angles == None:
                return None
            angles = (Arc_Radian(angles[0]), Arc_Radian(angles[1]))
            
            if angles[0] < lower_limits[index] or \
               angles[0] > upper_limits[index]:
                # If the angle doesnt fit our limits,
                #   use the other two joint solution
                angles = (-angles[0], -angles[1])
            
        a_1, a_2 = angles
        # Store relative angle values
        resulting_angles[index] = a_1
        resulting_angles[index] -= sum(resulting_angles[:index])
        if index == len(lengths)-2:
            resulting_angles[index+1] = a_2
            
        # Subtract current progress to the point
        absolute_angle = sum(resulting_angles[:index+1])
        offset = Vector(lengths[index] * math.cos(absolute_angle),
                        lengths[index] * math.sin(absolute_angle))
        point = point - offset
    return resulting_angles
