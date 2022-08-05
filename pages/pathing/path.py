import sys
from n_jointed_arm.n_jointed_arm_ik import Vector, OutOfRangeException
from math import *

class PathInProgress(Exception):
    pass
class PiecewiseRangeOverlap(Exception):
    pass
        
class Path:
    def __init__(self, functions):
        self.update_point_event = None
        self.__functions = functions
        self.__start = sys.maxsize
        self.__duration = 0.0
        for func in functions:
            start_t = func.get_start_t()
            if start_t <= self.__start:
                self.__start = start_t
            end_t = func.get_end_t()
            if end_t >= self.__duration:
                self.__duration = end_t

    
    def get_start(self):
        return self.__start
    def get_duration(self):
        return self.__duration
        
    def get_point(self, dt):
        updated_x = False
        updated_y = False
        point = Vector(0,0)
        for funct in self.__functions:
            if funct.contains_t(dt):
                if funct.has_x_evaluation():
                    point.x = funct.evaluate_x(dt)
                    updated_x = True
                if funct.has_y_evaluation():
                    point.y = funct.evaluate_y(dt)
                    updated_y = True
                if updated_x and updated_y:
                    break
        return point
    


    def __piecewise_overlap_at_t(self, base_func, check_func, t):
        if not check_func.evaluate_t(t):
            return False
        if base_func.has_x_evaluation() and check_func.has_x_evaluation():
            return True
        if base_func.has_y_evaluation() and check_func.has_y_evaluation():
            return True
        return False
