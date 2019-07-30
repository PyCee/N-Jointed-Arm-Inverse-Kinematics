from n_jointed_arm_ik import Vector, OutOfRangeException
from math import *

#Path runtime (seconds)
MAX_PATH_DURATION = 60.0

class PathInProgress(Exception):
    pass
class PiecewiseRangeOverlap(Exception):
    pass
class Piecewise_Function:
    def __init__(self, t_eval, x_eval, y_eval):
        self.__t_eval = t_eval
        self.__x_eval = x_eval
        self.__y_eval = y_eval
    def evaluate_t(self, t):
        return eval(self.__t_eval)
    def evaluate_x(self, t):
        return eval(self.__x_eval)
    def evaluate_y(self, t):
        return eval(self.__y_eval)
        
class Path_Controller:
    def __init__(self):
        self.update_point_event = None
        self.__t_functions = []
        self.point = Vector(0.0, 0.0)
        self.__t = 0.0
        self.__duration = 0.0
    def get_point(self):
        return self.point
    def get_time(self):
        return self.__t
    def set_update_point_event(self, e):
        self.update_point_event = e
    def in_progress(self):
        return self.__t > 0.0
    
    def get_duration(self):
        return self.__duration
    def is_finished(self):
        return self.__t >= self.get_duration()
    
    def __piecewise_overlap(self, piecewise_function):
        '''Check that the new piecewise function doesn't overlap 
        with any previously added functions'''

        overlap = False
        t = 0.0
        while t < MAX_PATH_DURATION:
            if piecewise_function.evaluate_t(t):
                for func in self.__t_functions:
                    if func.evaluate_t(t):
                        overlap = True
                        break
            if overlap:
                break
            t += 0.01
        return overlap
    
    def add_piecewise_function(self, piecewise_function):
        if self.in_progress():
            raise PathInProgress

        if self.__piecewise_overlap(piecewise_function):
            raise PiecewiseRangeOverlap
        else:
            t = self.get_duration()
            while t < MAX_PATH_DURATION:
                if piecewise_function.evaluate_t(t):
                    self.__duration = t
                t += 0.01
            self.__t_functions.append(piecewise_function)
        
    def step(self, dt):
        self.__t += dt
        
        if self.__t > self.get_duration():
            self.__t = self.get_duration()

        for funct in self.__t_functions:
            if funct.evaluate_t(self.__t):
                # TODO: check if piecewise function has x, and if it doesn't, don't change x. same for y
                x = funct.evaluate_x(self.__t)
                y = funct.evaluate_y(self.__t)
                self.point = Vector(x, y)
                break
        if self.update_point_event != None:
            self.update_point_event(self.point)
    def reset(self):
        self.time = 0.0
    def __repr__(self):
        output_str = "["
        for inst in self.instants:
            output_str += str(inst.time) + ": " + str(inst.get_point()) + "\n"
        output_str += "]"
        return  output_str
