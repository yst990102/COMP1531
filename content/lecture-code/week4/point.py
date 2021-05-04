from json import dumps
from flask import Flask, request

APP = Flask(__name__)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def setX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y
        
# GLOBAL VARIABLE BELOW
point = None
# GLOBAL VARIABLE ABOVE

@APP.route('/point/get', methods=['GET'])
def get():
    global point
    x = 0
    y = 0
    print(point)
    if point is not None:
        x = point.getX()
        y = point.getY()
    return dumps({
        'x' : x,
        'y' : y,
    })

@APP.route('/point1/create', methods=['POST'])
def create():
    global point
    data = request.get_json()
    point = Point(data['x'], data['y'])
    return dumps({
    })

@APP.route('/point/update', methods=['PUT'])
def update():
    global point
    data = request.get_json()
    point.setX(data['x'])
    point.setY(data['y'])
    return dumps({
    })

@APP.route('/point/delete', methods=['DELETE'])
def delete():
    global point
    point = None
    return dumps({
    })


if __name__ == '__main__':
    APP.run(port=20000)

