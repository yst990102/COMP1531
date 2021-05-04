# https://wiki.python.org/moin/UsingPickle

import pickle

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

with open('export.p', 'wb') as FILE:
    pickle.dump(DATA_STRUCTURE, FILE)
