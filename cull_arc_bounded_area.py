from math import sin, cos, tan, fabs, acos, asin, pi
from vector import Vector, Angle_Vector
from arc import Arc

class Point_Info:
    def __init__(self, point):
        self.point = point
        self.arcs = []
        self.indices = []
    def __repr__(self):
        output = "Point Info("
        output += "Vector" + str(self.point) + ", "
        output += "" + str(len(self.arcs)) + ")"
        return output
    def get_point(self):
        return self.point
    def add_arc(self, arc, index):
        self.arcs.append(arc)
        self.indices.append(index)
    def get_tangents(self):
        tangents = []
        for i in range(len(self.arcs)):
            tangent = self.arcs[i].get_origin().get_angle(self.point)
            
            if self.indices[i] == 0:
                tangent += (pi/2.0)
            else:
                tangent -= (pi/2.0)
            
            '''
            while tangent > pi:
                tangent -= pi
            while tangent < -1.0 * pi:
                tangent += pi
             '''
            tangents.append(tangent)
        return tangents
    def get_largest_arcs(self):
        '''
        Get difference in arcs depending on the largest 
        difference in tangents

        If 2 tangents are equal, use arc with larger radius
        '''
        results = (None, None)
        if len(self.arcs) == 2:
            results = (self.arcs[0], self.arcs[1])
        elif len(self.arcs) > 2:
            stored_indices = (0, 0)
            stored_difference = 0.0
            stored_radius_sum = 0.0
            tangents = self.get_tangents()
            for i in range(len(tangents) - 1):
                for j in range(i+1, len(tangents)):
                    difference = fabs(tangents[i] - tangents[j])
                    
                    if difference > pi:
                        difference = (2.0*pi) - difference
                    
                    radius_sum = self.arcs[i].get_radius() + \
                                 self.arcs[j].get_radius()
                    if difference > stored_difference or \
                       (difference == stored_difference and \
                        radius_sum > stored_radius_sum):
                        stored_indices = (i, j)
                        stored_difference = difference
                        stored_radius_sum = radius_sum
                        results = (self.arcs[i], self.arcs[j])
        return results

def get_arc_bounded_area_point_info(arcs):
    point_list = []
    point_info_list = []
    for arc in arcs:
        limits = (arc.get_first_point(), arc.get_last_point())
        for i in range(len(limits)):
            if limits[i] not in point_list:
                point_list.append(limits[i])
                point_info_list.append(Point_Info(limits[i]))
            for j in range(len(point_info_list)):
                if limits[i] == point_info_list[j].get_point():
                    point_info_list[j].add_arc(arc, i)
    return point_info_list

def cull_arc_bounded_area(arcs):
    point_info_list = get_arc_bounded_area_point_info(arcs)
    arc_ref_count = [0] * len(arcs)
    for point_info in point_info_list:
        largest_arcs = point_info.get_largest_arcs()
        for i in range(len(arcs)):
            if arcs[i] in largest_arcs:
                arc_ref_count[i] += 1

    leftover_arcs = []
    for i in range(len(arcs)):
        if arc_ref_count[i] == 2:
            leftover_arcs.append(arcs[i])

    leftover_point_info_list = []
    for point_info in point_info_list:
        largest_arcs = point_info.get_largest_arcs()
        if largest_arcs[0] in leftover_arcs and \
           largest_arcs[1] in leftover_arcs:
            leftover_point_info_list.append(point_info)
    
    arc_ref_count = [0] * len(arcs)
    for point_info in leftover_point_info_list:
        largest_arcs = point_info.get_largest_arcs()
        for i in range(len(arcs)):
            if arcs[i] in largest_arcs:
                arc_ref_count[i] += 1
                
    #print(arc_ref_count)
    results = []
    
    for i in range(len(arcs)):
        if arc_ref_count[i] == 2:
            results.append(arcs[i])
    
    return results
