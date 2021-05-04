# https://realpython.com/python-json/

import json

with open('export.json', 'r') as FILE:
    DATA = json.load(FILE)
    print(DATA)
