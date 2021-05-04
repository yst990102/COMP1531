import pytest
import requests
import json
from src import config
"""
http server tests of channel.py and channels.py
Author: Emir Aditya Zen
"""


@pytest.fixture
def user1():
    user1 = {
        "email": "haha@gmail.com",
        "password": "123123123",
        "name_first": "Peter",
        "name_last": "White"
    }
    return user1

@pytest.fixture
def user2():
    user2 = {
        "email": "test@testexample.com",
        "password": "wp01^#$dp1o23",
        "name_first": "Tom",
        "name_last": "Green"
    }
    return user2

@pytest.fixture
def user3():
    user3 = {
        "email": "test@secondtestexample.com",
        "password": "somerandomword",
        "name_first": "John",
        "name_last": "Jones"
    }
    return user3


#############################################################################
#                                                                           #
#                       http test for channel_invite Error                  #
#                                                                           #
#############################################################################


def test_channel_invite_invalid_channel_http(user1, user2):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    token1 = json.loads(user1_login.text).get('token')
    json.loads(user2_login.text).get('token')
    u_id2 = json.loads(user2_login.text).get('auth_user_id')
    channel = requests.post(config.url + 'channels/create/v2', json={"token": token1,"name": "channelone", "is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    invalid_channelid = f"{channel_id}123"
    output = requests.post(config.url + 'channel/invite/v2', json={"token":token1,"channel_id":invalid_channelid, "u_id":u_id2}).status_code
    assert output == 400


def test_channel_invite_invalid_u_id_http(user1, user2):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    token1 = json.loads(user1_login.text).get('token')
    json.loads(user2_login.text).get('token')
    u_id2 = json.loads(user2_login.text).get('auth_user_id')
    invalid_u_id = f"{u_id2}123"
    channel = requests.post(config.url + 'channels/create/v2', json={"token": token1, "name": "channelone", "is_public": True})
    channel_id = json.loads(channel.text).get('channel_id')
    output = requests.post(config.url + 'channel/invite/v2', json={"token": token1, "channel_id": channel_id, "u_id": invalid_u_id}).status_code
    assert output == 400


def test_channel_invite_unauthorised_user_http(user1, user2,user3):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    requests.post(config.url + 'auth/register/v2', json=user3)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    user3_login = requests.post(config.url + 'auth/login/v2', json=user3)
    token1 = json.loads(user1_login.text).get('token')
    token2 = json.loads(user2_login.text).get('token')
    u_id3 = json.loads(user3_login.text).get('auth_user_id')
    channel = requests.post(config.url + 'channels/create/v2', json={"token": token1, "name": "channelone", "is_public": True})
    channel_id = json.loads(channel.text).get('channel_id')
    output = requests.post(config.url + 'channel/invite/v2', json={"token": token2, "channel_id": channel_id, "u_id": u_id3}).status_code
    assert output == 403


def test_channel_invite_invalid_token_http(user1, user2):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    token1 = json.loads(user1_login.text).get('token')
    invalid_token = f"{token1}123"
    json.loads(user2_login.text).get('token')
    u_id2 = json.loads(user2_login.text).get('auth_user_id')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    output = requests.post(config.url + 'channel/invite/v2', json={"token":invalid_token,"channel_id":channel_id,"u_id":u_id2}).status_code
    assert output == 403


#############################################################################
#                                                                           #
#                       http test for channel_details Error                 #
#                                                                           #
#############################################################################


def test_channel_details_invalid_channel_http(user1):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    token1 = json.loads(user1_login.text).get('token')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    invalid_channelid = f"{channel_id}123"
    output = requests.get(config.url + 'channel/details/v2' + f'?token={token1}&channel_id={invalid_channelid}').status_code
    assert output == 400


def test_channel_details_unauthorised_user_http(user1, user2):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    token1 = json.loads(user1_login.text).get('token')
    token2 = json.loads(user2_login.text).get('token')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    output = requests.get(config.url + 'channel/details/v2' + f'?token={token2}&channel_id={channel_id}').status_code
    assert output == 403


def test_channel_details_invalid_token_http(user1):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    token1 = json.loads(user1_login.text).get('token')
    invalid_token = f"{token1}123"
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    output = requests.get(config.url + 'channel/details/v2' + f'?token={invalid_token}&channel_id={channel_id}').status_code
    assert output == 403


#############################################################################
#                                                                           #
#                       http test for channel_join Error                    #
#                                                                           #
#############################################################################


def test_channel_join_invalid_channel_http(user1,user2):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    token1 = json.loads(user1_login.text).get('token')
    token2 = json.loads(user2_login.text).get('token')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    invalid_channelid = f"{channel_id}123"
    output = requests.post(config.url + 'channel/join/v2', json={"token":token2,"channel_id":invalid_channelid}).status_code
    assert output == 400


def test_channel_join_private_channel_http(user1,user2):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    token1 = json.loads(user1_login.text).get('token')
    token2 = json.loads(user2_login.text).get('token')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":False})
    channel_id = json.loads(channel.text).get('channel_id')
    output = requests.post(config.url + 'channel/join/v2', json={"token":token2,"channel_id":channel_id}).status_code
    assert output == 403


def test_channel_join_invalid_token_http(user1,user2):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    token1 = json.loads(user1_login.text).get('token')
    token2 = json.loads(user2_login.text).get('token')
    invalid_token = f"{token2}123"
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    output = requests.post(config.url + 'channel/join/v2', json={"token":invalid_token,"channel_id":channel_id}).status_code
    assert output == 403


#############################################################################
#                                                                           #
#               http test for channel_join Global exception                 #
#                                                                           #
#############################################################################


def test_channel_join_global_owner_exception_http(user1,user2):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    token1 = json.loads(user1_login.text).get('token')
    token2 = json.loads(user2_login.text).get('token')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token2,"name":"channelone","is_public":False})
    channel_id = json.loads(channel.text).get('channel_id')
    output = requests.post(config.url + 'channel/join/v2', json={"token":token1,"channel_id":channel_id}).status_code
    assert output == 200
    output2 = requests.get(config.url + 'channel/details/v2' + f'?token={token2}&channel_id={channel_id}')
    assert output2.status_code == 200
    assert len(json.loads(output2.text)['all_members']) == 2


#############################################################################
#                                                                           #
#                     http test for channel_addowner Error                  #
#                                                                           #
#############################################################################


def test_channel_addowner_invalid_channel_http(user1,user2):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    token1 = json.loads(user1_login.text).get('token')
    token2 = json.loads(user2_login.text).get('token')
    u_id2 = json.loads(user2_login.text).get('auth_user_id')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    invalid_channelid = f"{channel_id}123"
    requests.post(config.url + 'channels/join/v2', json={"token":token2,"channel_id":channel_id})
    output = requests.post(config.url + 'channel/addowner/v1', json={"token":token1,"channel_id":invalid_channelid,"u_id":u_id2}).status_code
    assert output == 400


def test_channel_addowner_current_owner_http(user1,user2):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    token1 = json.loads(user1_login.text).get('token')
    token2 = json.loads(user2_login.text).get('token')
    u_id2 = json.loads(user2_login.text).get('auth_user_id')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    requests.post(config.url + 'channels/join/v2', json={"token":token2,"channel_id":channel_id})
    requests.post(config.url + 'channel/addowner/v2', json={"token":token1,"channel_id":channel_id,"u_id":u_id2})
    output = requests.post(config.url + 'channel/addowner/v1', json={"token":token1,"channel_id":channel_id,"u_id":u_id2}).status_code
    assert output == 400


def test_channel_addowner_unauthorised_user_http(user1,user2,user3):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    requests.post(config.url + 'auth/register/v2', json=user3)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    user3_login = requests.post(config.url + 'auth/login/v2', json=user3)
    token1 = json.loads(user1_login.text).get('token')
    token2 = json.loads(user2_login.text).get('token')
    token3 = json.loads(user3_login.text).get('token')
    u_id2 = json.loads(user2_login.text).get('auth_user_id')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    requests.post(config.url + 'channel/join/v2', json={"token":token2,"channel_id":channel_id})
    requests.post(config.url + 'channel/join/v2', json={"token":token3,"channel_id":channel_id})
    output = requests.post(config.url + 'channel/addowner/v1', json={"token":token3,"channel_id":channel_id,"u_id":u_id2}).status_code
    assert output == 403


def test_channel_addowner_invalid_token_http(user1,user2):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    token1 = json.loads(user1_login.text).get('token')
    token2 = json.loads(user2_login.text).get('token')
    invalid_token = f"{token1}123"
    u_id2 = json.loads(user2_login.text).get('auth_user_id')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    requests.post(config.url + 'channel/join/v2', json={"token":token2,"channel_id":channel_id})
    output = requests.post(config.url + 'channel/addowner/v1', json={"token":invalid_token,"channel_id":channel_id,"u_id":u_id2}).status_code
    assert output == 403


#############################################################################
#                                                                           #
#             http test for channel_addowner Global exception               #
#                                                                           #
#############################################################################


def test_channel_addowner_global_owner_exception_http(user1,user2,user3):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    requests.post(config.url + 'auth/register/v2', json=user3)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    user3_login = requests.post(config.url + 'auth/login/v2', json=user3)
    token1 = json.loads(user1_login.text).get('token')
    token2 = json.loads(user2_login.text).get('token')
    token3 = json.loads(user3_login.text).get('token')
    u_id3 = json.loads(user3_login.text).get('auth_user_id')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token2,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    requests.post(config.url + 'channel/join/v2', json={"token":token3,"channel_id":channel_id})
    output = requests.post(config.url + 'channel/addowner/v1', json={"token":token1,"channel_id":channel_id,"u_id":u_id3}).status_code
    assert output == 200
    output2 = requests.get(config.url + 'channel/details/v2' + f'?token={token2}&channel_id={channel_id}')
    assert output2.status_code == 200
    assert len(json.loads(output2.text)['all_members']) == 2
    assert len(json.loads(output2.text)['owner_members']) == 2

#############################################################################
#                                                                           #
#                   http test for channel_removeowner Error                 #
#                                                                           #
#############################################################################


def test_channel_removeowner_invalid_channel_http(user1,user2):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    token1 = json.loads(user1_login.text).get('token')
    token2 = json.loads(user2_login.text).get('token')
    u_id2 = json.loads(user2_login.text).get('auth_user_id')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    invalid_channelid = f"{channel_id}123"
    requests.post(config.url + 'channels/join/v2', json={"token":token2,"channel_id":channel_id})
    requests.post(config.url + 'channel/addowner/v1', json={"token":token1,"channel_id":channel_id,"u_id":u_id2})
    output = requests.post(config.url + 'channel/removeowner/v1', json={"token":token1,"channel_id":invalid_channelid,"u_id":u_id2}).status_code
    assert output == 400


def test_channel_removeowner_current_member_http(user1,user2):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    token1 = json.loads(user1_login.text).get('token')
    token2 = json.loads(user2_login.text).get('token')
    u_id2 = json.loads(user2_login.text).get('auth_user_id')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    requests.post(config.url + 'channels/join/v2', json={"token":token2,"channel_id":channel_id})
    output = requests.post(config.url + 'channel/removeowner/v1', json={"token":token1,"channel_id":channel_id,"u_id":u_id2}).status_code
    assert output == 400


def test_channel_removeowner_only_owner_http(user1, user2):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    token1 = json.loads(user1_login.text).get('token')
    token2 = json.loads(user2_login.text).get('token')
    u_id2 = json.loads(user2_login.text).get('auth_user_id')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token2,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    output = requests.post(config.url + 'channel/removeowner/v1', json={"token":token1,"channel_id":channel_id,"u_id":u_id2}).status_code
    assert output == 400


def test_channel_removeowner_unauthorised_user_http(user1, user2, user3):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    requests.post(config.url + 'auth/register/v2', json=user3)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    user3_login = requests.post(config.url + 'auth/login/v2', json=user3)
    token1 = json.loads(user1_login.text).get('token')
    token2 = json.loads(user2_login.text).get('token')
    token3 = json.loads(user3_login.text).get('token')
    u_id2 = json.loads(user2_login.text).get('auth_user_id')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    requests.post(config.url + 'channel/join/v2', json={"token":token2,"channel_id":channel_id})
    requests.post(config.url + 'channel/join/v2', json={"token":token3,"channel_id":channel_id})
    requests.post(config.url + 'channel/addowner/v1', json={"token":token1,"channel_id":channel_id,"u_id":u_id2})
    output = requests.post(config.url + 'channel/removeowner/v1', json={"token":token3,"channel_id":channel_id,"u_id":u_id2}).status_code
    assert output == 403


def test_channel_removeowner_invalid_token_http(user1, user2):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    token1 = json.loads(user1_login.text).get('token')
    token2 = json.loads(user2_login.text).get('token')
    invalid_token = f"{token1}123"
    u_id2 = json.loads(user2_login.text).get('auth_user_id')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    requests.post(config.url + 'channel/join/v2', json={"token":token2,"channel_id":channel_id})
    requests.post(config.url + 'channel/addowner/v1', json={"token":token1,"channel_id":channel_id,"u_id":u_id2})
    output = requests.post(config.url + 'channel/removeowner/v1', json={"token":invalid_token,"channel_id":channel_id,"u_id":u_id2}).status_code
    assert output == 403


#############################################################################
#                                                                           #
#            http test for channel_removeowner Global exception             #
#                                                                           #
#############################################################################


def test_channel_removeowner_global_owner_exception_http(user1, user2, user3):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    requests.post(config.url + 'auth/register/v2', json=user3)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    user3_login = requests.post(config.url + 'auth/login/v2', json=user3)
    token1 = json.loads(user1_login.text).get('token')
    token2 = json.loads(user2_login.text).get('token')
    token3 = json.loads(user3_login.text).get('token')
    u_id3 = json.loads(user3_login.text).get('auth_user_id')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token2,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    requests.post(config.url + 'channel/join/v2', json={"token":token3,"channel_id":channel_id})
    requests.post(config.url + 'channel/addowner/v1', json={"token":token2,"channel_id":channel_id,"u_id":u_id3})
    output = requests.post(config.url + 'channel/removeowner/v1', json={"token":token1,"channel_id":channel_id,"u_id":u_id3}).status_code
    assert output == 200
    output2 = requests.get(config.url + 'channel/details/v2' + f'?token={token2}&channel_id={channel_id}')
    assert output2.status_code == 200
    assert len(json.loads(output2.text)['all_members']) == 2
    assert len(json.loads(output2.text)['owner_members']) == 1


#############################################################################
#                                                                           #
#                      http test for channel_leave Error                    #
#                                                                           #
#############################################################################


def test_channel_leave_invalid_channel_http(user1, user2):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    token1 = json.loads(user1_login.text).get('token')
    token2 = json.loads(user2_login.text).get('token')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    invalid_channelid = f"{channel_id}123"
    requests.post(config.url + 'channels/join/v2', json={"token":token2,"channel_id":channel_id})
    output = requests.post(config.url + 'channel/leave/v1', json={"token":token2,"channel_id":invalid_channelid}).status_code
    assert output == 400


def test_channel_leave_unauthorised_user_http(user1,user2):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    token1 = json.loads(user1_login.text).get('token')
    token2 = json.loads(user2_login.text).get('token')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    output = requests.post(config.url + 'channel/leave/v1', json={"token":token2,"channel_id":channel_id}).status_code
    assert output == 403


def test_channel_leave_invalid_token_http(user1,user2):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    token1 = json.loads(user1_login.text).get('token')
    token2 = json.loads(user2_login.text).get('token')
    invalid_token = f"{token2}123"
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    requests.post(config.url + 'channels/join/v2', json={"token":token2,"channel_id":channel_id})
    output = requests.post(config.url + 'channel/leave/v1', json={"token":invalid_token,"channel_id":channel_id}).status_code
    assert output == 403


#############################################################################
#                                                                           #
#                      http test for channels_list Error                    #
#                                                                           #
#############################################################################


def test_channels_list_invalid_token_http(user1):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    token1 = json.loads(user1_login.text).get('token')
    invalid_token = f"{token1}123"
    requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    output = requests.get(config.url + 'channels/list/v2' + f'?token={invalid_token}').status_code
    assert output == 403


#############################################################################
#                                                                           #
#                    http test for channels_listall Error                   #
#                                                                           #
#############################################################################


def test_channels_listall_invalid_token_http(user1):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    token1 = json.loads(user1_login.text).get('token')
    invalid_token = f"{token1}123"
    requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    output = requests.get(config.url + 'channels/listall/v2' + f'?token={invalid_token}').status_code
    assert output == 403


#############################################################################
#                                                                           #
#                    http test for channels_create Error                    #
#                                                                           #
#############################################################################


def test_channels_create_invalid_name_http(user1):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    token1 = json.loads(user1_login.text).get('token')
    invalid_name = "a"*50
    output = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":invalid_name,"is_public":True}).status_code
    assert output == 400


def test_channels_create_invalid_token_http(user1):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    token1 = json.loads(user1_login.text).get('token')
    invalid_token = f"{token1}123"
    output = requests.post(config.url + 'channels/create/v2', json={"token":invalid_token,"name":"channelone","is_public":True}).status_code
    assert output == 403


#############################################################################
#                                                                           #
#         http test for valid channel and channels implementation           #
#                                                                           #
#############################################################################


def test_channel_channels_valid_implementation(user1,user2,user3):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    requests.post(config.url + 'auth/register/v2', json=user2)
    requests.post(config.url + 'auth/register/v2', json=user3)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    user3_login = requests.post(config.url + 'auth/login/v2', json=user3)
    token1 = json.loads(user1_login.text).get('token')
    token2 = json.loads(user2_login.text).get('token')
    token3 = json.loads(user3_login.text).get('token')
    u_id2 = json.loads(user2_login.text).get('auth_user_id')

    # Test valid channels_create function
    create_channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(create_channel.text).get('channel_id')
    assert create_channel.status_code == 200

    # Test valid channels_listall function and test create_channel created a channel
    channels_listall_test = requests.get(config.url + 'channels/listall/v2' + f'?token={token1}')
    assert json.loads(channels_listall_test.text).get('channels')[0]['channel_id'] == channel_id
    assert channels_listall_test.status_code == 200

    # Test valid channel_join and channel_invite function
    channel_invite_test = requests.post(config.url + 'channel/invite/v2', json={"token":token1,"channel_id":channel_id,"u_id":u_id2})
    assert channel_invite_test.status_code == 200
    channel_join_test = requests.post(config.url + 'channel/join/v2', json={"token":token3,"channel_id":channel_id})
    assert channel_join_test.status_code == 200

    # Test valid channels_list function and test user2 is in channel
    channels_list_test = requests.get(config.url + 'channels/list/v2' + f'?token={token2}')
    assert json.loads(channels_list_test.text).get('channels')[0]['channel_id'] == channel_id
    assert channels_list_test.status_code == 200

    # Test valid channel_details function and test user2 and user3 is in channel
    channel_details_test = requests.get(config.url + 'channel/details/v2' + f'?token={token3}&channel_id={channel_id}')
    assert channel_details_test.status_code == 200
    assert json.loads(channel_details_test.text).get('name') == "channelone"
    assert json.loads(channel_details_test.text).get('is_public') == True
    assert len(json.loads(channel_details_test.text).get('all_members')) == 3
    assert len(json.loads(channel_details_test.text).get('owner_members')) == 1

    # Test valid channel_addowner function
    channel_addowner_test = requests.post(config.url + 'channel/addowner/v1', json={"token":token1,"channel_id":channel_id,"u_id":u_id2})
    assert channel_addowner_test.status_code == 200
    details1 = requests.get(config.url + 'channel/details/v2' + f'?token={token1}&channel_id={channel_id}')
    assert len(json.loads(details1.text).get('owner_members')) == 2
    assert len(json.loads(details1.text).get('all_members')) == 3

    # Test valid channel_removeowner function
    channel_removeowner_test = requests.post(config.url + 'channel/removeowner/v1', json={"token":token1,"channel_id":channel_id,"u_id":u_id2})
    assert channel_removeowner_test.status_code == 200
    details2 = requests.get(config.url + 'channel/details/v2' + f'?token={token1}&channel_id={channel_id}')
    assert len(json.loads(details2.text).get('owner_members')) == 1
    assert len(json.loads(details2.text).get('all_members')) == 3

    # Test valid channel_leave function
    channel_leave_test = requests.post(config.url + 'channel/leave/v1', json={"token":token3,"channel_id":channel_id})
    assert channel_leave_test.status_code == 200
    details3 = requests.get(config.url + 'channel/details/v2' + f'?token={token1}&channel_id={channel_id}')
    assert len(json.loads(details3.text).get('owner_members')) == 1
    assert len(json.loads(details3.text).get('all_members')) == 2
    requests.delete(config.url + 'clear/v1')