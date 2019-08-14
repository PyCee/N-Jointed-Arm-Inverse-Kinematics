from math import sin, cos, tan, fabs, acos, asin, pi
from vector import Vector, Angle_Vector
from arc import Arc, Arc_Radian

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
            
            '''
            if self.indices[i] == 0:
                tangent += (pi/2.0)
            else:
                tangent -= (pi/2.0)
            '''
                
            tangent += (pi / 2.0)
            if self.indices[i] == 0:
                tangent -= 3.14159
                
            from arc import Arc_Radian
            tangent = Arc_Radian(tangent)

            
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
            stored = False
            stored_difference = 0.0
            stored_radius_sum = 0.0
            tangents = self.get_tangents()
            for i in range(len(tangents) - 1):
                for j in range(i+1, len(tangents)):
                    radius_sum = self.arcs[i].get_radius() + \
                                 self.arcs[j].get_radius()
                    
                    difference = fabs(tangents[i] - tangents[j])
                    if self.indices[i] != self.indices[j]:
                        difference = pi * 2.0 - difference
                    if not stored or (difference - stored_difference > 0.00001) or \
                       (fabs(difference - stored_difference) < 0.00001 and \
                        radius_sum > stored_radius_sum):
                        
                        stored = True
                        stored_indices = (i, j)
                        stored_difference = difference
                        stored_radius_sum = radius_sum
                        results = (self.arcs[i], self.arcs[j])
                    
                    if self.point == Vector(0,1):
                        print(difference)
        
        if self.point == Vector(0,1):
            print("starting info:")
            print(self.indices)
            for tangent in self.get_tangents():
                print(tangent)
            for arc in self.arcs:
                print(arc)
            print(len(self.arcs))
            print("results: " + str(results))
        
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

def cull_arc_bounded_areaa(arcs):
    point_info_list = get_arc_bounded_area_point_info(arcs)
    arc_ref_count = [0] * len(arcs)
    for point_info in point_info_list:
        counter = 0
        largest_arcs = point_info.get_largest_arcs()
        
        for i in range(len(arcs)):
            if arcs[i] in largest_arcs:
                arc_ref_count[i] += 1
                counter += 1
        print(counter)
    leftover_arcs = []
    for i in range(len(arcs)):
        if arc_ref_count[i] == 2:
            leftover_arcs.append(arcs[i])
            
    print("pass 1")
    print(arc_ref_count)
    print(len(arc_ref_count) == len(arcs))
    for arc in arcs:
        print(arc)
    for info in point_info_list:
        print(info)
    #return leftover_arcs
    return arcs

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
    print("culled")
    return results

def find_arcs_rightmost_value(arc):
    rightmost_value = None
    for extreme in arc.get_extremes():
        if rightmost_value == None or extreme.x > rightmost_value:
            rightmost_value = extreme.x
    return rightmost_value
def find_rightmost_arc(arcs):
    rightmost_arc = None
    rightmost_value = 0.0
    for arc in arcs:
        right_value = find_arcs_rightmost_value(arc)
        if rightmost_arc == None or right_value > rightmost_value:
            rightmost_arc = arc
            rightmost_value = right_value
    return rightmost_arc

def find_next_outer_arc(arcs, prev_arc, prev_point):
    #print("\n")
    point = None
    if prev_arc.get_last_point() == prev_point:
        point = prev_arc.get_first_point()
    else:
        point = prev_arc.get_last_point()
    
    #print(point)
            
    modified_original_tangent = Arc_Radian((pi) - prev_arc.get_tangent(point))
    #modified_original_tangent = prev_arc.get_tangent(point) - pi
    #print("original modified tangent: ")
    #print(modified_original_tangent)
    next_arc = None
    min_tangent_diff = 0.0
    next_arc_indice = 0
    for arc in arcs:
        if arc == prev_arc:
            continue
        if point in (arc.get_first_point(), arc.get_last_point()):
            arc_indice = 0
            if point == arc.get_last_point():
                arc_indice = 1
                
            tangent = arc.get_tangent(point)
            
            #if they are the same indice, no fabs
            if arc_indice == next_arc_indice:
                tangent_diff = tangent - modified_original_tangent
            else:
                tangent_diff = fabs(tangent - modified_original_tangent)
            tangent_diff = Arc_Radian(tangent_diff)
            '''
            print("Potential Arc: ")
            print(arc)
            print("tangent: ")
            print(tangent)
            print("diff: ")
            print(tangent_diff)
            print("arc indice: " + str(arc_indice))
            '''
            if next_arc == None or \
               ((next_arc_indice >= arc_indice) and \
               ((tangent_diff < min_tangent_diff and \
                 not fabs(min_tangent_diff - tangent_diff) < 0.00001) or \
                (fabs(min_tangent_diff - tangent_diff) < 0.00001 and \
                 arc.get_radius() > next_arc.get_radius()))):
                next_arc = arc
                min_tangent_diff = tangent_diff
                next_arc_indice = arc_indice
    return next_arc, point
            

def cull_arc_bounded_area(arcs): 
    '''
    Find the bounded area by traversing the outer bounds starting with the
    rightmost value (greatest x)
    '''
    point_info_list = get_arc_bounded_area_point_info(arcs)
    rightmost_arc = find_rightmost_arc(arcs)
    arc_list = [rightmost_arc]
    arc, last_point = find_next_outer_arc(arcs, rightmost_arc,
                                          rightmost_arc.get_first_point())
    i = 0
    while(arc != rightmost_arc):
        arc_list.append(arc)
        arc, last_point = find_next_outer_arc(arcs, arc, last_point)
        #print("result: " + str(arc))
        if arc == None:
            raise Exception("Failed to cull arc bounded area, hit dead end")
        i += 1
        if i > len(arcs):
            raise Exception("Infinite loop while determining outer arcs")
    return arc_list
