import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y 
    def __repr__(self):
        return "(" + str(round(self.x, 3)) + ", " + \
            str(round(self.y, 3)) + ")"
    def __eq__(self, other):
        return other != None and math.isclose(self.x, other.x, abs_tol=0.001) and \
                        math.isclose(self.y, other.y, abs_tol=0.001)
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    def scale(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    def magnitude(self):
        mag_sq = self.x**2 + self.y**2
        if mag_sq == 0.0:
            return 0.0
        else:
            return math.sqrt(mag_sq)
    def normalize(self):
        return self.scale(1.0 / self.magnitude())
    def dot(self, other):
        return self.x * other.x + self.y * other.y
    def cross_z(self, other):
        return self.x * other.y - self.y * other.x
    def get_angle(self, other):
        norm_difference = (other - self).normalize()
        angle = math.acos(norm_difference.x)
        if math.asin(norm_difference.y) < 0.0:
            angle *= -1.0
        return angle
    def get_abs_angle(self):
        if self == Vector(0.0, 0.0):
            return 0.0
        return Vector(0.0, 0.0).get_angle(self)
    
def Angle_Vector(radians, length):
    return Vector(math.cos(radians), math.sin(radians)).scale(length)
