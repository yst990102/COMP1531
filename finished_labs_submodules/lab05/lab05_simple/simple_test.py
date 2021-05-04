import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests

BASE_URL = 'http://127.0.0.1:5001'


# Use this fixture to get the URL of the server.
@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "simple.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")


def test_url(url):
    '''
    A simple sanity test to check that your server is set up properly
    '''

    requests.post(f"{BASE_URL}/name/add", json={"name": "Asus"})
    requests.post(f"{BASE_URL}/name/add", json={"name": "Acer"})
    requests.post(f"{BASE_URL}/name/add", json={"name": "Dell"})

    get_content01 = requests.get(f"{BASE_URL}/names")
    Names01 = get_content01.json()
    assert Names01['name'] == ['Asus', 'Acer', 'Dell']

    requests.delete(f"{BASE_URL}/name/remove", json={"name": "Dell"})

    get_content02 = requests.get(f"{BASE_URL}/names")
    Names02 = get_content02.json()
    assert Names02['name'] == ['Asus', 'Acer']
