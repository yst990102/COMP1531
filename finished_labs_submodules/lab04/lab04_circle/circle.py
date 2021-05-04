import math


class Circle:
    def __init__(self, radius):
        self.radius = radius
        if radius <= 0:
            raise ValueError("radius needs to be greater than 0!")

    def circumference(self):
        return 2 * math.pi * self.radius

    def area(self):
        return math.pi * (self.radius ** 2)
