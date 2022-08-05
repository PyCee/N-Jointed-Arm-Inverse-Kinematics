from limited_arm.limited_n_jointed_arm_ik import limited_n_jointed_arm_ik, limited_n_jointed_arm_range, limited_n_jointed_arm_validity, OutOfRangeException
from n_jointed_arm.n_jointed_arm_ik import n_jointed_arm_ik
from n_jointed_arm.recreate_point import recreate_point
from vector import Vector
class InvalidArmControllerParameters(Exception):
    pass

class Arm_Controller:
    def __init__(self):
        self.has_set_point = False
        self.N = 0
        self.lengths = []
        self.lower_limits = []
        self.upper_limits = []
        self.weights = []
        self.point = None
        self.angles = []
        self.update_event = None
    def get_arc_bounded_area(self):
        return limited_n_jointed_arm_range(self.lengths, self.lower_limits,
                                           self.upper_limits)
    
    def set_update_event(self, update_event):
        self.update_event = update_event
    def set_N(self, new_N):
        self.N = new_N

        def change_N_for_list(li, N, default_value):
            li = li[:min(len(li), N)]
            li += [default_value] * max(0, N - len(li))

        change_N_for_list(self.lengths, self.N, 1.0)
        change_N_for_list(self.lower_limits, self.N, -1.5)
        change_N_for_list(self.upper_limits, self.N, 1.5)
        change_N_for_list(self.weights, self.N, 0.7)
        
        self.angles = [0.0] * self.N
        
    def set_parameters(self, N, lengths, lower_limits, upper_limits,
                           weights):
        self.set_N(N)
        self.set_lengths(lengths)
        self.set_lower_limits(lower_limits)
        self.set_upper_limits(upper_limits)
        self.set_weights(weights)
        #TODO make sure point is valid, or find a new valid point
        if self.point == None or not \
           limited_n_jointed_arm_validity(self.lengths, self.lower_limits,
                                          self.upper_limits, self.point):
            self.point = recreate_point(self.lengths, self.lower_limits)

        self.update_angles()
        
    def set_lengths(self, lengths):
        '''
        Validate and set lengths
        '''
        if len(lengths) != self.N:
            raise InvalidArmControllerParameters("Lengths being set ('" +
                                                 str(len(lengths)) +
                                                 "') does not match ('" +
                                                 str(self.N) + "')")
        
        self.lengths = lengths
        
    def set_lower_limits(self, lower_limits):
        '''
        Validate and set lower_limits
        '''
        if len(lower_limits) != self.N:
            raise InvalidArmControllerParameters
        
        self.lower_limits = lower_limits
    def set_upper_limits(self, upper_limits):
        '''
        Validate and set upper_limits
        '''
        if len(upper_limits) != self.N:
            raise InvalidArmControllerParameters
        
        self.upper_limits = upper_limits
    def set_weights(self, weights):
        '''
        Validate and set weights
        '''
        if len(weights) != self.N - 2:
            raise InvalidArmControllerParameters
        
        self.weights = weights

    def refresh_results(self):
        self.update_angles()
        
    def set_point(self, new_point):
        '''
        Update point and angles with new point
        '''
        self.point = new_point
        self.update_angles()
        
    def update_angles(self):
        '''
        Run inverse kinematics equations to update self.angles
        '''
        if not self.point is None:
            try:
                print("pre angles")
                self.angles = limited_n_jointed_arm_ik(self.lengths,
                                                       self.lower_limits,
                                                       self.upper_limits,
                                                       self.weights,
                                                       self.point)
                self.update_event(self.angles)
                print("angles")
            except (OutOfRangeException):
                print("Out of range... oh well")
            #self.angles = n_jointed_arm_ik(self.lengths,
            #                               self.weights, self.point)
