from json import dumps
from flask import Flask, request
import hashlib

APP = Flask(__name__)
        
data = {
    'users': [],
}

def getData():
    global data
    return data

def generateToken(username):
    return username

def getUserFromToken(token):
    data = getData()
    userInput = token
    for user in data['users']:
        if user['username'] == userInput:
            return userInput
    return None

@APP.route('/secrets', methods=['GET'])
def get():
    user = getUserFromToken(request.args.get('token'))
    if user is not None:
        password = None
        for dataUser in data['users']:
            if dataUser['username'] == user:
                password = dataUser['password']
        return dumps({
            'secrets' : password,
        })
    else:
        raise ValueError("Invalid permissions or token")

@APP.route('/register', methods=['POST'])
def create():
    info = request.get_json()
    data = getData()
    data['users'].append({
        'username': info['username'],
        'password': hashlib.sha256(info['password'].encode()).hexdigest(),
    })
    return dumps({
        'token': generateToken(info['username']),
    })

@APP.route('/login', methods=['POST'])
def connect():
    info = request.get_json()
    data = getData()
    print(data)
    for user in data['users']:
        if user['username'] == info['username']:
            if user['password'] == hashlib.sha256(info['password'].encode()).hexdigest():
                return dumps({
                    'token': generateToken(info['username']),
                })
    raise ValueError("Invalid username or password")

if __name__ == '__main__':
    APP.run(port=15333)
