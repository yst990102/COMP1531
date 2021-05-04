import json
import requests
import urllib

BASE_URL = 'http://127.0.0.1:9002'

def test_system():

    # Reset
    requests.post(f"{BASE_URL}/reset")

    # Get empty
    queryString = urllib.parse.urlencode({
        'uc' : False,
    })
    r = requests.get(f"{BASE_URL}/info?{queryString}")
    payload = r.json()
    assert payload['firstName'] == ''
    assert payload['lastName'] == ''

    r = requests.post(f"{BASE_URL}/set", json={
        'firstName' : 'Hayden',
        'lastName' : 'Smith',
    })
    payload = r.json()
    assert payload['firstName'] == 'Hayden'
    assert payload['lastName'] == 'Smith'

    queryString = urllib.parse.urlencode({
        'uc' : False,
    })
    r = requests.get(f"{BASE_URL}/info?{queryString}")
    payload = r.json()
    assert payload['firstName'] == 'HAYDEN'
    assert payload['lastName'] == 'SMITH'

if __name__ == '__main__':
    test_system()
