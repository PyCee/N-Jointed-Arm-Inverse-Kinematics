import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y 
    def __repr__(self):
        return "(" + str(round(self.x, 3)) + ", " + \
            str(round(self.y, 3)) + ")"
    def __eq__(self, other):
        return other != None and math.fabs(self.x - other.x) < 0.001 and \
                        math.fabs(self.y - other.y) < 0.001
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    def scale(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2) 
    def dot(self, other):
        return self.x * other.x + self.y * other.y
    def cross_z(self, other):
        return self.x * other.y - self.y * self.x
