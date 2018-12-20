from n_jointed_arm_ik import Vector, n_jointed_arm_ik, n_joint_range

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
        self.upper_bound = 0.0
        self.lower_bound = 0.0
        self.update_event = None
    def get_bounds(self):
        return n_joint_range(self.lengths)
    def set_update_event(self, update_event):
        self.update_event = update_event
    def set_N(self, new_N):
        self.N = new_N
            
        self.lengths = self.lengths[:min(len(self.lengths), self.N)]
        self.lengths += [1.0] * max(0, self.N - len(self.lengths))
        
        self.weights = self.weights[:min(len(self.weights), self.N)]
        self.weights += [1.0] * max(0, self.N - len(self.weights))

        self.angles = [0.0] * self.N
        
    def set_lengths(self, new_lengths):
        '''
        Set self.lengths and update associated values,
        and update self.point with new bounds
        '''
        if len(new_lengths) != self.N:
            print(self.N)
            raise InvalidArmControllerParameters
        
        self.lengths = new_lengths
        self.lower_bound, self.upper_bound = n_joint_range(self.lengths)

        if self.point == None:
            range = self.upper_bound - self.lower_bound
            midway_point = self.lower_bound + range / 2
            self.point = Vector(midway_point, 0.0)

    def set_weights(self, new_weights):
        '''
        Set self.weights and update angles with new weights
        '''
        if len(new_weights) != self.N - 2:
            raise InvalidArmControllerParameters
        
        self.weights = new_weights

    def refresh_results(self):
        self.update_angles()

    def bind_point(self):
        '''
        Calculate new self.point based on what is
        within the range of self.lengths
        '''
        if not self.point == None:
            point_mag = self.point.magnitude()
            point_scale = 1.0
            if point_mag < self.lower_bound:
                modified_lower = self.lower_bound * 1.000000000000001
                point_scale = modified_lower / point_mag
            elif point_mag > self.upper_bound:
                modified_upper = self.upper_bound * 0.999999999999999
                point_scale = modified_upper / point_mag
            self.point = self.point.scale(point_scale)
        
    def set_point(self, new_point):
        '''
        Update point and angles with new point
        '''
        self.point = new_point
        self.bind_point()
        self.update_angles()
        
    def update_angles(self):
        '''
        Run inverse kinematics equations to update self.angles
        '''
        if self.point != None:
            self.angles = n_jointed_arm_ik(self.lengths,
                                           self.weights, self.point)
            self.update_event(self.angles)
