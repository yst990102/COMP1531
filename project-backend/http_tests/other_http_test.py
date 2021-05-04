import pytest
import requests
import json
from src import config

"""
http server tests of other.py
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


@pytest.fixture
def parameters1():
    parameters = {
        "email": "haha1@gmail.com",
        "password": "123iwuiused",
        "name_first": "Lan",
        "name_last": "Lin"
    }
    return parameters


@pytest.fixture
def parameters2():
    parameters = {
        "email": "haha2@gmail.com",
        "password": "123iwuiused",
        "name_first": "Lan",
        "name_last": "Lin"
    }
    return parameters


#############################################################################
#                                                                           #
#                       http test for clear                                 #
#                                                                           #
#############################################################################


def test_clear(parameters):
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json=parameters)
    token = json.loads(user.text).get('token')
    u_id = json.loads(user.text).get('auth_user_id')
    json_input1 = {"token": token, "name": "channel0", "is_public": True}
    requests.post(config.url + 'channels/create/v2', json=json_input1)
    # check that the user exists and the channel exists
    assert requests.get(config.url + 'channels/list/v2?token=' + token).status_code == 200
    requests.delete(config.url + 'clear/v1')
    # check that the user does not exist
    assert requests.get(config.url + 'user/profile/v2?token=' + token + '&u_id=' + str(u_id)).status_code == 403


#############################################################################
#                                                                           #
#                       http test for search                                 #
#                                                                           #
#############################################################################


def test_search_invalid_length(parameters, parameters1):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters)
    token0 = json.loads(user0.text).get('token')
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    uid1 = json.loads(user1.text).get('auth_user_id')
    # create a dm, users in dm are user0, 1
    json_input1 = {"token": token0, "u_ids": [uid1]}
    dm = requests.post(config.url + 'dm/create/v1', json=json_input1)
    dm_id = json.loads(dm.text).get('dm_id')
    # send 3 messages to the dm
    json_input3 = {"token": token0, "dm_id": dm_id, "message": "hha"}
    requests.post(config.url + 'message/senddm/v1', json=json_input3)
    invalid_query = "h" * 1005
    status = requests.get(config.url + 'search/v2?token=' + token0 + '&query_str=' + invalid_query).status_code
    assert status == 400


def test_search_valid(parameters, parameters1):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters)
    token0 = json.loads(user0.text).get('token')
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    uid1 = json.loads(user1.text).get('auth_user_id')
    # create a dm, users in dm are user0, 1
    json_input1 = {"token": token0, "u_ids": [uid1]}
    dm = requests.post(config.url + 'dm/create/v1', json=json_input1)
    dm_id = json.loads(dm.text).get('dm_id')
    # send 3 messages to the dm
    json_input3 = {"token": token0, "dm_id": dm_id, "message": "haha0"}
    json_input4 = {"token": token0, "dm_id": dm_id, "message": "you know HAHA"}
    json_input5 = {"token": token0, "dm_id": dm_id, "message": "ha is not invalid"}
    requests.post(config.url + 'message/senddm/v1', json=json_input3)
    requests.post(config.url + 'message/senddm/v1', json=json_input4)
    requests.post(config.url + 'message/senddm/v1', json=json_input5)

    message_list = requests.get(config.url + 'search/v2?token=' + token0 + '&query_str=haha')
    message_list = json.loads(message_list.text).get('messages')
    assert message_list[0]['message'] == "haha0"
    assert message_list[1]['message'] == "you know HAHA"


#############################################################################
#                                                                           #
#                       http test for notification                          #
#                                                                           #
#############################################################################


def test_notification(parameters, parameters1):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters)
    token0 = json.loads(user0.text).get('token')
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    uid1 = json.loads(user1.text).get('auth_user_id')
    token1 = json.loads(user1.text).get('token')
    # create a dm, users in dm are user0, 1
    json_input1 = {"token": token0, "u_ids": [uid1]}
    dm = requests.post(config.url + 'dm/create/v1', json=json_input1)
    dm_id = json.loads(dm.text).get('dm_id')
    # send 3 messages to the dm
    json_input3 = {"token": token0, "dm_id": dm_id, "message": "It's the message sent to test notification, @lanlin0"}
    requests.post(config.url + 'message/senddm/v1', json=json_input3)

    notification_list = requests.get(config.url + 'notifications/get/v1?token=' + token1)
    notification_list = json.loads(notification_list.text).get('notifications')
    assert notification_list[1]['notification_message'] == "lanlin added you to lanlin, lanlin0"
    assert notification_list[0]['notification_message'] == "lanlin tagged you in lanlin, lanlin0: It's the message sen"
    requests.delete(config.url + 'clear/v1')