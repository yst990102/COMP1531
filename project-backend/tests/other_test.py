from src.error import AccessError, InputError
from src.dm import dm_create_v1
from src.server import auth_login_v2, message_senddm
import pytest
from src.channel import channel_invite_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.other import clear_v1, search_v1
from src.auth import auth_login_v1, auth_register_v1
from src.message import message_senddm_v1, message_send_v2

"""
Author : Shaozhen Yan

This file is for testing clear_v1 function implementation

Background
Resets the internal data of the application to it's initial state

Parameters: ()
Return Type: {}
"""


def test_clear_v1():
    # clear all of information to run test
    clear_v1()

    # create an user with details to run test
    register = auth_register_v1('user@gmail.com', 'qwe1212', 'shaozhen', 'yan')

    # create channels
    channels_create_v1(register['token'], 'test_public_channel', True)
    channels_create_v1(register['token'], 'test_private_channel', False)

    # check if the user and channel are created correctly
    assert channels_listall_v1(register['token'])['channels'][0] == {'channel_id': 0, 'name': 'test_public_channel'}
    assert channels_listall_v1(register['token'])['channels'][1] == {'channel_id': 1, 'name': 'test_private_channel'}

    # clear the information we created and check the validity of clear_v1
    clear_v1()
    register = auth_register_v1('user@gmail.com', 'qwe1212', 'shaozhen', 'yan')

    assert channels_listall_v1(register['token'])['channels'] == []


def test_search_v1():
    auth_register_v1('user0@gmail.com', 'qwe1212', 'shaozhen', 'yan')
    token0 = auth_login_v1('user0@gmail.com', 'qwe1212')['token']

    u_id1 = auth_register_v1('user1@gmail.com', 'yst990102', 'shitong', 'yuan')['auth_user_id']
    auth_login_v1('user1@gmail.com', 'yst990102')

    channel0_id = channels_create_v1(token0, "test_channel", True)['channel_id']
    dm0_id = dm_create_v1(token0, [u_id1])['dm_id']

    def test_invalid_token():
        # token type error
        with pytest.raises(AccessError):
            search_v1("invalid token", "query string")

    def test_oversize_string():
        oversize_string = ""
        for _i in range(0, 2000):
            oversize_string += "a"
        with pytest.raises(InputError):
            search_v1(token0, oversize_string)

    def test_search_in_channel():
        message_send_v2(token0, channel0_id, "channel_msg")

        msg_found = search_v1(token0, "channel_msg")['messages']
        assert msg_found[0]['message'] == "channel_msg"
        assert msg_found[0]['message_id'] == 0

    def test_search_in_dm():
        message_senddm_v1(token0, dm0_id, "dm_msg")

        msg_found = search_v1(token0, "dm_msg")['messages']
        assert msg_found[0]['message'] == "dm_msg"
        assert msg_found[0]['message_id'] == 1

    # ---------------------------testing--------------------------
    test_invalid_token()
    test_oversize_string()
    test_search_in_channel()
    test_search_in_dm()
    pass
    clear_v1()
