import pytest
import requests
import json
from src import config
from src.data_file import Permission

"""
http server tests of user.py
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
    parameters = {"email": "haha1@gmail.com", "password": "123iwuiused", "name_first": "Lan", "name_last": "Lin"}
    return parameters


@pytest.fixture
def parameters2():
    parameters = {"email": "haha2@gmail.com", "password": "123iwuiused", "name_first": "Lan", "name_last": "Lin"}
    return parameters


#############################################################################
#                                                                           #
#                       http test for auth_profile Error                   #
#                                                                           #
#############################################################################


def test_user_profile_v1_inputError_http(parameters):
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', json=parameters)
    token = json.loads(resp.text).get('token')
    invalid_uid = -1
    status = requests.get(config.url + 'user/profile/v2', params={'token': token, 'u_id': invalid_uid}).status_code
    assert status == 400


def test_user_profile_v1_accessError_http():
    requests.delete(config.url + 'clear/v1')
    status = requests.get(config.url + 'user/profile/v2?token=invalid_token&u_id=0').status_code
    assert status == 403


#############################################################################
#                                                                           #
#                http test for user_profile_setname Error                   #
#                                                                           #
#############################################################################


def test_user_profile_setname_nameFirst_inputError_http(parameters):
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', json=parameters)
    token = json.loads(resp.text).get('token')
    new_input = {'token': token, 'name_first': '', 'name_last': 'Lan'}
    status = requests.put(config.url + 'user/profile/setname/v2', json=new_input).status_code
    assert status == 400


def test_user_profile_setname_nameLast_inputError_http(parameters):
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', json=parameters)
    token = json.loads(resp.text).get('token')
    new_input = {'token': token, 'name_first': 'Lin', 'name_last': ''}
    status = requests.put(config.url + 'user/profile/setname/v2', json=new_input).status_code
    assert status == 400


#############################################################################
#                                                                           #
#                http test for user_profile_setemail Error                   #
#                                                                           #
#############################################################################


def test_user_profile_setemail_invalid_email_http(parameters):
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', json=parameters)
    token = json.loads(resp.text).get('token')
    new_input = {'token': token, 'email': '123.com'}
    status = requests.put(config.url + 'user/profile/setemail/v2', json=new_input).status_code
    assert status == 400


def test_user_profile_setemail_duplicate_email_http(parameters):
    requests.delete(config.url + 'clear/v1')
    resp0 = requests.post(config.url + 'auth/register/v2', json=parameters)
    parameters1 = {
        "email": "haha1@gmail.com",
        "password": "12345ufd",
        "name_first": "Lan",
        "name_last": "Lin"
    }
    token = json.loads(resp0.text).get('token')
    requests.post(config.url + 'auth/register/v2', json=parameters1)

    new_input = {'token': token, 'email': 'haha1@gmail.com'}
    status = requests.put(config.url + 'user/profile/setemail/v2', json=new_input).status_code
    assert status == 400


#############################################################################
#                                                                           #
#                http test for user_profile_sethandle Error                   #
#                                                                           #
#############################################################################


def test_user_profile_sethandle_invalid_length_http(parameters):
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', json=parameters)
    token = json.loads(resp.text).get('token')
    new_input = {'token': token, 'handle_str': 'a'}
    status = requests.put(config.url + 'user/profile/sethandle/v1', json=new_input).status_code
    assert status == 400


def test_user_profile_sethandle_duplicate_handle_http(parameters):
    requests.delete(config.url + 'clear/v1')
    resp0 = requests.post(config.url + 'auth/register/v2', json=parameters)
    token0 = json.loads(resp0.text).get('token')
    users_all = requests.get(config.url + 'users/all/v1', params={'token': token0})
    handle0 = json.loads(users_all.text).get('users')[0]['handle_str']

    parameters1 = {
        "email": "haha1@gmail.com",
        "password": "12345ufd",
        "name_first": "Lan",
        "name_last": "Lin"
    }
    resp1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    token1 = json.loads(resp1.text).get('token')

    new_input = {'token': token1, 'handle_str': handle0}
    status = requests.put(config.url + 'user/profile/sethandle/v1', json=new_input).status_code
    assert status == 400


#############################################################################
#                                                                           #
#                  http test for admin_user_remover Error                   #
#                                                                           #
#############################################################################


def test_admin_user_remover_only_owner_error_http(parameters):
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', json=parameters)
    token = json.loads(resp.text).get('token')
    status = requests.delete(config.url + 'admin/user/remove/v1', json={'token': token, 'u_id': 0}).status_code
    assert status == 400


def test_admin_user_remover_invalid_uid_http(parameters):
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', json=parameters)
    token0 = json.loads(resp.text).get('token')

    parameters['email'] = f"haha1@gmail.com"
    requests.post(config.url + 'auth/register/v2', json=parameters)
    uid1 = json.loads(resp.text).get('auth_user_id')
    invalid_uid = uid1 + 100

    status = requests.delete(config.url + 'admin/user/remove/v1',
                             json={'token': token0, 'u_id': invalid_uid}).status_code
    assert status == 400


def test_admin_user_remover_accessError_http(parameters):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=parameters)

    parameters['email'] = f"hah@gmail.com"
    resp1 = requests.post(config.url + 'auth/register/v2', json=parameters)
    token1 = json.loads(resp1.text).get('token')

    parameters['email'] = f"fafa@gmail.com"
    resp2 = requests.post(config.url + 'auth/register/v2', json=parameters)
    uid2 = json.loads(resp2.text).get('auth_user_id')

    status = requests.delete(config.url + 'admin/user/remove/v1', json={'token': token1, 'u_id': uid2}).status_code
    assert status == 403


#############################################################################
#                                                                           #
#                  http test for admin_user_remover Error                   #
#                                                                           #
#############################################################################


def test_admin_user_permission_invalid_uid_http(parameters):
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', json=parameters)
    token0 = json.loads(resp.text).get('token')

    parameters['email'] = f"haha1@gmail.com"
    requests.post(config.url + 'auth/register/v2', json=parameters)
    uid1 = json.loads(resp.text).get('auth_user_id')
    invalid_uid = uid1 + 100

    status = requests.post(config.url + 'admin/userpermission/change/v1',
                           json={'token': token0, 'u_id': invalid_uid, 'permission_id': Permission.global_owner}).status_code
    assert status == 400


def test_admin_user_permission_invalid_permission_http(parameters):
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', json=parameters)
    token0 = json.loads(resp.text).get('token')

    parameters['email'] = f"haha1@gmail.com"
    requests.post(config.url + 'auth/register/v2', json=parameters)
    uid1 = json.loads(resp.text).get('auth_user_id')

    status = requests.post(config.url + 'admin/userpermission/change/v1',
                           json={'token': token0, 'u_id': uid1, 'permission_id': 3}).status_code
    assert status == 400


def test_admin_user_permission_change_accessError_http(parameters):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=parameters)

    parameters['email'] = f"hah@gmail.com"
    resp1 = requests.post(config.url + 'auth/register/v2', json=parameters)
    token1 = json.loads(resp1.text).get('token')

    parameters['email'] = f"fafa@gmail.com"
    resp2 = requests.post(config.url + 'auth/register/v2', json=parameters)
    uid2 = json.loads(resp2.text).get('auth_user_id')

    status = requests.post(config.url + 'admin/userpermission/change/v1',
                           json={'token': token1, 'u_id': uid2, 'permission_id': Permission.global_owner}).status_code
    assert status == 403


#############################################################################
#                                                                           #
#                http test for user.py successfully                         #
#                                                                           #
#############################################################################


def test_user_profile_setname_valid_http(parameters):
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', json=parameters)
    token = json.loads(resp.text).get('token')
    u_id = json.loads(resp.text).get('auth_user_id')
    new_input = {'token': token, 'name_first': 'Linlin', 'name_last': 'Lanlan'}
    status = requests.put(config.url + 'user/profile/setname/v2', json=new_input).status_code
    assert status == 200

    user_profile = requests.get(config.url + 'user/profile/v2?token=' + token + '&u_id=' + str(u_id))
    new_name_first = json.loads(user_profile.text)['user']['name_first']
    new_name_last = json.loads(user_profile.text)['user']['name_last']
    assert new_name_first == 'Linlin'
    assert new_name_last == 'Lanlan'


def test_user_profile_setemail_valid_http(parameters):
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', json=parameters)
    token = json.loads(resp.text).get('token')
    u_id = json.loads(resp.text).get('auth_user_id')
    new_input = {'token': token, 'email': 'haha3@gmail.com'}
    status = requests.put(config.url + 'user/profile/setemail/v2', json=new_input).status_code
    assert status == 200
    user_profile = requests.get(config.url + 'user/profile/v2?token=' + token + '&u_id=' + str(u_id))
    new_email = json.loads(user_profile.text)['user']['email']
    assert new_email == 'haha3@gmail.com'


def test_user_profile_sethandle_valid_http(parameters):
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', json=parameters)
    token = json.loads(resp.text).get('token')
    u_id = json.loads(resp.text).get('auth_user_id')
    new_input = {'token': token, 'handle_str': 'tomgreen'}
    status = requests.put(config.url + 'user/profile/sethandle/v1', json=new_input).status_code
    assert status == 200
    user_profile = requests.get(config.url + 'user/profile/v2?token=' + token + '&u_id=' + str(u_id))
    new_handle = json.loads(user_profile.text)['user']['handle_str']
    assert new_handle == 'tomgreen'


def test_users_all_admin_remove_user_valid(parameters):
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', json=parameters)
    token = json.loads(resp.text).get('token')
    resp_n = None
    for i in range(10):
        parameters['email'] = f"haha{i}@gmail.com"
        resp_n = requests.post(config.url + 'auth/register/v2', json=parameters)

    token_n = json.loads(resp_n.text).get('token')
    uid_n = json.loads(resp_n.text).get('auth_user_id')

    resp_users_all = requests.get(config.url + 'users/all/v1?token=' + token)
    users_all_list = json.loads(resp_users_all.text)['users']
    assert len(users_all_list) == 11
    status = requests.delete(config.url + 'admin/user/remove/v1', json={'token': token, 'u_id': 10}).status_code
    assert status == 200
    user_profile = requests.get(config.url + 'user/profile/v2?token=' + token_n + '&u_id=' + str(uid_n))
    name_first = json.loads(user_profile.text)['user']['name_first']
    name_last = json.loads(user_profile.text)['user']['name_last']
    assert f"{name_first} {name_last}" == 'Removed user'


def test_admin_user_permission_change_invalid_http(parameters):
    requests.delete(config.url + 'clear/v1')
    resp0 = requests.post(config.url + 'auth/register/v2', json=parameters)
    token0 = json.loads(resp0.text).get('token')

    parameters['email'] = f"hah@gmail.com"
    resp1 = requests.post(config.url + 'auth/register/v2', json=parameters)
    token1 = json.loads(resp1.text).get('token')
    uid1 = json.loads(resp1.text).get('auth_user_id')

    parameters['email'] = f"fafa@gmail.com"
    resp2 = requests.post(config.url + 'auth/register/v2', json=parameters)
    uid2 = json.loads(resp2.text).get('auth_user_id')

    status1 = requests.post(config.url + 'admin/userpermission/change/v1',
                            json={'token': token0, 'u_id': uid1, 'permission_id': Permission.global_owner}).status_code
    assert status1 == 200

    status2 = requests.post(config.url + 'admin/userpermission/change/v1',
                            json={'token': token1, 'u_id': uid2, 'permission_id': Permission.global_owner}).status_code
    assert status2 == 200
#############################################################################
#                                                                           #
#                  http test for user_stats                                 #
#                                                                           #
#############################################################################


def test_user_stats(parameters, parameters1):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + "auth/register/v2", json=parameters)
    user1 = requests.post(config.url + "auth/register/v2", json=parameters1)
    token0 = json.loads(user0.text).get("token")
    token1 = json.loads(user1.text).get("token")
    uid1 = json.loads(user1.text).get("auth_user_id")

    def test_zero_involvement_rate():
        user_stat = requests.get(config.url + "user/stats/v1", params={'token': token0})
        rate = json.loads(user_stat.text).get("user_stats")
        assert rate['involvement_rate'] == 0
    # ----------------------------testing------------------------------------
    test_zero_involvement_rate()
    # ------------------------------------------------------------------------
    dm_info = requests.post(config.url + 'dm/create/v1', json={'token': token0, 'u_ids': [uid1]})
    dm_id = json.loads(dm_info.text).get('dm_id')
    channel = requests.post(config.url + 'channels/create/v2',
                            json={"token": token1, "name": "channelone", "is_public": True})
    channel_id = json.loads(channel.text).get('channel_id')

    requests.post(config.url + "message/senddm/v1", json={'token': token0, 'dm_id': dm_id, 'message': "haha"})
    for _i in range(2):
        requests.post(config.url + "message/send/v2", json={'token': token1, 'channel_id': channel_id, 'message': "haha"})

    def test_invalid_token_user_stats():
        input1 = {"token": "string token"}
        input2 = {"token": 111000}
        input3 = {"token": None}

        user_stat0 = requests.get(config.url + "user/stats/v1", params=input1)
        user_stat1 = requests.get(config.url + "user/stats/v1", params=input2)
        user_stat2 = requests.get(config.url + "user/stats/v1", params=input3)

        assert user_stat0.status_code == 403
        assert user_stat1.status_code == 403
        assert user_stat2.status_code == 403

    def test_valid1():
        user_stat0 = requests.get(config.url + "user/stats/v1", params={'token': token0})
        user0_stats = json.loads(user_stat0.text).get('user_stats')
        user_stat1 = requests.get(config.url + "user/stats/v1", params={'token': token1})
        user1_stats = json.loads(user_stat1.text).get('user_stats')
        assert len(user0_stats['channels_joined']) == 0
        assert len(user0_stats['dms_joined']) == 1
        assert len(user0_stats['messages_sent']) == 1
        assert user0_stats['involvement_rate'] == 2 / 5
        assert len(user1_stats['channels_joined']) == 1
        assert len(user1_stats['dms_joined']) == 1
        assert len(user1_stats['messages_sent']) == 2
        assert user1_stats['involvement_rate'] == 4 / 5
    # ----------------------------testing------------------------------------
    test_invalid_token_user_stats()
    test_valid1()
    # -----------------------------------------------------------------------
    for _i in range(3):
        requests.post(config.url + "message/senddm/v1", json={'token': token0, 'dm_id': dm_id, 'message': "haha"})

    def test_valid2():
        user_stat0 = requests.get(config.url + "user/stats/v1", params={'token': token0})
        user0_stats = json.loads(user_stat0.text).get('user_stats')
        assert len(user0_stats['messages_sent']) == 4
        assert user0_stats['involvement_rate'] == 5 / 8
    # ----------------------------testing------------------------------------
    test_valid2()
#############################################################################
#                                                                           #
#                        Test for users_stats_v1                             #
#                                                                           #
#############################################################################


def test_users_stats_v1(parameters, parameters1, parameters2):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + "auth/register/v2", json=parameters)
    user1 = requests.post(config.url + "auth/register/v2", json=parameters1)
    user2 = requests.post(config.url + "auth/register/v2", json=parameters2)
    token0 = json.loads(user0.text).get("token")
    token1 = json.loads(user1.text).get("token")
    uid1 = json.loads(user1.text).get("auth_user_id")
    uid2 = json.loads(user2.text).get("auth_user_id")

    dm_info = requests.post(config.url + 'dm/create/v1', json={'token': token0, 'u_ids': [uid1]})
    dm_id = json.loads(dm_info.text).get('dm_id')

    channel = requests.post(config.url + 'channels/create/v2',
                            json={"token": token1, "name": "channelone", "is_public": True})
    channel_id = json.loads(channel.text).get('channel_id')
    requests.post(config.url + 'channels/create/v2',
                  json={"token": token1, "name": "channeltwo", "is_public": True})

    requests.post(config.url + "message/senddm/v1", json={'token': token0, 'dm_id': dm_id, 'message': "haha"})

    message_id1 = requests.post(config.url + "message/send/v2", json={'token': token1, 'channel_id': channel_id,
                                                                      'message': "haha"})
    message_id1 = json.loads(message_id1.text).get('message_id')
    requests.post(config.url + "message/send/v2", json={'token': token1, 'channel_id': channel_id,
                                                        'message': "haha"})

    def test_invalid_token_users_stats():
        input1 = {"token": "string token"}
        input2 = {"token": 111000}
        input3 = {"token": None}

        user_stat0 = requests.get(config.url + "users/stats/v1", params=input1)
        user_stat1 = requests.get(config.url + "users/stats/v1", params=input2)
        user_stat2 = requests.get(config.url + "users/stats/v1", params=input3)

        assert user_stat0.status_code == 403
        assert user_stat1.status_code == 403
        assert user_stat2.status_code == 403

    def test_valid1():
        dreams_stats = requests.get(config.url + "users/stats/v1", params={'token': token0})
        dreams_stats = json.loads(dreams_stats.text)['dreams_stats']
        assert len(dreams_stats['channels_exist']) == 2
        assert len(dreams_stats['dms_exist']) == 1
        assert len(dreams_stats['messages_exist']) == 3
        assert dreams_stats['utilization_rate'] == 2 / 3
    # ----------------------------testing------------------------------------
    test_invalid_token_users_stats()
    test_valid1()
    # -----------------------------------------------------------------------
    requests.delete(config.url + "message/remove/v1", json={"token": token1, "message_id": message_id1})
    requests.delete(config.url + 'admin/user/remove/v1', json={'token': token0, 'u_id': uid2})

    def test_valid2():
        dreams_stats = requests.get(config.url + "users/stats/v1", params={'token': token0})
        dreams_stats = json.loads(dreams_stats.text)['dreams_stats']
        assert len(dreams_stats['messages_exist']) == 4
        assert dreams_stats['utilization_rate'] == 1
    # ----------------------------testing------------------------------------
    test_valid2()
#############################################################################
#                                                                           #
#                        Test for user_profile_uploadphoto_v1               #
#                                                                           #
#############################################################################


def user_profile_uploadphoto_v1_http(parameters):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + "auth/register/v2", json=parameters)
    token0 = json.loads(user0.text).get("token")
    uid0 = json.loads(user0.text).get("auth_user_id")
    url = 'https://static.boredpanda.com/blog/wp-content/uploads/2020/05/700-1.jpg'

    def test_invalid_token1():
        input1 = {"token": "string token", "img_url": url, "x_start": 0, "y_start": 0, "x_end": 50, "y_end": 50}
        input2 = {"token": 1110000, "img_url": url, "x_start": 0, "y_start": 0, "x_end": 50, "y_end": 50}
        input3 = {"token": None, "img_url": url, "x_start": 0, "y_start": 0, "x_end": 50, "y_end": 50}

        respond1 = requests.post(config.url + "user/profile/uploadphoto/v1", json=input1)
        respond2 = requests.get(config.url + "user/profile/uploadphoto/v1", json=input2)
        respond3 = requests.get(config.url + "user/profile/uploadphoto/v1", json=input3)

        assert respond1.status_code == 403
        assert respond2.status_code == 403
        assert respond3.status_code == 403

    def test_invalid_url():
        input1 = {"token": token0, "img_url": "http://haha", "x_start": 0, "y_start": 0, "x_end": 50, "y_end": 50}

        respond = requests.post(config.url + "user/profile/uploadphoto/v1", json=input1)
        assert respond.status_code == 400

    def test_invalid_image_format():
        input1 = {"token": token0, "img_url": 'https://pngimg.com/uploads/mario/mario_PNG53.png', "x_start": 0,
                  "y_start": 0, "x_end": 50, "y_end": 50}

        respond = requests.post(config.url + "user/profile/uploadphoto/v1", json=input1)
        assert respond.status_code == 400

    def test_invalid_x_bound():
        input1 = {"token": token0, "img_url": url, "x_start": 50, "y_start": 0, "x_end": 0, "y_end": 50}

        respond = requests.post(config.url + "user/profile/uploadphoto/v1", json=input1)
        assert respond.status_code == 400

    def test_invalid_y_bound():
        input1 = {"token": token0, "img_url": url, "x_start": 0, "y_start": 50, "x_end": 50, "y_end": 0}

        respond = requests.post(config.url + "user/profile/uploadphoto/v1", json=input1)
        assert respond.status_code == 400

    def test_valid():
        user_profile_start = requests.get(config.url + 'user/profile/v2', params={'token': token0, 'u_id': uid0})
        img_url1 = json.loads(user_profile_start.text)['profile_img_url']

        input1 = {"token": token0, "img_url": url, "x_start": 0, "y_start": 0, "x_end": 50, "y_end": 50}
        requests.post(config.url + "user/profile/uploadphoto/v1", json=input1)

        requests.get(config.url + 'user/profile/v2', params={'token': token0, 'u_id': uid0})
        img_url = json.loads(user_profile_start.text)['profile_img_url']

        assert img_url1 != img_url
        assert img_url == 'http://127.0.0.1:8080/static/' + str(uid0) + '.jpg'
    # ----------------------------testing------------------------------------
    test_invalid_token1()
    test_invalid_url()
    test_invalid_image_format()
    test_invalid_x_bound()
    test_invalid_y_bound()
    test_valid()
    requests.delete(config.url + 'clear/v1')
