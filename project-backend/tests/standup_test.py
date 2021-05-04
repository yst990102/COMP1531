import pytest
from datetime import datetime, timezone
from time import sleep
from src.other import clear_v1
from src.auth import auth_login_v1, auth_register_v1, auth_logout
from src.error import InputError, AccessError
from src.channels import channels_create_v1, create_channel_id
from src.channel import channel_invite_v1, channel_messages_v1
from src.standup import standup_start_v1, standup_active_v1, standup_send_v1


def test_zen_Lan_tests():
    """
    Author : Emir Aditya Zen

    Test for standup_start_v1 function implementation

    Tests content:
    1. Succesful implementation of standup_start_v1
    2. Input error due to invalid channel_id used
    3. Input error due to an active standup is already running
    4. Access error due to authorised user not in channel
    5. Access error dur to invalid token
    """

    #############################################################################
    #                                                                           #
    #                         Test for standup_start_v1                         #
    #                                                                           #
    #############################################################################


def test_standup_start_successful():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    time_finish_check = standup_start_v1(token1, channel_id1, 1)['time_finish']
    standup_info = standup_active_v1(token1, channel_id1)
    assert standup_info['time_finish'] == time_finish_check
    assert standup_info['is_active'] is True


def test_standup_start_invalid_channel():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channels_create_v1(token1, 'ChannelOne', True)
    invalid_channelid = 100
    with pytest.raises(InputError):
        standup_start_v1(token1, invalid_channelid, 1)


def test_standup_start_currently_running_standup():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    standup_start_v1(token1, channel_id1, 1)
    with pytest.raises(InputError):
        standup_start_v1(token1, channel_id1, 1)


def test_standup_start_invalid_token():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    invalid_token = token1 + 'tsyerhdjycgj'
    with pytest.raises(AccessError):
        standup_start_v1(invalid_token, channel_id1, 1)


def test_standup_start_unauthorised_user():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    token2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    with pytest.raises(AccessError):
        standup_start_v1(token2, channel_id1, 1)


"""
Author : Emir Aditya Zen

Test for standup_active_v1 function implementation

Tests content:
1. Succesful implementation of standup_active_v1 with a present standup running
2. Succesful implementation of standup_active_v1 with no standup running
3. Input error due to invalid channel_id used
4. Access error dur to invalid token
"""

#############################################################################
#                                                                           #
#                        Test for standup_active_v1                         #
#                                                                           #
#############################################################################


def test_standup_active_standup_present():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    time_finish_check = standup_start_v1(token1, channel_id1, 1)
    standup_info = standup_active_v1(token1, channel_id1)
    assert standup_info['time_finish'] == time_finish_check['time_finish']
    assert standup_info['is_active'] is True


def test_standup_active_no_standup_present():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    standup_info = standup_active_v1(token1, channel_id1)
    assert standup_info['time_finish'] is None
    assert standup_info['is_active'] is False


def test_standup_active_invalid_channel():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    invalid_channelid = 100
    standup_start_v1(token1, channel_id1, 1)
    with pytest.raises(InputError):
        standup_active_v1(token1, invalid_channelid)


def test_standup_active_invalid_token():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    invalid_token = token1 + 'vwkudhbae'
    standup_start_v1(token1, channel_id1, 1)
    with pytest.raises(AccessError):
        standup_active_v1(invalid_token, channel_id1)


"""
Author : Emir Aditya Zen

Test for standup_send_v1 function implementation

Tests content:
1. Succesful implementation of standup_send_v1
2. Input error due to invalid channel_id used
3. Input error due to message is more than 1000 characters excluding username and colon
4. Input error due to no active standup present
5. Access error due to unauthorised user calling the function
6. ACcess error due to invalid token
"""

#############################################################################
#                                                                           #
#                        Test for standup_active_v1                         #
#                                                                           #
#############################################################################


def test_standup_send_successful():
    pass


def test_standup_send_invalid_channel():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    invalid_channelid = 100
    standup_start_v1(token1, channel_id1, 1)
    with pytest.raises(InputError):
        standup_send_v1(token1, invalid_channelid, 'This is the first message')


def test_standup_send_invalid_message():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    standup_start_v1(token1, channel_id1, 1)
    message = 'a' * 1500
    with pytest.raises(InputError):
        standup_send_v1(token1, channel_id1, message)


def test_standup_send_no_active_standup():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    with pytest.raises(InputError):
        standup_send_v1(token1, channel_id1, 'This is the first message')


def test_standup_send_unauthorised_user():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    token2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    standup_start_v1(token1, channel_id1, 1)
    with pytest.raises(AccessError):
        standup_send_v1(token2, channel_id1, "this is a test")


def test_standup_send_invalid_token():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    invalid_token = token1 + 'qytwiefvgiauwgfv'
    standup_start_v1(token1, channel_id1, 1)
    with pytest.raises(AccessError):
        standup_send_v1(invalid_token, channel_id1, 'This is the first message')


#############################################################################
#                                                                           #
#                         Test for standup_start_v1                         #
#                                                                           #
#############################################################################
def test_standup_start():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")
    token_2 = auth_register_v1("test_email2@gmail.com", "password", "First2", "Last2")["token"]

    auth_login_v1("test_email0@gmail.com", "password")
    auth_login_v1("test_email1@gmail.com", "password")
    auth_login_v1("test_email2@gmail.com", "password")

    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    channel_1_id = channels_create_v1(token_0, "channel_1", True)["channel_id"]

    # test for the inputs checking
    def test_invalid_token():
        with pytest.raises(AccessError):
            standup_start_v1("string token", channel_0_id, 10)  # token's type is incorrect
        with pytest.raises(AccessError):
            standup_start_v1(111000, channel_0_id, 10)  # token's range is incorrect
        with pytest.raises(AccessError):
            standup_start_v1(None, channel_0_id, 10)  # token is None

    def test_invalid_channel_id():
        with pytest.raises(InputError):
            standup_start_v1(token_0, "invalid channel_id", 10)  # channel_id's type is incorrect
        with pytest.raises(InputError):
            standup_start_v1(token_0, 99999, 10)  # type matches, but channel_id not exist
        with pytest.raises(InputError):
            standup_start_v1(token_0, None, 10)  # channel_id is None

    def test_invalid_length():
        with pytest.raises(InputError):
            standup_start_v1(token_0, channel_0_id, "string length")  # length's type is incorrect
        with pytest.raises(InputError):
            standup_start_v1(token_0, channel_0_id, -999)  # length' type match, but not positive integer
        with pytest.raises(InputError):
            standup_start_v1(token_0, channel_0_id, None)  # length is None

    # InputError : An active standup is currently running in this channel
    def test_standup_started_already():
        standup_start_v1(token_0, channel_0_id, 10)
        with pytest.raises(InputError):
            standup_start_v1(token_0, channel_0_id, 10)

    # AccessError : Authorised user is not in the channel
    def test_user_isnot_member_of_channel():
        with pytest.raises(AccessError):
            standup_start_v1(token_2, channel_0_id, 10)

    # normal tests
    def test_normal_test01():
        time_sent = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
        time_expected = standup_start_v1(token_0, channel_1_id, 2)['time_finish']
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

    clear_v1()
    pass


#############################################################################
#                                                                           #
#                        Test for standup_active_v1                         #
#                                                                           #
#############################################################################


def test_standup_active():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")
    auth_register_v1("test_email2@gmail.com", "password", "First2", "Last2")

    auth_login_v1("test_email0@gmail.com", "password")
    auth_login_v1("test_email1@gmail.com", "password")
    auth_login_v1("test_email2@gmail.com", "password")

    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    channel_1_id = channels_create_v1(token_0, "channel_1", True)["channel_id"]

    def test_invalid_token():
        with pytest.raises(AccessError):
            standup_active_v1("string token", channel_0_id)  # token's type is incorrect
        with pytest.raises(AccessError):
            standup_active_v1(111000, channel_0_id)  # token's range is incorrect
        with pytest.raises(AccessError):
            standup_active_v1(None, channel_0_id)  # token is None

    def test_invalid_channel_id():
        with pytest.raises(InputError):
            standup_active_v1(token_0, "invalid channel_id")  # channel_id's type is incorrect
        with pytest.raises(InputError):
            standup_active_v1(token_0, 99999)  # type matches, but channel_id not exist
        with pytest.raises(InputError):
            standup_active_v1(token_0, None)  # channel_id is None

    # normal tests
    def test_normal_test01():
        time_sent = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
        time_expected_1 = standup_start_v1(token_0, channel_0_id, 2)
        time_expected_2 = standup_start_v1(token_0, channel_1_id, 3)

        assert standup_active_v1(token_0, channel_0_id)['is_active'] is True
        assert standup_active_v1(token_0, channel_0_id)['time_finish'] == time_sent + 2

        assert standup_active_v1(token_0, channel_1_id)['is_active'] is True
        assert standup_active_v1(token_0, channel_1_id)['time_finish'] == time_sent + 3

        sleep(2)
        assert standup_active_v1(token_0, channel_0_id)['is_active'] is False
        assert standup_active_v1(token_0, channel_1_id)['is_active'] is True

        sleep(1)
        assert standup_active_v1(token_0, channel_0_id)['is_active'] is False
        assert standup_active_v1(token_0, channel_1_id)['is_active'] is False

        time_finish = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
        print(type(time_finish), type(time_expected_1), type(time_expected_2), time_sent + 3)
        assert time_finish == time_expected_1['time_finish'] + 1 == time_expected_2['time_finish'] == time_sent + 3

    # ----------------------------testing------------------------------------
    test_invalid_token()
    test_invalid_channel_id()

    test_normal_test01()

    clear_v1()

    pass


#############################################################################
#                                                                           #
#                        Test for standup_send_v1                           #
#                                                                           #
#############################################################################


def test_standup_send():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    token_1 = auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")["token"]
    token_2 = auth_register_v1("test_email2@gmail.com", "password", "First2", "Last2")["token"]

    auth_login_v1("test_email0@gmail.com", "password")
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")["auth_user_id"]
    auth_login_v1("test_email2@gmail.com", "password")

    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    channel_invite_v1(token_0, channel_0_id, u_id_1)

    def test_invalid_token():
        with pytest.raises(AccessError):
            standup_send_v1("string token", channel_0_id, "I am message.")  # token's type is incorrect
        with pytest.raises(AccessError):
            standup_send_v1(111000, channel_0_id, "I am message.")  # token's range is incorrect
        with pytest.raises(AccessError):
            standup_send_v1(None, channel_0_id, "I am message.")  # token is None

    def test_invalid_channel_id():
        with pytest.raises(InputError):
            standup_send_v1(token_0, "invalid channel_id", "I am message.")  # channel_id's type is incorrect
        with pytest.raises(InputError):
            standup_send_v1(token_0, 99999, "I am message.")  # type matches, but channel_id not exist
        with pytest.raises(InputError):
            standup_send_v1(token_0, None, "I am message.")  # channel_id is None

    def test_invalid_message():
        with pytest.raises(InputError):
            standup_send_v1(token_0, channel_0_id, 123456)  # message's type is incorrect
        with pytest.raises(InputError):
            standup_send_v1(token_0, channel_0_id, "a" * 2000)  # message is over_length
        with pytest.raises(InputError):
            standup_send_v1(token_0, channel_0_id, None)  # message is None

    # InputError : An active standup is not currently running in this channel
    def test_standup_not_started():
        with pytest.raises(InputError):
            standup_send_v1(token_0, channel_0_id, "haha")

    # AccessError : Authorised user is not in the channel
    def test_user_isnot_member_of_channel():
        with pytest.raises(AccessError):
            standup_start_v1(token_2, channel_0_id, 10)

    # normal tests
    def test_normal_test01():
        standup_start_v1(token_0, channel_0_id, 1)
        assert standup_active_v1(token_0, channel_0_id)['is_active'] is True

        standup_send_v1(token_0, channel_0_id, "message send by user_0.")
        channel_0_msgs = channel_messages_v1(token_0, channel_0_id, 0)
        assert len(channel_0_msgs['messages']) == 0

        standup_send_v1(token_1, channel_0_id, "message send by user_1.")
        channel_0_msgs = channel_messages_v1(token_0, channel_0_id, 0)
        assert len(channel_0_msgs['messages']) == 0

        sleep(2)
        assert standup_active_v1(token_0, channel_0_id)['is_active'] is False
        channel_0_msgs = channel_messages_v1(token_0, channel_0_id, 0)
        assert len(channel_0_msgs['messages']) == 1

    # ----------------------------testing------------------------------------
    test_invalid_token()
    test_invalid_channel_id()
    test_invalid_message()

    test_standup_not_started()
    test_user_isnot_member_of_channel()
    test_normal_test01()

    clear_v1()
    pass
