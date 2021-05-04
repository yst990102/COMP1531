import json
import requests
import flask  # needed for urllib.parse

BASE_URL = 'http://127.0.0.1:5000'

def test_div():
    payload = requests.get(f"{BASE_URL}/getcount", params= { 'tag': 'div' }).json()
    assert payload['tag_count'] == 230


def test_img():
    payload = requests.get(f"{BASE_URL}/getcount", params= { 'tag': 'img' }).json()
    assert payload['tag_count'] == 17


def test_a():
    payload = requests.get(f"{BASE_URL}/getcount", params= { 'tag': 'a' }).json()
    assert payload['tag_count'] == 178


def test_non_existant_tag():
    payload = requests.get(f"{BASE_URL}/getcount", params= { 'tag': 'big' }).json()
    assert payload['tag_count'] == 0
