from flask import Flask, request
from json import dumps

app = Flask(__name__)

firstName = ''
lastName = ''

@app.route('/reset', methods=['POST'])
def reset():
    global firstName, lastName
    firstName = ''
    lastName = ''
    return ""

@app.route('/info', methods=['GET'])
def info():
    uc = request.args.get('uc')
    uc = uc if uc is not None else False 
    return dumps({
        'firstName': firstName.upper() if uc else firstName,
        'lastName': lastName.upper() if uc else lastName,
    })

@app.route('/set', methods=['POST'])
def set():
    global firstName, lastName
    payload = request.get_json()
    firstName = payload['firstName']
    lastName = payload['lastName']
    return dumps({
        'firstName': payload['firstName'],
        'lastName': payload['lastName'],
    })

if __name__ == '__main__':
    app.run(port=9002)
