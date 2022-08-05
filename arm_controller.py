from limited_arm.limited_n_jointed_arm_ik import limited_n_jointed_arm_ik, limited_n_jointed_arm_range, limited_n_jointed_arm_validity, OutOfRangeException
from n_jointed_arm.n_jointed_arm_ik import n_jointed_arm_ik, n_jointed_arm_range, n_jointed_arm_validity
from n_jointed_arm.recreate_point import recreate_point
from vector import Vector
class InvalidArmControllerParameters(Exception):
    pass

class Arm_Controller:
    def __init__(self):
        self.has_set_point = False
        self.N = 0
        self.lengths = []
        self.weights = []
        self.point = None
        self.angles = []
        self.update_event = None
        self.can_reach_point = False
        self.attempted_reach_point = (0.0, 0.0)
    
    def set_update_event(self, update_event):
        self.update_event = update_event
    def set_N(self, new_N):
        self.N = new_N

        def change_N_for_list(li, N, default_value):
            li = li[:min(len(li), N)]
            li += [default_value] * max(0, N - len(li))

        change_N_for_list(self.lengths, self.N, 1.0)
        change_N_for_list(self.weights, self.N, 0.7)
        
        self.angles = [0.0] * self.N
        
    def set_parameters(self, N, lengths,
                           weights):
        self.set_N(N)
        self.set_lengths(lengths)
        self.set_weights(weights)
        #TODO make sure point is valid, or find a new valid point
        if self.point == None or not \
            n_jointed_arm_validity(self.lengths, self.point):
            self.point = recreate_point(self.lengths, self.angles)

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
            self.can_reach_point = n_jointed_arm_validity(self.lengths, self.point)
            if not self.can_reach_point:
                self.attempted_reach_point = self.point
                self.point = self.calculate_point_in_range(self.point)
            else:
                self.attempted_reach_point = None

            self.angles = n_jointed_arm_ik(self.lengths,
                                           self.weights, self.point)
    def calculate_point_in_range(self, point):
        magnitude = point.magnitude()
        if magnitude == 0.0: magnitude = 1
        temp_bounds = self.get_bounds()
        bounds = (temp_bounds[0] * 1.000001, temp_bounds[1] * 0.999999)
        ratio = 1
        angle = 0
        if magnitude < bounds[0]:
            ratio = bounds[0] / magnitude
        elif magnitude > bounds[1]:
            ratio = bounds[1] / magnitude
        point = point.scale(ratio)
        return point
    def get_bounds(self):
        return n_jointed_arm_range(self.lengths)
