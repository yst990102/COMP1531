import json
import requests

def get_payload():
    response = requests.get('http://127.0.0.1:5000/echo?data=hi')
    payload = response.json()
    print(payload)

if __name__ == '__main__':
    get_payload()
