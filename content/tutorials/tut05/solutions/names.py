# Coming Soon
import math
import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

names = []

def dateToAge(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp)
    now = datetime.datetime.now()
    diff = now - dt
    return math.floor(diff.days / 365)

@app.route('/addname', methods=['POST'])
def addname():
    global names # Why this? :O
    data = request.get_json()
    names.append({
        'name': data['name'],
        'age': dateToAge(int(data['dob']))
    })
    print(data)
    return {}

@app.route('/getnames', methods=['GET'])
def getnames():
    return jsonify(names)

if __name__ == '__main__':
    app.run()
