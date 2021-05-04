from flask import Flask, request
from json import dumps

APP = Flask(__name__)

@APP.route("/one", methods=['GET'])
def one():
    return dumps({
    	'1': request.args.get('data1'),
    	'2': request.args.get('data2'),
    })

@APP.route("/two", methods=['POST'])
def two():
    data = request.get_json()
    return dumps({
    	'1': data['data1'],
    	'2': data['data2'],
    })

@APP.route("/three", methods=['PUT'])
def three():
    data = request.get_json()
    return dumps({
    	'1': data['data1'],
    	'2': data['data2'],
    })

@APP.route("/four", methods=['DELETE'])
def four():
    data = request.get_json()
    return dumps({
    	'1': data['data1'],
    	'2': data['data2'],
    })

if __name__ == '__main__':
    APP.run()