import pytest
import requests
import json
from src import config
"""
http server tests of auth.py
Auther: Lan Lin
"""


@pytest.fixture
def parameters():
    parameters = {
        "email": "haha@gmail.com",
        "password": "123iwuiused",
        "name_first": "Lan",
        "name_last": "Lin"
    }
    return parameters
#############################################################################
#                                                                           #
#                       http test for auth_register Error                   #
#                                                                           #
#############################################################################


def test_auth_register_invalid_email_http():
    requests.delete(config.url + 'clear/v1')
    parameters = {
        "email": "123.com",
        "password": "12345ufd",
        "name_first": "Lan",
        "name_last": "Lin"
    }
    status = requests.post(config.url + 'auth/register/v2', json=parameters).status_code
    assert status == 400


def test_auth_register_duplicate_email_http():
    requests.delete(config.url + 'clear/v1')
    parameters = {
        "email": "123.com",
        "password": "12345ufd",
        "name_first": "Lan",
        "name_last": "Lin"
    }
    requests.post(config.url + 'auth/register/v2', json=parameters)
    status = requests.post(config.url + 'auth/register/v2', json=parameters).status_code
    assert status == 400


def test_auth_register_pwd_length_http():
    requests.delete(config.url + 'clear/v1')
    parameters = {
        "email": "haha@gmail.com",
        "password": "123",
        "name_first": "Lan",
        "name_last": "Lin"
    }
    status = requests.post(config.url + 'auth/register/v2', json=parameters).status_code
    assert status == 400


def test_auth_register_firstName_length_http():
    requests.delete(config.url + 'clear/v1')
    parameters = {
        "email": "haha@gmail.com",
        "password": "123iwuiused",
        "name_first": "",
        "name_last": "Lin"
    }
    status = requests.post(config.url + 'auth/register/v2', json=parameters).status_code
    assert status == 400


def test_auth_register_lastName_length_http():
    requests.delete(config.url + 'clear/v1')
    parameters = {
        "email": "haha@gmail.com",
        "password": "123iwuiused",
        "name_first": "Lan",
        "name_last": ""
    }
    status = requests.post(config.url + 'auth/register/v2', json=parameters).status_code
    assert status == 400
#############################################################################
#                                                                           #
#                       http test for auth_login Error                   #
#                                                                           #
#############################################################################


def test_auth_login_invalid_email_http():
    requests.delete(config.url + 'clear/v1')
    parameters = {
        "email": "123.com",
        "password": "12345ufd",
        "name_first": "Lan",
        "name_last": "Lin"
    }
    status = requests.post(config.url + 'auth/login/v2', json=parameters).status_code
    assert status == 400


def test_auth_login_not_registered_email_http():
    requests.delete(config.url + 'clear/v1')
    parameters = {
        "email": "haha@gmail.com",
        "password": "123iwuiused",
        "name_first": "Lan",
        "name_last": "Lin"
    }
    requests.post(config.url + 'auth/register/v2', json=parameters)
    parameters2 = {
        "email": "haha1@gmail.com",
        "password": "123iwuiused"
    }
    status = requests.post(config.url + 'auth/login/v2', json=parameters2).status_code
    assert status == 400


def test_auth_login_wrong_password_http(parameters):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=parameters)
    parameters2 = {
        "email": "haha@gmail.com",
        "password": "123iwuiusepp"
    }
    status = requests.post(config.url + 'auth/login/v2', json=parameters2).status_code
    assert status == 400
#############################################################################
#                                                                           #
#                       http test for auth_logout Error                   #
#                                                                           #
#############################################################################


def test_auth_logout_invalid_token_http(parameters):
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', json=parameters)
    token = json.loads(resp.text).get('token')
    invalid_token = f"{token}123"
    resp = requests.post(config.url + 'auth/logout/v1', json={"token": invalid_token})
    assert json.loads(resp.text).get('is_success') is False

#############################################################################
#                                                                           #
#          http test for auth_register, auth_login, auth_logout             #
#                                                                           #
#############################################################################


"""
http tests for auth_register, auth_login, auth_logout successfully
to test logout, the test calls auth_register and auth_login,
which tests the three functions together
"""


def test_auth_logout_successfully_http(parameters):
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', json=parameters)
    parameters2 = {
        "email": "haha@gmail.com",
        "password": "123iwuiused"
    }
    resp2 = requests.post(config.url + 'auth/login/v2', json=parameters2)
    auth_user_id0 = json.loads(resp.text).get('auth_user_id')
    auth_user_id1 = json.loads(resp2.text).get('auth_user_id')
    token0 = json.loads(resp.text).get('token')
    token1 = json.loads(resp2.text).get('token')
    assert auth_user_id0 == 0
    assert auth_user_id1 == 0
    resp_logout0 = requests.post(config.url + 'auth/logout/v1', json={"token": token0})
    resp_logout1 = requests.post(config.url + 'auth/logout/v1', json={"token": token1})
    assert json.loads(resp_logout0.text).get('is_success') is True
    assert json.loads(resp_logout1.text).get('is_success') is True
    requests.delete(config.url + 'clear/v1')
#############################################################################
#                                                                           #
#   Test for auth_passwordreset_request_v1 and auth_passwordreset_reset_v1  #
#                                                                           #
#############################################################################


def test_for_request_and_reset_password(parameters):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + "auth/register/v2", json=parameters)

    def test_auth_passwordrequest_invalid_email():
        resp = requests.post(config.url + "auth/passwordreset/request/v1", json={'email': 'heihei@gmail.com'})
        assert resp.status_code == 400

    def test_auth_passwordreset_request_valid():
        resp = requests.post(config.url + "auth/passwordreset/request/v1", json={'email': 'haha@gmail.com'})
        assert resp.status_code == 200

    test_auth_passwordrequest_invalid_email()
    test_auth_passwordreset_request_valid()
    requests.delete(config.url + 'clear/v1')