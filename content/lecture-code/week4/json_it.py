# https://realpython.com/python-json/

import json

DATA_STRUCTURE = {
    'names': [
        {
            'first' : 'Bob',
            'last' : 'Carr'
        },
        {
            'first' : 'Julia',
            'last' : 'Gillard'
        },
        {
            'first' : 'Ken',
            'last' : 'Henry'
        },
    ]
}

with open('export.json', 'w') as FILE:
    print(json.dumps(DATA_STRUCTURE))
    json.dump(DATA_STRUCTURE, FILE)
