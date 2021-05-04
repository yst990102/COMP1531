from flask import Flask, request
from json import dumps

APP = Flask(__name__)

@APP.route("/echo", methods=['GET'])
def echo():
    return dumps({'data': request.args.get('data')})

if __name__ == '__main__':
    APP.run()