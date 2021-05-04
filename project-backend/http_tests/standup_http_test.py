import requests
import pytest
import json
from time import sleep
from datetime import datetime, timezone
from src import config


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
#                 http test for standup_start_v1                            #
#                                                                           #
#############################################################################
def test_standup_start(parameters, parameters1, parameters2):
    requests.delete(config.url + "clear/v1")
    user0 = requests.post(config.url + "auth/register/v2", json=parameters)
    user1 = requests.post(config.url + "auth/register/v2", json=parameters1)
    user2 = requests.post(config.url + "auth/register/v2", json=parameters2)

    token_0 = json.loads(user0.text).get("token")
    json.loads(user1.text).get("token")
    token_2 = json.loads(user2.text).get("token")

    json.loads(user0.text).get("auth_user_id")
    json.loads(user1.text).get("auth_user_id")
    json.loads(user2.text).get("auth_user_id")

    channel_0 = requests.post(config.url + "channels/create/v2", json={"token": token_0, "name": "channel_0", "is_public": True})
    channel_0_id = json.loads(channel_0.text).get("channel_id")
    channel_1 = requests.post(config.url + "channels/create/v2", json={"token": token_0, "name": "channel_1", "is_public": True})
    channel_1_id = json.loads(channel_1.text).get("channel_id")

    def test_invalid_token():
        input1 = {"token": "string token", "channel_id": channel_0_id, "length": 10}
        input2 = {"token": 111000, "channel_id": channel_0_id, "length": 10}
        input3 = {"token": None, "channel_id": channel_0_id, "length": 10}

        status1 = requests.post(config.url + "standup/start/v1", json=input1).status_code
        status2 = requests.post(config.url + "standup/start/v1", json=input2).status_code
        status3 = requests.post(config.url + "standup/start/v1", json=input3).status_code

        assert status1 == 403
        assert status2 == 403
        assert status3 == 403

    def test_invalid_channel_id():
        input1 = {"token": token_0, "channel_id": "invalid channel_id", "length": 10}
        input2 = {"token": token_0, "channel_id": 99999, "length": 10}
        input3 = {"token": token_0, "channel_id": None, "length": 10}

        status1 = requests.post(config.url + "standup/start/v1", json=input1).status_code
        status2 = requests.post(config.url + "standup/start/v1", json=input2).status_code
        status3 = requests.post(config.url + "standup/start/v1", json=input3).status_code

        assert status1 == 400
        assert status2 == 400
        assert status3 == 400

    def test_invalid_length():
        input1 = {"token": token_0, "channel_id": channel_0_id, "length": "string length"}
        input2 = {"token": token_0, "channel_id": channel_0_id, "length": -999}
        input3 = {"token": token_0, "channel_id": channel_0_id, "length": None}

        status1 = requests.post(config.url + "standup/start/v1", json=input1).status_code
        status2 = requests.post(config.url + "standup/start/v1", json=input2).status_code
        status3 = requests.post(config.url + "standup/start/v1", json=input3).status_code

        assert status1 == 400
        assert status2 == 400
        assert status3 == 400

    # InputError : An active standup is currently running in this channel
    def test_standup_started_already():
        input1 = {"token": token_0, "channel_id": channel_0_id, "length": 10}
        input2 = {"token": token_0, "channel_id": channel_0_id, "length": 10}

        status1 = requests.post(config.url + "standup/start/v1", json=input1).status_code
        status2 = requests.post(config.url + "standup/start/v1", json=input2).status_code

        assert status1 == 200
        assert status2 == 400

    # AccessError : Authorised user is not in the channel
    def test_user_isnot_member_of_channel():
        input1 = {"token": token_2, "channel_id": channel_0_id, "length": 10}

        status1 = requests.post(config.url + "standup/start/v1", json=input1).status_code

        assert status1 == 403

    # normal tests
    def test_normal_test01():
        time_sent = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())

        input1 = {"token": token_0, "channel_id": channel_1_id, "length": 2}
        expected = requests.post(config.url + "standup/start/v1", json=input1)
        time_expected = json.loads(expected.text).get("time_finish")

        sleep(2)

        time_finish = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())

        assert time_expected == time_finish == time_sent + 2

    # ----------------------------testing------------------------------------
    test_invalid_token()
    test_invalid_channel_id()
    test_invalid_length()

    test_standup_started_already()
    test_user_isnot_member_of_channel()

    # normal tests
    test_normal_test01()
    requests.delete(config.url + "clear/v1")
    pass
#############################################################################
#                                                                           #
#                 http test for standup_active_v1                           #
#                                                                           #
#############################################################################


def test_standup_active(parameters, parameters1, parameters2):
    requests.delete(config.url + "clear/v1")
    user0 = requests.post(config.url + "auth/register/v2", json=parameters)
    user1 = requests.post(config.url + "auth/register/v2", json=parameters1)
    user2 = requests.post(config.url + "auth/register/v2", json=parameters2)

    token_0 = json.loads(user0.text).get("token")
    json.loads(user1.text).get("token")
    json.loads(user2.text).get("token")

    json.loads(user0.text).get("auth_user_id")
    json.loads(user1.text).get("auth_user_id")
    json.loads(user2.text).get("auth_user_id")

    channel_0 = requests.post(config.url + "channels/create/v2", json={"token": token_0, "name": "channel_0", "is_public": True})
    channel_0_id = json.loads(channel_0.text).get("channel_id")
    channel_1 = requests.post(config.url + "channels/create/v2", json={"token": token_0, "name": "channel_1", "is_public": True})
    channel_1_id = json.loads(channel_1.text).get("channel_id")

    def test_invalid_token():
        input1 = {"token": "string token", "channel_id": channel_0_id}
        input2 = {"token": 111000, "channel_id": channel_0_id}
        input3 = {"token": None, "channel_id": channel_0_id}

        status1 = requests.get(config.url + "standup/active/v1", params=input1).status_code
        status2 = requests.get(config.url + "standup/active/v1", params=input2).status_code
        status3 = requests.get(config.url + "standup/active/v1", params=input3).status_code

        assert status1 == 403
        assert status2 == 403
        assert status3 == 403

    def test_invalid_channel_id():
        input1 = {"token": token_0, "channel_id": "invalid channel_id"}
        input2 = {"token": token_0, "channel_id": 99999}
        input3 = {"token": token_0, "channel_id": None}

        status1 = requests.get(config.url + "standup/active/v1", params=input1).status_code
        status2 = requests.get(config.url + "standup/active/v1", params=input2).status_code
        status3 = requests.get(config.url + "standup/active/v1", params=input3).status_code

        assert status1 == 400
        assert status2 == 400
        assert status3 == 400

    # normal tests
    def test_normal_test01():
        time_sent = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())

        input1 = {"token": token_0, "channel_id": channel_0_id, "length": 2}
        input2 = {"token": token_0, "channel_id": channel_1_id, "length": 3}

        expected_1 = requests.post(config.url + "standup/start/v1", json=input1)
        expected_2 = requests.post(config.url + "standup/start/v1", json=input2)

        time_finish_1 = json.loads(expected_1.text).get("time_finish")
        time_finish_2 = json.loads(expected_2.text).get("time_finish")

        input3 = {"token": token_0, "channel_id": channel_0_id}
        input4 = {"token": token_0, "channel_id": channel_1_id}

        active_1 = requests.get(config.url + "standup/active/v1", params=input3)
        active_2 = requests.get(config.url + "standup/active/v1", params=input4)

        assert json.loads(active_1.text).get("is_active") is True
        assert json.loads(active_1.text).get("time_finish") == time_sent + 2

        assert json.loads(active_2.text).get("is_active") is True
        assert json.loads(active_2.text).get("time_finish") == time_sent + 3

        sleep(2)
        active_1 = requests.get(config.url + "standup/active/v1", params=input3)
        active_2 = requests.get(config.url + "standup/active/v1", params=input4)
        assert json.loads(active_1.text).get("is_active") is False
        assert json.loads(active_2.text).get("is_active") is True

        sleep(1)
        active_1 = requests.get(config.url + "standup/active/v1", params=input3)
        active_2 = requests.get(config.url + "standup/active/v1", params=input4)
        assert json.loads(active_1.text).get("is_active") is False
        assert json.loads(active_2.text).get("is_active") is False

        time_finish = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())

        assert time_finish_1 + 1 - 2 <= time_finish <= time_finish_1 + 1 + 2
        assert time_finish_2 - 2 <= time_finish <= time_finish_2 + 2
        assert time_sent + 3 - 2 <= time_finish <= time_sent + 3 + 2
    # ----------------------------testing------------------------------------
    test_invalid_token()
    test_invalid_channel_id()

    test_normal_test01()
    requests.delete(config.url + "clear/v1")
    pass
#############################################################################
#                                                                           #
#                 http test for standup_send_v1                             #
#                                                                           #
#############################################################################


def test_standup_send(parameters, parameters1, parameters2):
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

    channel_0 = requests.post(config.url + "channels/create/v2", json={"token": token_0, "name": "channel_0", "is_public": True})
    channel_0_id = json.loads(channel_0.text).get("channel_id")

    requests.post(config.url + "channel/invite/v2", json={"token": token_0, "channel_id": channel_0_id, "u_id": u_id_1})

    def test_invalid_token():
        input1 = {"token": "string token", "channel_id": channel_0_id, "message": "I am message."}
        input2 = {"token": 111000, "channel_id": channel_0_id, "message": "I am message."}
        input3 = {"token": None, "channel_id": channel_0_id, "message": "I am message."}

        status1 = requests.post(config.url + "standup/send/v1", json=input1).status_code
        status2 = requests.post(config.url + "standup/send/v1", json=input2).status_code
        status3 = requests.post(config.url + "standup/send/v1", json=input3).status_code

        assert status1 == 403
        assert status2 == 403
        assert status3 == 403

    def test_invalid_channel_id():
        input1 = {"token": token_0, "channel_id": "invalid channel_id", "message": "I am message."}
        input2 = {"token": token_0, "channel_id": 99999, "message": "I am message."}
        input3 = {"token": token_0, "channel_id": None, "message": "I am message."}

        status1 = requests.post(config.url + "standup/send/v1", json=input1).status_code
        status2 = requests.post(config.url + "standup/send/v1", json=input2).status_code
        status3 = requests.post(config.url + "standup/send/v1", json=input3).status_code

        assert status1 == 400
        assert status2 == 400
        assert status3 == 400

    def test_invalid_message():
        input1 = {"token": token_0, "channel_id": channel_0_id, "message": 123456}
        input2 = {"token": token_0, "channel_id": channel_0_id, "message": "a" * 2000}
        input3 = {"token": token_0, "channel_id": channel_0_id, "message": None}

        status1 = requests.post(config.url + "standup/send/v1", json=input1).status_code
        status2 = requests.post(config.url + "standup/send/v1", json=input2).status_code
        status3 = requests.post(config.url + "standup/send/v1", json=input3).status_code

        assert status1 == 400
        assert status2 == 400
        assert status3 == 400

    # InputError : An active standup is not currently running in this channel
    def test_standup_not_started():
        input1 = {"token": token_0, "channel_id": channel_0_id, "message": "I am message."}

        status1 = requests.post(config.url + "standup/send/v1", json=input1).status_code

        assert status1 == 400

    # AccessError : Authorised user is not in the channel
    def test_user_isnot_member_of_channel():
        input1 = {"token": token_2, "channel_id": channel_0_id, "message": "I am message."}

        status1 = requests.post(config.url + "standup/send/v1", json=input1).status_code

        assert status1 == 403

    # normal tests
    def test_normal_test01():
        requests.post(config.url + "standup/start/v1", json={"token": token_0, "channel_id": channel_0_id, "length": 1})
        active_1 = requests.get(config.url + "standup/active/v1", params={"token": token_0, "channel_id": channel_0_id})
        assert json.loads(active_1.text).get("is_active") is True

        requests.post(config.url + "standup/send/v1", json={"token": token_0, "channel_id": channel_0_id, "message": "message send by user_0."})
        channel_0_msgs = requests.get(config.url + "channel/messages/v2", params={"token": token_0, "channel_id": channel_0_id, "start": 0})
        assert len(json.loads(channel_0_msgs.text).get("messages")) == 0

        requests.post(config.url + "standup/send/v1", json={"token": token_1, "channel_id": channel_0_id, "message": "message send by user_1."})
        channel_0_msgs = requests.get(config.url + "channel/messages/v2", params={"token": token_0, "channel_id": channel_0_id, "start": 0})
        assert len(json.loads(channel_0_msgs.text).get("messages")) == 0

        sleep(2)
        active_1 = requests.get(config.url + "standup/active/v1", params={"token": token_0, "channel_id": channel_0_id})
        assert json.loads(active_1.text).get("is_active") is False
        channel_0_msgs = requests.get(config.url + "channel/messages/v2", params={"token": token_0, "channel_id": channel_0_id, "start": 0})
        assert len(json.loads(channel_0_msgs.text).get("messages")) == 1

    # ----------------------------testing------------------------------------
    test_invalid_token()
    test_invalid_channel_id()
    test_invalid_message()

    test_standup_not_started()
    test_user_isnot_member_of_channel()
    test_normal_test01()
    requests.delete(config.url + "clear/v1")
