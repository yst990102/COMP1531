from datetime import datetime, timezone
from os import stat
import pytest
import requests
import json
from src import config

"""
http server tests of message.py
Auther: Lan Lin
"""


@pytest.fixture
def parameters():
    parameters = {"email": "haha@gmail.com", "password": "123iwuiused", "name_first": "Lan", "name_last": "Lin"}
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
#                       http test for message_send Error                    #
#                                                                           #
#############################################################################

def test_message_send_invalid_length_http(parameters):
    requests.delete(config.url + "clear/v1")
    user = requests.post(config.url + "auth/register/v2", json=parameters)
    token = json.loads(user.text).get("token")
    json_input1 = {"token": token, "name": "channel0", "is_public": True}
    channel = requests.post(config.url + "channels/create/v2", json=json_input1)
    channel_id = json.loads(channel.text).get("channel_id")

    msg = "a" * 1005
    json_input2 = {"token": token, "channel_id": channel_id, "message": msg}
    status = requests.post(config.url + "message/send/v2", json=json_input2).status_code
    assert status == 400


def test_message_send_not_join_http(parameters, parameters1):
    requests.delete(config.url + "clear/v1")
    user0 = requests.post(config.url + "auth/register/v2", json=parameters)
    token0 = json.loads(user0.text).get("token")
    user1 = requests.post(config.url + "auth/register/v2", json=parameters1)
    token1 = json.loads(user1.text).get("token")

    json_input1 = {"token": token0, "name": "channel0", "is_public": True}
    channel = requests.post(config.url + "channels/create/v2", json=json_input1)
    channel_id = json.loads(channel.text).get("channel_id")

    json_input2 = {"token": token1, "channel_id": channel_id, "message": "haha"}
    status = requests.post(config.url + "message/send/v2", json=json_input2).status_code
    assert status == 403

#############################################################################
#                                                                           #
#                       http test for message_edit Error                    #
#                                                                           #
#############################################################################


def test_message_edit_deleted_msg_http(parameters):
    requests.delete(config.url + "clear/v1")
    user = requests.post(config.url + "auth/register/v2", json=parameters)
    token = json.loads(user.text).get("token")
    json_input1 = {"token": token, "name": "channel0", "is_public": True}
    channel = requests.post(config.url + "channels/create/v2", json=json_input1)
    channel_id = json.loads(channel.text).get("channel_id")

    json_input2 = {"token": token, "channel_id": channel_id, "message": "first"}
    msg_id = requests.post(config.url + "message/send/v2", json=json_input2)
    message_id = json.loads(msg_id.text).get("message_id")

    requests.delete(config.url + "message/remove/v1", json={"token": token, "message_id": message_id})
    json_input3 = {"token": token, "message_id": message_id, "message": "second"}
    status = requests.put(config.url + "message/edit/v2", json=json_input3).status_code
    assert status == 400


def test_message_edit_accessError(parameters, parameters1):
    requests.delete(config.url + "clear/v1")
    user0 = requests.post(config.url + "auth/register/v2", json=parameters)
    token0 = json.loads(user0.text).get("token")
    user1 = requests.post(config.url + "auth/register/v2", json=parameters1)
    token1 = json.loads(user1.text).get("token")

    json_input1 = {"token": token0, "name": "channel0", "is_public": True}
    channel = requests.post(config.url + "channels/create/v2", json=json_input1)
    channel_id = json.loads(channel.text).get("channel_id")
    st = requests.post(config.url + "channel/join/v2", json={"token": token1, "channel_id": channel_id}).status_code
    assert st == 200

    json_input2 = {"token": token0, "channel_id": channel_id, "message": "haha"}
    msg_id = requests.post(config.url + "message/send/v2", json=json_input2)
    message_id = json.loads(msg_id.text).get("message_id")

    json_input3 = {"token": token1, "message_id": message_id, "message": "heihei"}
    status = requests.put(config.url + "message/edit/v2", json=json_input3).status_code
    assert status == 403

#############################################################################
#                                                                           #
#                     http test for message_remove Error                    #
#                                                                           #
#############################################################################


def test_message_remove_invalid_msg_id(parameters):
    requests.delete(config.url + "clear/v1")
    user = requests.post(config.url + "auth/register/v2", json=parameters)
    token = json.loads(user.text).get("token")
    json_input1 = {"token": token, "name": "channel0", "is_public": True}
    requests.post(config.url + "channels/create/v2", json=json_input1)

    json_input2 = {"token": token, "message_id": "haha"}
    status = requests.delete(config.url + "message/remove/v1", json=json_input2).status_code
    assert status == 400


def test_message_remove_accessError(parameters, parameters1):
    requests.delete(config.url + "clear/v1")
    user0 = requests.post(config.url + "auth/register/v2", json=parameters)
    token0 = json.loads(user0.text).get("token")
    user1 = requests.post(config.url + "auth/register/v2", json=parameters1)
    token1 = json.loads(user1.text).get("token")

    json_input1 = {"token": token0, "name": "channel0", "is_public": True}
    channel = requests.post(config.url + "channels/create/v2", json=json_input1)
    channel_id = json.loads(channel.text).get("channel_id")
    requests.post(config.url + "channel/join/v2", json={"token": token1, "channel_id": channel_id})

    json_input2 = {"token": token0, "channel_id": channel_id, "message": "haha"}
    requests.post(config.url + "message/send/v2", json=json_input2)
    msg_id = requests.post(config.url + "message/send/v2", json=json_input2)
    message_id = json.loads(msg_id.text).get("message_id")

    json_input3 = {"token": token1, "message_id": message_id}
    status = requests.delete(config.url + "message/remove/v1", json=json_input3).status_code
    assert status == 403

#############################################################################
#                                                                           #
#                      http test for message_share Error                    #
#                                                                           #
#############################################################################


def test_message_share_not_join_http(parameters, parameters1):
    requests.delete(config.url + "clear/v1")
    user0 = requests.post(config.url + "auth/register/v2", json=parameters)
    token0 = json.loads(user0.text).get("token")
    user1 = requests.post(config.url + "auth/register/v2", json=parameters1)
    token1 = json.loads(user1.text).get("token")

    json_input1 = {"token": token0, "name": "channel0", "is_public": True}
    channel = requests.post(config.url + "channels/create/v2", json=json_input1)
    channel_id = json.loads(channel.text).get("channel_id")

    json_input2 = {"token": token0, "channel_id": channel_id, "message": "haha"}
    requests.post(config.url + "message/send/v2", json=json_input2)
    msg_id = requests.post(config.url + "message/send/v2", json=json_input2)
    og_message_id = json.loads(msg_id.text).get("message_id")
    json_input3 = {"token": token1, "og_message_id": og_message_id, "message": "good", "channel_id": channel_id, "dm_id": -1}
    status = requests.post(config.url + "message/share/v1", json=json_input3).status_code
    assert status == 403

#############################################################################
#                                                                           #
#                       http test for message_senddm Error                  #
#                                                                           #
#############################################################################


def test_message_senddm_invalid_length_http(parameters):
    requests.delete(config.url + "clear/v1")
    user0 = requests.post(config.url + "auth/register/v2", json=parameters)
    token0 = json.loads(user0.text).get("token")
    user1 = requests.post(config.url + "auth/register/v2", json=parameters)
    uid1 = json.loads(user1.text).get("auth_user_id")
    json_input1 = {"token": token0, "u_ids": [uid1]}
    dm = requests.post(config.url + "dm/create/v1", json=json_input1)
    dm_id = json.loads(dm.text).get("dm_id")

    msg = "a" * 1005
    json_input2 = {"token": token0, "dm_id": dm_id, "message": msg}
    status = requests.post(config.url + "message/senddm/v1", json=json_input2).status_code
    assert status == 400


def test_message_senddm_not_join_http(parameters, parameters1, parameters2):
    requests.delete(config.url + "clear/v1")
    user0 = requests.post(config.url + "auth/register/v2", json=parameters)
    token0 = json.loads(user0.text).get("token")
    user1 = requests.post(config.url + "auth/register/v2", json=parameters1)
    uid1 = json.loads(user1.text).get("auth_user_id")
    user2 = requests.post(config.url + "auth/register/v2", json=parameters2)
    token2 = json.loads(user2.text).get("token")

    json_input1 = {"token": token0, "u_ids": [uid1]}
    dm = requests.post(config.url + "dm/create/v1", json=json_input1)
    dm_id = json.loads(dm.text).get("dm_id")

    json_input2 = {"token": token2, "dm_id": dm_id, "message": "haha"}
    status = requests.post(config.url + "message/senddm/v1", json=json_input2).status_code
    assert status == 403


#############################################################################
#                                                                           #
#                       http test for message successfully                  #
#                                                                           #
#############################################################################
"""
successful tests for message_send, message_senddm, message_edit,
message_remove, message_share, channel_messages, dm_messages
"""


def test_message_valid_http(parameters, parameters1, parameters2):
    requests.delete(config.url + "clear/v1")
    user0 = requests.post(config.url + "auth/register/v2", json=parameters)
    token0 = json.loads(user0.text).get("token")
    user1 = requests.post(config.url + "auth/register/v2", json=parameters1)
    uid1 = json.loads(user1.text).get("auth_user_id")
    user2 = requests.post(config.url + "auth/register/v2", json=parameters2)
    token2 = json.loads(user2.text).get("token")

    # create a dm, users in dm are user0, 1
    json_input1 = {"token": token0, "u_ids": [uid1]}
    dm = requests.post(config.url + "dm/create/v1", json=json_input1)
    dm_id = json.loads(dm.text).get("dm_id")

    # create a channel by user2
    json_input2 = {"token": token2, "name": "channel0", "is_public": True}
    channel = requests.post(config.url + "channels/create/v2", json=json_input2)
    channel_id = json.loads(channel.text).get("channel_id")

    # send a message to the dm
    json_input3 = {"token": token0, "dm_id": dm_id, "message": "haha0"}
    requests.post(config.url + "message/senddm/v1", json=json_input3)

    # check the message in the dm
    dm_msg = requests.get(config.url + "dm/messages/v1?token=" + token0 + "&dm_id=" + str(dm_id) + "&start=0")
    dm_msg = json.loads(dm_msg.text).get("messages")[0]
    assert dm_msg["message"] == "haha0"
    message_id = dm_msg["message_id"]

    # edit the message in the dm
    # check the edited message in the dm
    json_input7 = {"token": token0, "message_id": message_id, "message": "haha1"}
    requests.put(config.url + "message/edit/v2", json=json_input7)
    dm_msg = requests.get(config.url + "dm/messages/v1?token=" + token0 + "&dm_id=" + str(dm_id) + "&start=0")
    dm_msg = json.loads(dm_msg.text).get("messages")[0]
    assert dm_msg["message"] == "haha1"

    # remove the message in the dm
    json_input8 = {"token": token0, "message_id": message_id}
    requests.delete(config.url + "message/remove/v1", json=json_input8)
    # check that the message has been removed
    dm_msg = requests.get(config.url + "dm/messages/v1?token=" + token0 + "&dm_id=" + str(dm_id) + "&start=0")
    dm_msg = json.loads(dm_msg.text).get("messages")
    assert len(dm_msg) == 0

    # send 60 messages to the channel
    for _i in range(60):
        json_input4 = {"token": token2, "channel_id": channel_id, "message": f"good{_i}"}
        requests.post(config.url + "message/send/v2", json=json_input4)

    # check if the message are sent successfully
    channel_msg = requests.get(config.url + "channel/messages/v2?token=" + token2 + "&channel_id=" + str(channel_id) + "&start=5")
    channel_msg = json.loads(channel_msg.text)
    message_list = channel_msg.get("messages")
    start = channel_msg.get("start")
    end = channel_msg.get("end")
    assert message_list[0]["message"] == "good54"
    assert len(message_list) == 50
    assert start == 5
    assert end == 55

    # share the first message in the channel to the dm
    json_input9 = {"token": token0, "og_message_id": 1, "message": "this is comment", "channel_id": -1, "dm_id": 0}
    assert requests.post(config.url + "message/share/v1", json=json_input9).status_code == 200
    # check if the message has been shared successfully
    dm_msg = requests.get(config.url + "dm/messages/v1?token=" + token0 + "&dm_id=" + str(dm_id) + "&start=0")
    dm_msg = json.loads(dm_msg.text).get("messages")[0]["message"]
    correct = "this is comment" '"""' "good0" '"""'
    assert dm_msg == correct


#############################################################################
#                                                                           #
#                    http test for message_sendlater Error                  #
#                                                                           #
#############################################################################


def test_message_sendlater(parameters, parameters1, parameters2):
    requests.delete(config.url + "clear/v1")
    user0 = requests.post(config.url + "auth/register/v2", json=parameters)
    user1 = requests.post(config.url + "auth/register/v2", json=parameters1)
    user2 = requests.post(config.url + "auth/register/v2", json=parameters2)

    token_0 = json.loads(user0.text).get("token")
    json.loads(user1.text).get("token")
    token_2 = json.loads(user2.text).get("token")

    json.loads(user0.text).get("auth_user_id")
    u_id_1 = json.loads(user1.text).get("auth_user_id")
    json.loads(user2.text).get("auth_user_id")

    channel = requests.post(config.url + "channels/create/v2", json={"token": token_0, "name": "channel_0", "is_public": True})
    channel_0_id = json.loads(channel.text).get("channel_id")
    requests.post(config.url + "channel/invite/v2", json={"token": token_0, "channel_id": channel_0_id, "u_id": u_id_1})

    time_sent = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()) + 1

    def test_invalid_token():
        input1 = {"token": "string token", "channel_id": channel_0_id, "message": "I am message.", "time_sent": time_sent}
        input2 = {"token": 111000, "channel_id": channel_0_id, "message": "I am message.", "time_sent": time_sent}
        input3 = {"token": None, "channel_id": channel_0_id, "message": "I am message.", "time_sent": time_sent}

        status1 = requests.post(config.url + "message/sendlater/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/sendlater/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/sendlater/v1", json=input3).status_code

        assert status1 == 403
        assert status2 == 403
        assert status3 == 403

    def test_invalid_channel_id():
        input1 = {"token": token_0, "channel_id": "invalid channel_id", "message": "I am message.", "time_sent": time_sent}
        input2 = {"token": token_0, "channel_id": 99999, "message": "I am message.", "time_sent": time_sent}
        input3 = {"token": token_0, "channel_id": None, "message": "I am message.", "time_sent": time_sent}

        status1 = requests.post(config.url + "message/sendlater/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/sendlater/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/sendlater/v1", json=input3).status_code

        assert status1 == 400
        assert status2 == 400
        assert status3 == 400

    def test_invalid_message():
        input1 = {"token": token_0, "channel_id": channel_0_id, "message": 123456, "time_sent": time_sent}
        input2 = {"token": token_0, "channel_id": channel_0_id, "message": "a" * 2000, "time_sent": time_sent}
        input3 = {"token": token_0, "channel_id": channel_0_id, "message": None, "time_sent": time_sent}

        status1 = requests.post(config.url + "message/sendlater/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/sendlater/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/sendlater/v1", json=input3).status_code

        assert status1 == 400
        assert status2 == 400
        assert status3 == 400

    def test_invalid_time_sent():
        past_time_sent = datetime(1999, 1, 2).replace(tzinfo=timezone.utc).timestamp()
        input1 = {"token": token_0, "channel_id": channel_0_id, "message": "I am message.", "time_sent": "string time_sent"}
        input2 = {"token": token_0, "channel_id": channel_0_id, "message": "I am message.", "time_sent": 123456}
        input3 = {"token": token_0, "channel_id": channel_0_id, "message": "I am message.", "time_sent": None}
        input4 = {"token": token_0, "channel_id": channel_0_id, "message": "I am message.", "time_sent": past_time_sent}

        status1 = requests.post(config.url + "message/sendlater/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/sendlater/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/sendlater/v1", json=input3).status_code
        status4 = requests.post(config.url + "message/sendlater/v1", json=input4).status_code

        assert status1 == 400
        assert status2 == 400
        assert status3 == 400
        assert status4 == 400

    def test_user_isnot_member_of_channel():
        input1 = {"token": token_2, "channel_id": channel_0_id, "message": "I am message.", "time_sent": time_sent}

        status1 = requests.post(config.url + "message/sendlater/v1", json=input1).status_code

        assert status1 == 403

    # ----------------------------testing------------------------------------
    # InputError Tests
    test_invalid_channel_id()
    test_invalid_message()
    test_invalid_time_sent()

    # AccessError Tests
    test_invalid_token()

    test_user_isnot_member_of_channel()


#############################################################################
#                                                                           #
#                  http test for message_sendlaterdm Error                  #
#                                                                           #
#############################################################################
def test_message_sendlaterdm(parameters, parameters1, parameters2):
    requests.delete(config.url + "clear/v1")
    user0 = requests.post(config.url + "auth/register/v2", json=parameters)
    user1 = requests.post(config.url + "auth/register/v2", json=parameters1)
    user2 = requests.post(config.url + "auth/register/v2", json=parameters2)

    token_0 = json.loads(user0.text).get("token")
    json.loads(user1.text).get("token")
    token_2 = json.loads(user2.text).get("token")

    json.loads(user0.text).get("auth_user_id")
    u_id_1 = json.loads(user1.text).get("auth_user_id")
    json.loads(user2.text).get("auth_user_id")

    dm = requests.post(config.url + "dm/create/v1", json={"token": token_0, "u_ids": [u_id_1]})
    dm_0_id = json.loads(dm.text).get("dm_id")

    time_sent = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()) + 5

    def test_invalid_token():
        input1 = {"token": "string token", "dm_id": dm_0_id, "message": "I am message.", "time_sent": time_sent}
        input2 = {"token": 111000, "dm_id": dm_0_id, "message": "I am message.", "time_sent": time_sent}
        input3 = {"token": None, "dm_id": dm_0_id, "message": "I am message.", "time_sent": time_sent}

        status1 = requests.post(config.url + "message/sendlaterdm/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/sendlaterdm/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/sendlaterdm/v1", json=input3).status_code

        assert status1 == 403
        assert status2 == 403
        assert status3 == 403

    def test_invalid_dm_id():
        input1 = {"token": token_0, "dm_id": "invalid channel_id", "message": "I am message.", "time_sent": time_sent}
        input2 = {"token": token_0, "dm_id": 99999, "message": "I am message.", "time_sent": time_sent}
        input3 = {"token": token_0, "dm_id": None, "message": "I am message.", "time_sent": time_sent}

        status1 = requests.post(config.url + "message/sendlaterdm/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/sendlaterdm/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/sendlaterdm/v1", json=input3).status_code

        assert status1 == 400
        assert status2 == 400
        assert status3 == 400

    def test_invalid_message():
        input1 = {"token": token_0, "dm_id": dm_0_id, "message": 123456, "time_sent": time_sent}
        input2 = {"token": token_0, "dm_id": dm_0_id, "message": "a" * 2000, "time_sent": time_sent}
        input3 = {"token": token_0, "dm_id": dm_0_id, "message": None, "time_sent": time_sent}

        status1 = requests.post(config.url + "message/sendlaterdm/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/sendlaterdm/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/sendlaterdm/v1", json=input3).status_code

        assert status1 == 400
        assert status2 == 400
        assert status3 == 400

    def test_invalid_time_sent():
        past_time_sent = datetime(1999, 1, 2).replace(tzinfo=timezone.utc).timestamp()
        input1 = {"token": token_0, "dm_id": dm_0_id, "message": "I am message.", "time_sent": "string time_sent"}
        input2 = {"token": token_0, "dm_id": dm_0_id, "message": "I am message.", "time_sent": 123456}
        input3 = {"token": token_0, "dm_id": dm_0_id, "message": "I am message.", "time_sent": None}
        input4 = {"token": token_0, "dm_id": dm_0_id, "message": "I am message.", "time_sent": past_time_sent}

        status1 = requests.post(config.url + "message/sendlaterdm/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/sendlaterdm/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/sendlaterdm/v1", json=input3).status_code
        status4 = requests.post(config.url + "message/sendlaterdm/v1", json=input4).status_code

        assert status1 == 400
        assert status2 == 400
        assert status3 == 400
        assert status4 == 400

    def test_user_isnot_member_of_dm():
        input1 = {"token": token_2, "dm_id": dm_0_id, "message": "I am message.", "time_sent": time_sent}

        status1 = requests.post(config.url + "message/sendlaterdm/v1", json=input1).status_code

        assert status1 == 403

    # ----------------------------testing------------------------------------
    # InputError Tests
    test_invalid_dm_id()
    test_invalid_message()
    test_invalid_time_sent()

    # AccessError Tests
    test_invalid_token()

    test_user_isnot_member_of_dm()


#############################################################################
#                                                                           #
#                      http test for message_react Error                    #
#                                                                           #
#############################################################################


def test_message_react(parameters, parameters1, parameters2):
    requests.delete(config.url + "clear/v1")
    user0 = requests.post(config.url + "auth/register/v2", json=parameters)
    user1 = requests.post(config.url + "auth/register/v2", json=parameters1)
    user2 = requests.post(config.url + "auth/register/v2", json=parameters2)

    token_0 = json.loads(user0.text).get("token")
    json.loads(user1.text).get("token")
    token_2 = json.loads(user2.text).get("token")

    json.loads(user0.text).get("auth_user_id")
    u_id_1 = json.loads(user1.text).get("auth_user_id")
    json.loads(user2.text).get("auth_user_id")

    dm = requests.post(config.url + "dm/create/v1", json={"token": token_0, "u_ids": [u_id_1]})
    dm_0_id = json.loads(dm.text).get("dm_id")
    channel = requests.post(config.url + "channels/create/v2", json={"token": token_0, "name": "channel_0", "is_public": True})
    channel_0_id = json.loads(channel.text).get("channel_id")

    requests.post(config.url + "channel/invite/v2", json={"token": token_0, "channel_id": channel_0_id, "u_id": u_id_1})

    dm_message_0 = requests.post(config.url + "message/senddm/v1", json={"token": token_0, "dm_id": dm_0_id, "message": "I am message."})
    dm_message_0_message_id = json.loads(dm_message_0.text).get("message_id")
    dm_message_1 = requests.post(config.url + "message/senddm/v1", json={"token": token_0, "dm_id": dm_0_id, "message": "@first1last1 I am message."})
    dm_message_1_message_id = json.loads(dm_message_1.text).get("message_id")

    channel_message_0 = requests.post(config.url + "message/send/v2", json={"token": token_0, "channel_id": channel_0_id, "message": "I am message."})
    channel_message_0_message_id = json.loads(channel_message_0.text).get("message_id")
    channel_message_1 = requests.post(config.url + "message/send/v2", json={"token": token_0, "channel_id": channel_0_id, "message": "@first0last0 I am messag."})
    channel_message_1_message_id = json.loads(channel_message_1.text).get("message_id")

    def test_invalid_token():
        input1 = {"token": "string token", "message_id": dm_message_0_message_id, "react_id": 1}
        input2 = {"token": 111000, "message_id": dm_message_0_message_id, "react_id": 1}
        input3 = {"token": None, "message_id": dm_message_0_message_id, "react_id": 1}

        status1 = requests.post(config.url + "message/react/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/react/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/react/v1", json=input3).status_code

        assert status1 == 403
        assert status2 == 403
        assert status3 == 403

    def test_invalid_message_id():
        input1 = {"token": token_0, "message_id": "string message_id", "react_id": 1}
        input2 = {"token": token_0, "message_id": 99999999, "react_id": 1}
        input3 = {"token": token_0, "message_id": None, "react_id": 1}

        status1 = requests.post(config.url + "message/react/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/react/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/react/v1", json=input3).status_code

        assert status1 == 400
        assert status2 == 400
        assert status3 == 400

    def test_invalid_react_id():
        input1 = {"token": token_0, "message_id": dm_message_0_message_id, "react_id": "string react_id"}
        input2 = {"token": token_0, "message_id": dm_message_0_message_id, "react_id": 9999}
        input3 = {"token": token_0, "message_id": dm_message_0_message_id, "react_id": None}

        status1 = requests.post(config.url + "message/react/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/react/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/react/v1", json=input3).status_code

        assert status1 == 400
        assert status2 == 400
        assert status3 == 400

    # InputError : React_id is already contained in the message

    def test_react_id_already_in_message():
        input1 = {"token": token_0, "message_id": dm_message_0_message_id, "react_id": 1}
        input2 = {"token": token_0, "message_id": dm_message_0_message_id, "react_id": 1}
        input3 = {"token": token_0, "message_id": dm_message_0_message_id, "react_id": 1}

        status1 = requests.post(config.url + "message/react/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/react/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/unreact/v1", json=input3).status_code

        assert status1 == 200
        assert status2 == 403
        assert status3 == 200

    # AccessError: The authorised user is not a member of the channel or DM

    def test_user_isnot_member_of_channel():
        input1 = {"token": token_2, "message_id": channel_message_0_message_id, "react_id": 1}
        input2 = {"token": token_2, "message_id": channel_message_1_message_id, "react_id": 1}

        status1 = requests.post(config.url + "message/react/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/react/v1", json=input2).status_code

        assert status1 == 403
        assert status2 == 403

    def test_user_isnot_member_of_dm():
        input1 = {"token": token_2, "message_id": dm_message_0_message_id, "react_id": 1}
        input2 = {"token": token_2, "message_id": dm_message_1_message_id, "react_id": 1}

        status1 = requests.post(config.url + "message/react/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/react/v1", json=input2).status_code

        assert status1 == 403
        assert status2 == 403

    # ----------------------------testing------------------------------------
    # InputError Tests
    test_invalid_message_id()
    test_invalid_react_id()
    test_react_id_already_in_message()

    # AccessError Tests
    test_invalid_token()

    test_user_isnot_member_of_channel()
    test_user_isnot_member_of_dm()


#############################################################################
#                                                                           #
#                    http test for message_unreact Error                    #
#                                                                           #
#############################################################################


def test_message_unreact(parameters, parameters1, parameters2):
    requests.delete(config.url + "clear/v1")
    user0 = requests.post(config.url + "auth/register/v2", json=parameters)
    user1 = requests.post(config.url + "auth/register/v2", json=parameters1)
    user2 = requests.post(config.url + "auth/register/v2", json=parameters2)

    token_0 = json.loads(user0.text).get("token")
    json.loads(user1.text).get("token")
    token_2 = json.loads(user2.text).get("token")

    json.loads(user0.text).get("auth_user_id")
    u_id_1 = json.loads(user1.text).get("auth_user_id")
    json.loads(user2.text).get("auth_user_id")

    dm = requests.post(config.url + "dm/create/v1", json={"token": token_0, "u_ids": [u_id_1]})
    dm_0_id = json.loads(dm.text).get("dm_id")
    channel = requests.post(config.url + "channels/create/v2", json={"token": token_0, "name": "channel_0", "is_public": True})
    channel_0_id = json.loads(channel.text).get("channel_id")

    requests.post(config.url + "channel/invite/v2", json={"token": token_0, "channel_id": channel_0_id, "u_id": u_id_1})

    dm_message_0 = requests.post(config.url + "message/senddm/v1", json={"token": token_0, "dm_id": dm_0_id, "message": "I am message."})
    dm_message_0_message_id = json.loads(dm_message_0.text).get("message_id")
    dm_message_1 = requests.post(config.url + "message/senddm/v1", json={"token": token_0, "dm_id": dm_0_id, "message": "@first1last1 I am message."})
    dm_message_1_message_id = json.loads(dm_message_1.text).get("message_id")

    channel_message_0 = requests.post(config.url + "message/send/v2", json={"token": token_0, "channel_id": channel_0_id, "message": "I am message."})
    channel_message_0_message_id = json.loads(channel_message_0.text).get("message_id")
    channel_message_1 = requests.post(config.url + "message/send/v2", json={"token": token_0, "channel_id": channel_0_id, "message": "@first0last0 I am messag."})
    channel_message_1_message_id = json.loads(channel_message_1.text).get("message_id")

    def test_invalid_token():
        input1 = {"token": "string token", "message_id": dm_message_0_message_id, "react_id": 1}
        input2 = {"token": 111000, "message_id": dm_message_0_message_id, "react_id": 1}
        input3 = {"token": None, "message_id": dm_message_0_message_id, "react_id": 1}

        status1 = requests.post(config.url + "message/unreact/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/unreact/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/unreact/v1", json=input3).status_code

        assert status1 == 403
        assert status2 == 403
        assert status3 == 403

    def test_invalid_message_id():
        input1 = {"token": token_0, "message_id": "string message_id", "react_id": 1}
        input2 = {"token": token_0, "message_id": 99999999, "react_id": 1}
        input3 = {"token": token_0, "message_id": None, "react_id": 1}

        status1 = requests.post(config.url + "message/unreact/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/unreact/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/unreact/v1", json=input3).status_code

        assert status1 == 400
        assert status2 == 400
        assert status3 == 400

    def test_invalid_react_id():
        input1 = {"token": token_0, "message_id": dm_message_0_message_id, "react_id": "string react_id"}
        input2 = {"token": token_0, "message_id": dm_message_0_message_id, "react_id": 9999}
        input3 = {"token": token_0, "message_id": dm_message_0_message_id, "react_id": None}

        status1 = requests.post(config.url + "message/unreact/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/unreact/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/unreact/v1", json=input3).status_code

        assert status1 == 400
        assert status2 == 400
        assert status3 == 400

    # InputError : React_id is not contained in the message

    def test_react_id_not_in_message():
        input1 = {"token": token_0, "message_id": dm_message_0_message_id, "react_id": 1}
        input2 = {"token": token_0, "message_id": dm_message_0_message_id, "react_id": 1}
        input3 = {"token": token_0, "message_id": dm_message_0_message_id, "react_id": 1}

        status1 = requests.post(config.url + "message/react/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/unreact/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/unreact/v1", json=input3).status_code

        assert status1 == 200
        assert status2 == 200
        assert status3 == 403

    # AccessError: The authorised user is not a member of the channel or DM

    def test_user_isnot_member_of_channel():
        input1 = {"token": token_0, "message_id": channel_message_0_message_id, "react_id": 1}
        input2 = {"token": token_0, "message_id": channel_message_1_message_id, "react_id": 1}
        input3 = {"token": token_2, "message_id": channel_message_0_message_id, "react_id": 1}
        input4 = {"token": token_2, "message_id": channel_message_1_message_id, "react_id": 1}

        status1 = requests.post(config.url + "message/react/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/react/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/unreact/v1", json=input3).status_code
        status4 = requests.post(config.url + "message/unreact/v1", json=input4).status_code
        status5 = requests.post(config.url + "message/unreact/v1", json=input1).status_code
        status6 = requests.post(config.url + "message/unreact/v1", json=input2).status_code

        assert status1 == 200
        assert status2 == 200
        assert status3 == 403
        assert status4 == 403
        assert status5 == 200
        assert status6 == 200

    def test_user_isnot_member_of_dm():
        input1 = {"token": token_0, "message_id": dm_message_0_message_id, "react_id": 1}
        input2 = {"token": token_0, "message_id": dm_message_1_message_id, "react_id": 1}
        input3 = {"token": token_2, "message_id": dm_message_0_message_id, "react_id": 1}
        input4 = {"token": token_2, "message_id": dm_message_1_message_id, "react_id": 1}

        status1 = requests.post(config.url + "message/react/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/react/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/unreact/v1", json=input3).status_code
        status4 = requests.post(config.url + "message/unreact/v1", json=input4).status_code
        status5 = requests.post(config.url + "message/unreact/v1", json=input1).status_code
        status6 = requests.post(config.url + "message/unreact/v1", json=input2).status_code

        assert status1 == 200
        assert status2 == 200
        assert status3 == 403
        assert status4 == 403
        assert status5 == 200
        assert status6 == 200

    # ----------------------------testing------------------------------------
    # InputError Tests
    test_invalid_message_id()
    test_invalid_react_id()
    test_react_id_not_in_message()

    # AccessError Tests
    test_invalid_token()

    test_user_isnot_member_of_channel()
    test_user_isnot_member_of_dm()


#############################################################################
#                                                                           #
#                       http test for message_pin Error                     #
#                                                                           #
#############################################################################


def test_message_pin(parameters, parameters1, parameters2):
    requests.delete(config.url + "clear/v1")
    user0 = requests.post(config.url + "auth/register/v2", json=parameters)
    user1 = requests.post(config.url + "auth/register/v2", json=parameters1)
    user2 = requests.post(config.url + "auth/register/v2", json=parameters2)

    token_0 = json.loads(user0.text).get("token")
    token_1 = json.loads(user1.text).get("token")
    token_2 = json.loads(user2.text).get("token")

    json.loads(user0.text).get("auth_user_id")
    u_id_1 = json.loads(user1.text).get("auth_user_id")
    json.loads(user2.text).get("auth_user_id")

    dm = requests.post(config.url + "dm/create/v1", json={"token": token_0, "u_ids": [u_id_1]})
    dm_0_id = json.loads(dm.text).get("dm_id")
    channel = requests.post(config.url + "channels/create/v2", json={"token": token_0, "name": "channel_0", "is_public": True})
    channel_0_id = json.loads(channel.text).get("channel_id")

    requests.post(config.url + "channel/invite/v2", json={"token": token_0, "channel_id": channel_0_id, "u_id": u_id_1})

    dm_message_0 = requests.post(config.url + "message/senddm/v1", json={"token": token_0, "dm_id": dm_0_id, "message": "I am message."})
    dm_message_0_message_id = json.loads(dm_message_0.text).get("message_id")
    requests.post(config.url + "message/senddm/v1", json={"token": token_0, "dm_id": dm_0_id, "message": "@first1last1 I am message."})
    dm_message_1_message_id = json.loads(dm_message_0.text).get("message_id")

    requests.post(config.url + "message/send/v2", json={"token": token_0, "channel_id": channel_0_id, "message": "I am message."})
    channel_message_0_message_id = json.loads(dm_message_0.text).get("message_id")
    requests.post(config.url + "message/send/v2", json={"token": token_0, "channel_id": channel_0_id, "message": "@first0last0 I am messag."})
    channel_message_1_message_id = json.loads(dm_message_0.text).get("message_id")

    def test_invalid_token():
        input1 = {"token": "string token", "message_id": dm_message_0_message_id}
        input2 = {"token": 111000, "message_id": dm_message_0_message_id}
        input3 = {"token": None, "message_id": dm_message_0_message_id}

        status1 = requests.post(config.url + "message/pin/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/pin/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/pin/v1", json=input3).status_code

        assert status1 == 403
        assert status2 == 403
        assert status3 == 403

    def test_invalid_message_id():
        input1 = {"token": token_0, "message_id": "string message_id"}
        input2 = {"token": token_0, "message_id": 99999999}
        input3 = {"token": token_0, "message_id": None}

        status1 = requests.post(config.url + "message/pin/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/pin/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/pin/v1", json=input3).status_code

        assert status1 == 400
        assert status2 == 400
        assert status3 == 400

    # InputError : Message with ID message_id is already pinned

    def test_message_id_already_pinned():
        input1 = {"token": token_0, "message_id": dm_message_0_message_id}

        status1 = requests.post(config.url + "message/pin/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/pin/v1", json=input1).status_code
        status3 = requests.post(config.url + "message/unpin/v1", json=input1).status_code

        assert status1 == 200
        assert status3 == 200
        assert status2 == 400

    # AccessError: The authorised user is not a member of the channel or DM

    def test_user_isnot_member_of_channel():
        input1 = {"token": token_2, "message_id": channel_message_0_message_id}
        input2 = {"token": token_2, "message_id": channel_message_1_message_id}

        status1 = requests.post(config.url + "message/pin/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/pin/v1", json=input2).status_code

        assert status1 == 403
        assert status2 == 403

    def test_user_isnot_member_of_dm():
        input1 = {"token": token_2, "message_id": dm_message_0_message_id}
        input2 = {"token": token_2, "message_id": dm_message_1_message_id}

        status1 = requests.post(config.url + "message/pin/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/pin/v1", json=input2).status_code

        assert status1 == 403
        assert status2 == 403

    # AccessError: The authorised user is not an owner of the channel or DM

    def test_user_isnot_owner_of_channel():
        input1 = {"token": token_1, "message_id": channel_message_0_message_id}

        status1 = requests.post(config.url + "message/pin/v1", json=input1).status_code

        assert status1 == 403

    def test_user_isnot_owner_of_dm():
        input1 = {"token": token_1, "message_id": dm_message_1_message_id}

        status1 = requests.post(config.url + "message/pin/v1", json=input1).status_code

        assert status1 == 403

    # ----------------------------testing------------------------------------
    # InputError Tests
    test_invalid_message_id()
    test_message_id_already_pinned()

    # AccessError Tests
    test_invalid_token()

    test_user_isnot_member_of_channel()
    test_user_isnot_member_of_dm()

    test_user_isnot_owner_of_channel()
    test_user_isnot_owner_of_dm()


#############################################################################
#                                                                           #
#                    http test for message_unpin Error                      #
#                                                                           #
#############################################################################


def test_message_unpin(parameters, parameters1, parameters2):
    requests.delete(config.url + "clear/v1")
    user0 = requests.post(config.url + "auth/register/v2", json=parameters)
    user1 = requests.post(config.url + "auth/register/v2", json=parameters1)
    user2 = requests.post(config.url + "auth/register/v2", json=parameters2)

    token_0 = json.loads(user0.text).get("token")
    token_1 = json.loads(user1.text).get("token")
    token_2 = json.loads(user2.text).get("token")

    json.loads(user0.text).get("auth_user_id")
    u_id_1 = json.loads(user1.text).get("auth_user_id")
    json.loads(user2.text).get("auth_user_id")

    dm = requests.post(config.url + "dm/create/v1", json={"token": token_0, "u_ids": [u_id_1]})
    dm_0_id = json.loads(dm.text).get("dm_id")
    channel = requests.post(config.url + "channels/create/v2", json={"token": token_0, "name": "channel_0", "is_public": True})
    channel_0_id = json.loads(channel.text).get("channel_id")

    requests.post(config.url + "channel/invite/v2", json={"token": token_0, "channel_id": channel_0_id, "u_id": u_id_1})

    dm_message_0 = requests.post(config.url + "message/senddm/v1", json={"token": token_0, "dm_id": dm_0_id, "message": "I am message."})
    dm_message_0_message_id = json.loads(dm_message_0.text).get("message_id")
    dm_message_1 = requests.post(config.url + "message/senddm/v1", json={"token": token_0, "dm_id": dm_0_id, "message": "@first1last1 I am message."})
    dm_message_1_message_id = json.loads(dm_message_1.text).get("message_id")

    channel_message_0 = requests.post(config.url + "message/send/v2", json={"token": token_0, "channel_id": channel_0_id, "message": "I am message."})
    channel_message_0_message_id = json.loads(channel_message_0.text).get("message_id")
    channel_message_1 = requests.post(config.url + "message/send/v2", json={"token": token_0, "channel_id": channel_0_id, "message": "@first0last0 I am messag."})
    channel_message_1_message_id = json.loads(channel_message_1.text).get("message_id")

    def test_invalid_token():
        input1 = {"token": "string token", "message_id": dm_message_0_message_id}
        input2 = {"token": 111000, "message_id": dm_message_0_message_id}
        input3 = {"token": None, "message_id": dm_message_0_message_id}

        status1 = requests.post(config.url + "message/unpin/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/unpin/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/unpin/v1", json=input3).status_code

        assert status1 == 403
        assert status2 == 403
        assert status3 == 403

    def test_invalid_message_id():
        input1 = {"token": token_0, "message_id": "string message_id"}
        input2 = {"token": token_0, "message_id": 99999999}
        input3 = {"token": token_0, "message_id": None}

        status1 = requests.post(config.url + "message/unpin/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/unpin/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/unpin/v1", json=input3).status_code

        assert status1 == 400
        assert status2 == 400
        assert status3 == 400

    # InputError : Message with ID message_id is already unpinned

    def test_message_id_already_unpinned():
        input1 = {"token": token_0, "message_id": dm_message_0_message_id}

        status1 = requests.post(config.url + "message/pin/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/unpin/v1", json=input1).status_code
        status3 = requests.post(config.url + "message/unpin/v1", json=input1).status_code

        assert status1 == 200
        assert status2 == 200
        assert status3 == 400

    # AccessError: The authorised user is not a member of the channel or DM

    def test_user_isnot_member_of_channel():
        input1 = {"token": token_0, "message_id": channel_message_0_message_id}
        input2 = {"token": token_0, "message_id": channel_message_1_message_id}
        input3 = {"token": token_2, "message_id": channel_message_0_message_id}
        input4 = {"token": token_2, "message_id": channel_message_1_message_id}

        status1 = requests.post(config.url + "message/pin/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/pin/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/unpin/v1", json=input3).status_code
        status4 = requests.post(config.url + "message/unpin/v1", json=input4).status_code

        assert status1 == 200
        assert status2 == 200
        assert status3 == 403
        assert status4 == 403

    def test_user_isnot_member_of_dm():
        input1 = {"token": token_0, "message_id": dm_message_0_message_id}
        input2 = {"token": token_0, "message_id": dm_message_1_message_id}
        input3 = {"token": token_2, "message_id": dm_message_0_message_id}
        input4 = {"token": token_2, "message_id": dm_message_1_message_id}

        status1 = requests.post(config.url + "message/pin/v1", json=input1).status_code
        status2 = requests.post(config.url + "message/pin/v1", json=input2).status_code
        status3 = requests.post(config.url + "message/unpin/v1", json=input3).status_code
        status4 = requests.post(config.url + "message/unpin/v1", json=input4).status_code

        assert status1 == 200
        assert status2 == 200
        assert status3 == 403
        assert status4 == 403

    # AccessError: The authorised user is not an owner of the channel or DM

    def test_user_isnot_owner_of_channel():
        input1 = {"token": token_1, "message_id": channel_message_0_message_id}

        status1 = requests.post(config.url + "message/unpin/v1", json=input1).status_code

        assert status1 == 403

    def test_user_isnot_owner_of_dm():
        input1 = {"token": token_1, "message_id": dm_message_1_message_id}

        status1 = requests.post(config.url + "message/unpin/v1", json=input1).status_code

        assert status1 == 403

    # ----------------------------testing------------------------------------
    # InputError Tests
    test_invalid_message_id()
    test_message_id_already_unpinned()

    # AccessError Tests
    test_invalid_token()

    test_user_isnot_member_of_channel()
    test_user_isnot_member_of_dm()

    test_user_isnot_owner_of_channel()
    test_user_isnot_owner_of_dm()
    requests.delete(config.url + 'clear/v1')
