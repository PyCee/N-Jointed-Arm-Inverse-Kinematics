from n_jointed_arm_ik import Vector, OutOfRange

class PathInProgress(Exception):
    pass
class Path_Instant:
    def __init__(self, t, point):
        self.time = t
        self.point = point
    def get_time(self):
        return self.time
    def get_point(self):
        return self.point
        
class Path_Controller:
    def __init__(self):
        self.update_point_event = None
        self.instants = []
        self.point = Vector(0.0, 0.0)
        self.time = 0.0
    def get_point(self):
        return self.point
    def get_time(self):
        return self.time
    def set_update_point_event(self, e):
        self.update_point_event = e
    def in_progress(self):
        return self.time > 0.0
    def add_instant(self, instant):
        if self.in_progress():
            raise PathInProgress
        
        self.instants.append(instant)
        self.instants.sort(key=lambda inst: inst.time)
    def get_duration(self):
        return self.instants[len(self.instants) - 1].get_time()
    def is_finished(self):
        return self.time >= self.get_duration()
    def step(self, dt):
        self.time += dt
        
        if self.time > self.get_duration():
            self.time = self.get_duration()
        for i in range(1, len(self.instants)):
            instant_time = self.instants[i].get_time()
            if self.time <= instant_time:
                prev_instant_time = self.instants[i-1].get_time()
                time_range = instant_time - prev_instant_time
                time_difference = self.time - prev_instant_time
                time_progress = time_difference / time_range

                base_point = self.instants[i-1].get_point()
                next_point = self.instants[i].get_point()
                
                point_range = next_point.subtract(base_point)
                scaled_point_range = point_range.scale(time_progress)
                self.point = base_point.add(scaled_point_range)
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
