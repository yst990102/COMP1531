from stubs.auth import login

def test_login1():
    assert login() == 'token'
