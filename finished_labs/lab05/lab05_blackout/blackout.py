import math

Earth_radius = 6378137


class City():
    def __init__(self, name, theta):
        self.name = name
        self.theta = theta
        self.intervals = 0
        self.x = math.sin(theta) * Earth_radius
        self.y = math.cos(theta) * Earth_radius


class Satellite():
    def __init__(self, height, velocity, theta):
        self.height = height
        self.velocity = velocity
        self.theta = theta
        self.tangent_len = ((Earth_radius + height)**2 - (Earth_radius**2))**0.5
        self.angular_velocity_min = velocity * 60 / (Earth_radius + height)

    @property
    def x(self):
        return math.sin(self.theta) * (self.height + Earth_radius)

    @property
    def y(self):
        return math.cos(self.theta) * (self.height + Earth_radius)


def dis_city_satellite(City, Satellite):
    x_dis = abs(Satellite.x - City.x)
    y_dis = abs(Satellite.y - City.y)
    return ((x_dis**2) + (y_dis**2))**0.5


def update_satellite(Satellite):
    Satellite.theta += Satellite.angular_velocity_min


def check_blackout(City, Satellite):
    if dis_city_satellite(City, Satellite) < Satellite.tangent_len:
        return False  # no blackout
    elif feq(dis_city_satellite(City, Satellite), Satellite.tangent_len) == True:
        return False
    else:
        return True  # blackout


def feq(a, b):
    return abs(a - b) <= 1e-6