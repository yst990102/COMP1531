from flask import Flask, request
from json import dumps
import pickle

APP = Flask(__name__)


data = []
try:
    data = pickle.load(open("datastore.p", "rb"))
except Exception:
	pass

def getData():
    global data
    return data

def save():
    data = getData()
    with open('datastore.p', 'wb') as FILE:
        pickle.dump(data, FILE)

@APP.route("/add", methods=['POST'])
def add():
    args = request.get_json()
    data = getData()
    data.append(args['data'])
    save()
    return dumps(data)

if __name__ == '__main__':
    APP.run()