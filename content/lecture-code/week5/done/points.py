from math import sqrt, pi, cos, sin

class Point:
    def __init__(self, r, theta):
        self.r = r
        self.theta = theta

    def getX(self):
    	return self.r * cos(self.theta)

    def getY(self):
    	return self.r * sin(self.theta)

def distance(start, end):
    return sqrt((end.getX() - start.getX())**2 + (end.getY() - start.getY())**2)

if __name__ == '__main__':
	p1 = Point(3, pi/4)
	p2 = Point(4, pi/6)
	print(distance(p1, p2))