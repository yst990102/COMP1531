from flask import Flask, request
from json import dump, dumps

app = Flask(__name__)

names = []

# Write your routes here


@app.route('/name/add', methods=['POST'])
def add():
    global names
    data = request.get_json()
    names.append(data['name'])
    return dumps({})


@app.route('/names', methods=['GET'])
def names_print():
    global names
    return dumps({'name': names})


@app.route('/name/remove', methods=['DELETE'])
def remove():
    global names
    data = request.get_json()
    del_name = data['name']

    new_names = []
    for i in names:
        if i != del_name:
            new_names.append(i)
    names = new_names

    return dumps({})


if __name__ == '__main__':
    app.run(port=5001)