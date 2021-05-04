from datetime import datetime, timezone
from src.channel import channel_invite_v1, channel_messages_v1
import pytest
from src.dm import dm_create_v1, dm_invite_v1, dm_messages_v1, dm_remove_v1
from src.error import InputError, AccessError
from src.channels import channels_create_v1
from src.auth import auth_register_v1, auth_login_v1
from src.other import clear_v1
from src.message import (
    message_send_v2,
    message_edit_v2,
    message_remove_v1,
    message_share_v1,
    message_senddm_v1,
    message_sendlater_v1,
    message_sendlaterdm_v1,
    message_react_v1,
    message_unreact_v1,
    message_pin_v1,
    message_unpin_v1,
)


#############################################################################
#                                                                           #
#                        Test for message_send_v2                           #
#                                                                           #
#############################################################################
"""

Author: Shaozhen Yan

Background:
Send a message from authorised_user to the channel specified by channel_id. 
Note: Each message should have it's own unique ID. I.E. No messages should share an ID with another message, even if that other message is in a different channel.

Parameters: (token, channel_id, message)
Return Type: { message_id }
HTTP Method: POST

InputError:
    - (Added) Invalid token.
    - Message is more than 1000 characters
AccessError:
    - (Added) Invalid channel_id
    - the authorised user has not joined the channel they are trying to post to

"""


def test_message_send_invalid_token_v1():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First", "Last")["token"]
    auth_login_v1("test_email0@gmail.com", "password")
    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    message_send_v2(token_0, channel_0_id, "Hope it works")

    with pytest.raises(AccessError):
        message_send_v2("invlaid_token", channel_0_id, "it works!")

    clear_v1()


def test_message_send_long_message_v1():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First", "Last")["token"]
    auth_login_v1("test_email0@gmail.com", "password")
    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    long_message = "m" * 1001

    with pytest.raises(InputError):
        message_send_v2(token_0, channel_0_id, long_message)

    clear_v1()


def test_message_send_invalid_channel_id_v1():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First", "Last")["token"]
    auth_login_v1("test_email0@gmail.com", "password")
    channels_create_v1(token_0, "channel_0", True)

    with pytest.raises(InputError):
        message_send_v2(token_0, "invalid channel_id", "it not works")

    clear_v1()


def test_message_send_not_join_v1():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    auth_login_v1("test_email0@gmail.com", "password")
    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]

    token_1 = auth_register_v1("test_email1@email.com", "password", "First1", "Last1")["token"]
    auth_login_v1("test_email1@email.com", "password")

    with pytest.raises(AccessError):
        message_send_v2(token_1, channel_0_id, "You can't send msg")

    clear_v1()


def test_message_send_same_message_id():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    auth_login_v1("test_email0@gmail.com", "password")
    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    message_send_v2(token_0, channel_0_id, "Hope it works")

    token_1 = auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")["token"]
    auth_login_v1("test_email1@gmail.com", "password")

    with pytest.raises(AccessError):
        message_send_v2(token_1, channel_0_id, "Hope it works")

    clear_v1()


def test_message_send_valid_case():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First", "Last")["token"]
    u_id = auth_login_v1("test_email0@gmail.com", "password")["auth_user_id"]
    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    message_0_id = message_send_v2(token_0, channel_0_id, "Hope it works")["message_id"]
    all_messages = channel_messages_v1(token_0, channel_0_id, 0)

    assert all_messages["messages"][0]["message"] == "Hope it works"
    assert all_messages["messages"][0]["message_id"] == message_0_id
    assert all_messages["messages"][0]["u_id"] == u_id

    clear_v1()


#############################################################################
#                                                                           #
#                        Test for message_remove_v1                         #
#                                                                           #
#############################################################################
"""
Author: Shaozhen Yan

Background:
Given a message_id for a message, this message is removed from the channel/DM

Parameters: (token, message_id)
Return Type: {}
HTTP Method: DELETE

InputError:
    - (Added) Invalid token.
    - Message (based on ID) no longer exists
AccessError when none of the following are true:
    - Message with message_id was sent by the authorised user making this request
    - The authorised user is an owner of this channel (if it was sent to a channel) or the **Dreams**

"""


def test_message_remove_invalid_token():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First", "Last")["token"]
    auth_login_v1("test_email0@gmail.com", "password")
    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    message_0_id = message_send_v2(token_0, channel_0_id, "Hope it works")["message_id"]

    with pytest.raises(AccessError):
        message_remove_v1("invlaid_token", message_0_id)

    clear_v1()


def test_message_remove_message_not_exist():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")
    auth_login_v1("test_email0@gmail.com", "password")
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")["auth_user_id"]

    dm_0_id = dm_create_v1(token_0, [u_id_1])["dm_id"]
    message_id = message_senddm_v1(token_0, dm_0_id, "test_msg")["message_id"]

    message_remove_v1(token_0, message_id)

    with pytest.raises(InputError):
        message_remove_v1(token_0, message_id)

    clear_v1()


def test_message_remove_not_owner_or_authorised_user_channel():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    token_1 = auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")["token"]
    auth_login_v1("test_email0@gmail.com", "password")
    auth_login_v1("test_email1@gmail.com", "password")

    channel_0_id = channels_create_v1(token_0, "channel_0", False)["channel_id"]
    message_0_id = message_send_v2(token_0, channel_0_id, "Hope it works")["message_id"]

    # channel_invite_v1(token_0, channel_0_id, u_id_1)

    with pytest.raises(AccessError):
        message_remove_v1(token_1, message_0_id)

    clear_v1()


def test_message_remove_not_owner_or_authorised_user_dm():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")
    token_2 = auth_register_v1("test_email2@gmail.com", "password", "First2", "Last2")["token"]
    auth_login_v1("test_email0@gmail.com", "password")
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")["auth_user_id"]
    auth_login_v1("test_email2@gmail.com", "password")

    dm_0_id = dm_create_v1(token_0, [u_id_1])["dm_id"]
    message_1_id = message_senddm_v1(token_0, dm_0_id, "msg to dm")["message_id"]

    with pytest.raises(AccessError):
        message_remove_v1(token_2, message_1_id)

    clear_v1()


def test_message_remove_channel_valid_case():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First", "Last")["token"]
    auth_login_v1("test_email0@gmail.com", "password")

    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    message_0_id = message_send_v2(token_0, channel_0_id, "Hope it works")["message_id"]

    assert message_remove_v1(token_0, message_0_id) == {}

    clear_v1()


def test_message_remove_dm_valid_case():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First", "Last")["token"]
    auth_register_v1("test_email1@gmail.com", "password", "First", "Last")
    auth_login_v1("test_email0@gmail.com", "password")
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")["auth_user_id"]

    dm_id = dm_create_v1(token_0, [u_id_1])["dm_id"]
    message_0_id = message_senddm_v1(token_0, dm_id, "Hope it works")["message_id"]

    assert message_remove_v1(token_0, message_0_id) == {}

    clear_v1()


def test_remove_channel_dm_after_message_send():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First", "Last")["token"]
    auth_register_v1("test_email1@gmail.com", "password", "First", "Last")
    auth_login_v1("test_email0@gmail.com", "password")
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")["auth_user_id"]

    dm_id = dm_create_v1(token_0, [u_id_1])["dm_id"]
    message_0_id = message_senddm_v1(token_0, dm_id, "Hope it works")["message_id"]

    dm_remove_v1(token_0, 0)

    with pytest.raises(InputError):
        message_remove_v1(token_0, message_0_id)

    clear_v1()


#############################################################################
#                                                                           #
#                        Test for message_edit_v1                           #
#                                                                           #
#############################################################################
"""
Author: Shaozhen Yan

Background:
Given a message, update its text with new text. 
If the new message is an empty string, the message is deleted.

Parameters: (token, message_id, message)
Return Type: {}
HTTP Method: PUT

InputError:
    - (Added) Invalid token.
    - Length of message is over 1000 characters message_id refers to a deleted message
AccessError when none of the following are true:
    - Message with message_id was sent by the authorised user making this request
    - The authorised user is an owner of this channel (if it was sent to a channel) or the **Dreams**

"""


def test_invalid_token1():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First", "Last")["token"]
    auth_login_v1("test_email0@gmail.com", "password")

    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]

    message_0_id = message_send_v2(token_0, channel_0_id, "Hope it works")

    with pytest.raises(AccessError):
        message_edit_v2("invalid token", message_0_id, "Hope it works")

    clear_v1()


def test_invalid_token2():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First", "Last")["token"]
    auth_login_v1("test_email0@gmail.com", "password")

    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]

    message_0_id = message_send_v2(token_0, channel_0_id, "Hope it works")

    with pytest.raises(AccessError):
        message_edit_v2("invalid token", message_0_id, "Hope it works")

    clear_v1()


def test_message_edit_long_message():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First", "Last")["token"]
    auth_login_v1("test_email0@gmail.com", "password")

    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    long_message = "m" * 1000
    message_0_id = message_send_v2(token_0, channel_0_id, long_message)

    longer_message = "m" * 1001
    with pytest.raises(InputError):
        message_edit_v2(token_0, message_0_id, longer_message)

    clear_v1()


def test_message_edit_deleted_message():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First", "Last")["token"]
    auth_login_v1("test_email0@gmail.com", "password")

    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]

    message_send_v2(token_0, channel_0_id, "Hope it works")

    with pytest.raises(InputError):
        message_edit_v2(token_0, "non_exist_message_id", "It works")

    clear_v1()


def test_message_edit_not_owner_or_authorised_user():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    auth_login_v1("test_email0@gmail.com", "password")
    token_1 = auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")["token"]
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")["auth_user_id"]

    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    message_0_id = message_send_v2(token_0, channel_0_id, "Hope it works")["message_id"]

    channel_invite_v1(token_0, channel_0_id, u_id_1)

    with pytest.raises(AccessError):
        message_edit_v2(token_1, message_0_id, "It works")

    clear_v1()


def test_message_edit_empty_message():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First", "Last")["token"]
    auth_login_v1("test_email0@gmail.com", "password")

    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    message_0_id = message_send_v2(token_0, channel_0_id, "")["message_id"]
    message_edit_v2(token_0, message_0_id, "")
    all_messages = channel_messages_v1(token_0, channel_0_id, 0)

    assert all_messages["messages"] == []

    clear_v1()


def test_message_edit_valid_case_channel_msg():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First", "Last")["token"]
    u_id = auth_login_v1("test_email0@gmail.com", "password")["auth_user_id"]

    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    message_0_id = message_send_v2(token_0, channel_0_id, "It works")["message_id"]

    message_edit_v2(token_0, message_0_id, "It really works")
    all_messages = channel_messages_v1(token_0, channel_0_id, 0)

    assert all_messages["messages"][0]["message"] == "It really works"
    assert all_messages["messages"][0]["message_id"] == message_0_id
    assert all_messages["messages"][0]["u_id"] == u_id

    clear_v1()


def test_message_edit_valid_case_dm_msg():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First", "Last")["token"]
    auth_register_v1("test_email1@gmail.com", "password", "First", "Last")

    u_id_0 = auth_login_v1("test_email0@gmail.com", "password")["auth_user_id"]
    u_id_1 = auth_login_v1("test_email0@gmail.com", "password")["auth_user_id"]

    dm_id = dm_create_v1(token_0, [u_id_1])["dm_id"]
    message_0_id = message_senddm_v1(token_0, dm_id, "It works")["message_id"]

    message_edit_v2(token_0, message_0_id, "It really works")
    all_messages = dm_messages_v1(token_0, dm_id, 0)

    assert all_messages["messages"][0]["message"] == "It really works"
    assert all_messages["messages"][0]["message_id"] == message_0_id
    assert all_messages["messages"][0]["u_id"] == u_id_0

    clear_v1()


#############################################################################
#                                                                           #
#                        Test for message_share_v1                          #
#                                                                           #
#############################################################################
"""
Author: Shaozhen Yan

Background:
og_message_id is the original message. 
channel_id is the channel that the message is being shared to, and is -1 if it is being sent to a DM. 
dm_id is the DM that the message is being shared to, and is -1 if it is being sent to a channel. 
message is the optional message in addition to the shared message, and will be an empty string '' if no message is given

Parameters: (token, og_message_id, message, channel_id, dm_id)
Return Type: {shared_message_id}
HTTP Method: POST

InputError:
    - (Added) if neither channel_id nor dm_id is -1 or both are -1

AccessError: 
    - the authorised user has not joined the channel or DM they are trying to share the message to

"""


def test_message_share_channel_normal_case1():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    auth_login_v1("test_email0@gmail.com", "password")

    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    og_message_0_id = message_send_v2(token_0, channel_0_id, "Hope it works")["message_id"]

    all_messages = channel_messages_v1(token_0, channel_0_id, 0)
    message_0 = all_messages["messages"][0]["message"]

    shared_message = message_share_v1(token_0, og_message_0_id, message_0, channel_0_id, -1)

    assert shared_message["shared_message_id"] == 1

    clear_v1()


def test_message_share_channel_normal_case2():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    auth_login_v1("test_email0@gmail.com", "password")

    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    og_message_0_id = message_send_v2(token_0, channel_0_id, "Hope it works")["message_id"]

    all_messages = channel_messages_v1(token_0, channel_0_id, 0)
    message_0 = all_messages["messages"][0]["message"]

    shared_message = message_share_v1(token_0, og_message_0_id, message_0, channel_0_id, -1)

    assert shared_message["shared_message_id"] == 1

    clear_v1()


def test_message_share_dm_normal_case():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    auth_login_v1("test_email0@gmail.com", "password")

    auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")["auth_user_id"]

    dm_0_id = dm_create_v1(token_0, [u_id_1])["dm_id"]
    og_message_0_id = message_senddm_v1(token_0, dm_0_id, "Hope it works")["message_id"]

    all_messages = dm_messages_v1(token_0, dm_0_id, 0)
    message_0 = all_messages["messages"][0]["message"]

    shared_message = message_share_v1(token_0, og_message_0_id, message_0, -1, dm_0_id)

    assert shared_message["shared_message_id"] == 1

    clear_v1()


def test_message_share_user_invalid():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    auth_login_v1("test_email0@gmail.com", "password")

    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    og_message_0_id = message_send_v2(token_0, channel_0_id, "Hope it works")["message_id"]

    all_messages = channel_messages_v1(token_0, channel_0_id, 0)
    message_0 = all_messages["messages"][0]["message"]

    with pytest.raises(AccessError):
        message_share_v1("invalid token", og_message_0_id, message_0, channel_0_id, -1)
    with pytest.raises(AccessError):
        message_share_v1(None, og_message_0_id, message_0, channel_0_id, -1)

    clear_v1()


def test_message_share_dm_normal_case2():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    auth_login_v1("test_email0@gmail.com", "password")
    auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")["auth_user_id"]

    dm_0_id = dm_create_v1(token_0, [u_id_1])["dm_id"]
    og_message_0_id = message_senddm_v1(token_0, dm_0_id, "Hope it works")["message_id"]

    all_messages = dm_messages_v1(token_0, dm_0_id, 0)
    message_0 = all_messages["messages"][0]["message"]

    shared_message = message_share_v1(token_0, og_message_0_id, message_0, -1, dm_0_id)

    assert shared_message["shared_message_id"] == 1

    clear_v1()


def test_message_share_user_invalid2():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    auth_login_v1("test_email0@gmail.com", "password")
    auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")
    auth_login_v1("test_email1@gmail.com", "password")

    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    og_message_0_id = message_send_v2(token_0, channel_0_id, "Hope it works")["message_id"]

    all_messages = channel_messages_v1(token_0, channel_0_id, 0)
    message_0 = all_messages["messages"][0]["message"]

    with pytest.raises(AccessError):
        message_share_v1("invalid token", og_message_0_id, message_0, channel_0_id, -1)
    with pytest.raises(AccessError):
        message_share_v1(None, og_message_0_id, message_0, channel_0_id, -1)

    clear_v1()


def test_message_share_not_joing_channel():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    auth_login_v1("test_email0@gmail.com", "password")
    token_1 = auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")["token"]
    auth_login_v1("test_email1@gmail.com", "password")

    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    og_message_0_id = message_send_v2(token_0, channel_0_id, "Hope it works")["message_id"]

    all_messages = channel_messages_v1(token_0, channel_0_id, 0)
    message_0 = all_messages["messages"][0]["message"]

    with pytest.raises(AccessError):
        message_share_v1(token_1, og_message_0_id, message_0, channel_0_id, -1)

    clear_v1()


def test_message_share_not_joing_dm():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")
    token_2 = auth_register_v1("test_email2@gmail.com", "password", "First2", "Last2")["token"]
    auth_login_v1("test_email2@gmail.com", "password")
    u_id_0 = auth_login_v1("test_email0@gmail.com", "password")["auth_user_id"]
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")["auth_user_id"]

    u_id_list = [u_id_0, u_id_1]
    dm_0_id = dm_create_v1(token_0, u_id_list)["dm_id"]
    og_message_0_id = message_senddm_v1(token_0, dm_0_id, "Hope it works")["message_id"]

    all_messages = dm_messages_v1(token_0, dm_0_id, 0)
    message_0 = all_messages["messages"][0]["message"]

    with pytest.raises(AccessError):
        message_share_v1(token_2, og_message_0_id, message_0, -1, dm_0_id)

    clear_v1()


def test_message_share_channel_dm_id_neither():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    auth_login_v1("test_email0@gmail.com", "password")
    token_1 = auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")["token"]
    auth_login_v1("test_email1@gmail.com", "password")

    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    og_message_0_id = message_send_v2(token_0, channel_0_id, "Hope it works")["message_id"]

    all_messages = channel_messages_v1(token_0, channel_0_id, 0)
    message_0 = all_messages["messages"][0]["message"]

    with pytest.raises(InputError):
        message_share_v1(token_1, og_message_0_id, message_0, -1, -1)

    clear_v1()
# dm_id and channel_id are both -1


def test_message_share_channel_dm_id_both():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    token_1 = auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")["token"]
    u_id_0 = auth_login_v1("test_email0@gmail.com", "password")["auth_user_id"]
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")["auth_user_id"]

    u_id_list = [u_id_0, u_id_1]
    dm_0_id = dm_create_v1(token_0, u_id_list)["dm_id"]
    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    og_message_0_id = message_send_v2(token_0, channel_0_id, "Hope it works")["message_id"]

    all_messages = channel_messages_v1(token_0, channel_0_id, 0)
    message_0 = all_messages["messages"][0]["message"]

    with pytest.raises(InputError):
        message_share_v1(token_1, og_message_0_id, message_0, channel_0_id, dm_0_id)

    clear_v1()


#############################################################################
#                                                                           #
#                        Test for message_senddm_v1                         #
#                                                                           #
#############################################################################
"""
Author: Shi Tong Yuan

message/senddm/v1

Background:
Send a message from authorised_user to the DM specified by dm_id. Note: Each message should have it's own unique ID. I.E. No messages should share an ID with another message, even if that other message is in a different channel or DM.

Parameters: (token, dm_id, message)
Return Type: { message_id }
HTTP Method: POST

InputError:
    - (Added) Invalid token.
    - Message is more than 1000 characters
AccessError:
    - (Added) Invalid channel_id
    - the authorised user has not joined the channel they are trying to post to

"""


def test_message_senddm_v1():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")
    token_2 = auth_register_v1("test_email2@gmail.com", "password", "First2", "Last2")["token"]
    auth_register_v1("test_email3@gmail.com", "password", "First3", "Last3")

    auth_login_v1("test_email0@gmail.com", "password")
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")["auth_user_id"]
    auth_login_v1("test_email2@gmail.com", "password")
    auth_login_v1("test_email3@gmail.com", "password")

    dm_0_id = dm_create_v1(token_0, [u_id_1])["dm_id"]

    def test_invalid_token():
        with pytest.raises(AccessError):
            message_senddm_v1("invalid_token", dm_0_id, "dm_msg")
        with pytest.raises(AccessError):
            message_senddm_v1(None, dm_0_id, "dm_msg")

    def test_large_message():
        message_send = ""
        for _i in range(0, 2000):
            message_send += "1"
        with pytest.raises(InputError):
            message_senddm_v1(token_0, dm_0_id, message_send)

    def test_invalid_dm_id():
        with pytest.raises(InputError):
            message_senddm_v1(token_0, "invalid dm_id", "dm_msg")
        with pytest.raises(InputError):
            message_senddm_v1(token_0, 99999, "dm_msg")
        with pytest.raises(InputError):
            message_senddm_v1(token_0, None, "dm_msg")

    def test_auth_not_dm_member():
        with pytest.raises(AccessError):
            message_senddm_v1(token_2, dm_0_id, "dm_msg")

    def test_normal_case():
        result = message_senddm_v1(token_0, dm_0_id, "dm_msg")
        assert result["message_id"] == 0

    def test_normal_case_with_at():
        # @_target_user exists and also in dm
        result = message_senddm_v1(token_0, dm_0_id, "@first1last1 i_love_you")
        assert result["message_id"] == 1

    def test_failed_case_with_at():
        # @_target_user exists but not in dm
        result = message_senddm_v1(token_0, dm_0_id, "@first3last3 i_love_you")
        assert result["message_id"] == 2

    def test_failed_case2_with_at():
        # @_target_user not exists
        result = message_senddm_v1(token_0, dm_0_id, "@yst990102 i_love_you")
        assert result["message_id"] == 3

    def test_failed_case3_with_at():
        # @_target_user is None
        result = message_senddm_v1(token_0, dm_0_id, "@yst990102 i_love_you")
        assert result["message_id"] == 4

    # ----------------------------testing------------------------------------
    test_invalid_token()
    test_large_message()
    test_invalid_dm_id()
    test_auth_not_dm_member()
    test_normal_case()
    test_normal_case_with_at()
    test_failed_case_with_at()
    test_failed_case2_with_at()
    test_failed_case3_with_at()

    clear_v1()


#############################################################################
#                                                                           #
#                      Test for message_sendlater_v1                        #
#                                                                           #
#############################################################################
"""
Author: Shi Tong Yuan

message/sendlater/v1

Background:
Send a message from authorised_user to the channel specified by channel_id automatically at a specified time in the future

Parameters: (token, channel_id, message, time_sent)
Return Type: { message_id }
HTTP Method: POST

InputError:
    - Channel ID is not a valid channel
    - Message is more than 1000 characters
    - Time sent is a time in the past
AccessError:
    - the authorised user has not joined the channel they are trying to post to

"""


def test_message_sendlater_v1():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")
    token_2 = auth_register_v1("test_email2@gmail.com", "password", "First2", "Last2")["token"]

    auth_login_v1("test_email0@gmail.com", "password")
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")["auth_user_id"]
    auth_login_v1("test_email2@gmail.com", "password")

    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    channel_invite_v1(token_0, channel_0_id, u_id_1)

    time_sent = int(datetime(2020, 5, 9).replace(tzinfo=timezone.utc).timestamp())

    # test for the inputs checking
    def test_invalid_token():
        with pytest.raises(AccessError):
            message_sendlater_v1("string token", channel_0_id, "I am message.", time_sent)  # token's type is incorrect
        with pytest.raises(AccessError):
            message_sendlater_v1(111000, channel_0_id, "I am message.", time_sent)  # token's range is incorrect
        with pytest.raises(AccessError):
            message_sendlater_v1(None, channel_0_id, "I am message.", time_sent)  # token is None

    def test_invalid_channel_id():
        with pytest.raises(InputError):
            message_sendlater_v1(token_0, "invalid channel_id", "I am message.", time_sent)  # channel_id's type is incorrect
        with pytest.raises(InputError):
            message_sendlater_v1(token_0, 99999, "I am message.", time_sent)  # type matches, but channel_id not exist
        with pytest.raises(InputError):
            message_sendlater_v1(token_0, None, "I am message.", time_sent)  # channel_id is None

    def test_invalid_message():
        with pytest.raises(InputError):
            message_sendlater_v1(token_0, channel_0_id, 123456, time_sent)  # message's type is incorrect
        with pytest.raises(InputError):
            message_sendlater_v1(token_0, channel_0_id, "a" * 2000, time_sent)  # message is over_length
        with pytest.raises(InputError):
            message_sendlater_v1(token_0, channel_0_id, None, time_sent)  # message is None

    def test_invalid_time_sent():
        with pytest.raises(InputError):
            message_sendlater_v1(token_0, channel_0_id, "I am message.", "string time_sent")  # time_sent's type is incorrect
        with pytest.raises(InputError):
            message_sendlater_v1(token_0, channel_0_id, "I am message.", 123456)  # time_sent's range is incorrect
        with pytest.raises(InputError):
            message_sendlater_v1(token_0, channel_0_id, "I am message.", None)  # time_sent is None

        past_time_sent = datetime(1999, 1, 2).replace(tzinfo=timezone.utc).timestamp()
        with pytest.raises(InputError):
            message_sendlater_v1(token_0, channel_0_id, "I am message.", past_time_sent)  # time_sent is a time in the past

    # AccessError: the authorised user has not joined the channel they are trying to post to
    def test_user_isnot_member_of_channel():
        with pytest.raises(AccessError):
            message_sendlater_v1(token_2, channel_0_id, "I am message.", time_sent)

    # normal tests
    def test_normal_case01():
        # two late_send messages
        time_sent_1 = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())

        channel_msgs = channel_messages_v1(token_0, channel_0_id, 0)
        assert len(channel_msgs['messages']) == 0

        message_sendlater_v1(token_0, channel_0_id, "Here is message 01.", time_sent_1 + 1)['message_id']
        message_sendlater_v1(token_0, channel_0_id, "Here is message 02.", time_sent_1 + 2)['message_id']

        channel_msgs = channel_messages_v1(token_0, channel_0_id, 0)
        assert len(channel_msgs['messages']) == 0

        # Note: 这边需要加了data[threads]之后，方可判断timers的运行情况，sleep不行会所有进程都sleep掉
        # for i in data['threads']:
        #     i.join()
        #
        # channel_msgs = channel_messages_v1(token_0, channel_0_id, 0)
        # assert len(channel_msgs['messages']) == 2
        # assert channel_msgs['messages'][0]['message'] == "Here is message 02."
        # assert channel_msgs['messages'][1]['message'] == "Here is message 01."
        #
        # assert message_id_0 == 0
        # assert message_id_1 == 1

    def test_normal_case02():
        # three late_send messages, with time crosses
        time_sent_1 = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())

        channel_msgs = channel_messages_v1(token_0, channel_0_id, 0)
        assert len(channel_msgs['messages']) == 0

        message_sendlater_v1(token_0, channel_0_id, "Here is message 03.", time_sent_1 + 1)['message_id']
        message_sendlater_v1(token_0, channel_0_id, "Here is message 04.", time_sent_1 + 4)['message_id']
        message_sendlater_v1(token_0, channel_0_id, "Here is message 05.", time_sent_1 + 2)['message_id']

        channel_msgs = channel_messages_v1(token_0, channel_0_id, 0)
        assert len(channel_msgs['messages']) == 0

        # Note: 这边需要加了data[threads]之后，方可判断timers的运行情况，sleep不行会所有进程都sleep掉
        # for i in data['threads']:
        #     i.join()
        #
        # channel_msgs = channel_messages_v1(token_0, channel_0_id, 0)
        # assert len(channel_msgs['messages']) == 5
        # assert channel_msgs['messages'][0]['message'] == "Here is message 04."
        # assert channel_msgs['messages'][1]['message'] == "Here is message 05."
        # assert channel_msgs['messages'][2]['message'] == "Here is message 03."
        #
        # assert message_id_3 == 2
        # assert message_id_4 == 3
        # assert message_id_5 == 4

    # ----------------------------testing------------------------------------
    # InputError Tests
    test_invalid_channel_id()
    test_invalid_message()
    test_invalid_time_sent()

    # AccessError Tests
    test_invalid_token()

    test_user_isnot_member_of_channel()

    # normal tests
    test_normal_case01()
    test_normal_case02()

    clear_v1()


#############################################################################
#                                                                           #
#                     Test for message_sendlaterdm_v1                       #
#                                                                           #
#############################################################################
"""
Author: Shi Tong Yuan

message/sendlaterdm/v1

Background:
Send a message from authorised_user to the DM specified by dm_id automatically at a specified time in the future

Parameters: (token, dm_id, message, time_sent)
Return Type: { message_id }
HTTP Method: POST

InputError:
    - DM ID is not a valid DM
    - Message is more than 1000 characters
    - Time sent is a time in the past
AccessError:
    - the authorised user is not a member of the DM they are trying to post to

"""


def test_message_sendlaterdm_v1():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")
    token_2 = auth_register_v1("test_email2@gmail.com", "password", "First2", "Last2")["token"]

    auth_login_v1("test_email0@gmail.com", "password")
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")["auth_user_id"]
    auth_login_v1("test_email2@gmail.com", "password")

    dm_0_id = dm_create_v1(token_0, [u_id_1])["dm_id"]

    time_sent = int(datetime(2021, 5, 9).replace(tzinfo=timezone.utc).timestamp())

    # test for the inputs checking
    def test_invalid_token():
        with pytest.raises(AccessError):
            message_sendlaterdm_v1("string token", dm_0_id, "I am message.", time_sent)  # token's type is incorrect
        with pytest.raises(AccessError):
            message_sendlaterdm_v1(111000, dm_0_id, "I am message.", time_sent)  # token's range is incorrect
        with pytest.raises(AccessError):
            message_sendlaterdm_v1(None, dm_0_id, "I am message.", time_sent)  # token is None

    def test_invalid_dm_id():
        with pytest.raises(InputError):
            message_sendlaterdm_v1(token_0, "invalid dm_id", "I am message.", time_sent)  # dm_id's type is incorrect
        with pytest.raises(InputError):
            message_sendlaterdm_v1(token_0, 99999, "I am message.", time_sent)  # type matches, but dm_id not exist
        with pytest.raises(InputError):
            message_sendlaterdm_v1(token_0, None, "I am message.", time_sent)  # dm_id is None

    def test_invalid_message():
        with pytest.raises(InputError):
            message_sendlaterdm_v1(token_0, dm_0_id, 123456, time_sent)  # message's type is incorrect
        with pytest.raises(InputError):
            message_sendlaterdm_v1(token_0, dm_0_id, "a" * 2000, time_sent)  # message is over_length
        with pytest.raises(InputError):
            message_sendlaterdm_v1(token_0, dm_0_id, None, time_sent)  # message is None

    def test_invalid_time_sent():
        with pytest.raises(InputError):
            message_sendlaterdm_v1(token_0, dm_0_id, "I am message.", "string time_sent")  # time_sent's type is incorrect
        with pytest.raises(InputError):
            message_sendlaterdm_v1(token_0, dm_0_id, "I am message.", 123456)  # time_sent's range is incorrect
        with pytest.raises(InputError):
            message_sendlaterdm_v1(token_0, dm_0_id, "I am message.", None)  # time_sent is None

        past_time_sent = datetime(1999, 1, 2).replace(tzinfo=timezone.utc).timestamp()
        with pytest.raises(InputError):
            message_sendlaterdm_v1(token_0, dm_0_id, "I am message.", past_time_sent)  # time_sent is a time in the past

    # AccessError: the authorised user is not a member or owner of the DM

    def test_user_isnot_member_of_dm():
        with pytest.raises(AccessError):
            message_sendlaterdm_v1(token_2, dm_0_id, "I am message.", time_sent)

    # normal tests
    def test_normal_case01():
        # two late_send messages
        time_sent_1 = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())

        dm_msgs = dm_messages_v1(token_0, dm_0_id, 0)
        assert len(dm_msgs['messages']) == 0

        message_sendlaterdm_v1(token_0, dm_0_id, "Here is message 01.", time_sent_1 + 2)['message_id']
        message_sendlaterdm_v1(token_0, dm_0_id, "Here is message 02.", time_sent_1 + 3)['message_id']

        dm_msgs = dm_messages_v1(token_0, dm_0_id, 0)
        assert len(dm_msgs['messages']) == 0

        # for i in data['threads']:
        #     i.join()
        #
        # dm_msgs = dm_messages_v1(token_0, dm_0_id, 0)
        # assert len(dm_msgs['messages']) == 2
        # assert dm_msgs['messages'][0]['message'] == "Here is message 02."
        # assert dm_msgs['messages'][1]['message'] == "Here is message 01."
        #
        # assert message_id_0 == 0
        # assert message_id_1 == 1

    def test_normal_case02():
        # three late_send messages, with time crosses
        time_sent_1 = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())

        dm_msgs = dm_messages_v1(token_0, dm_0_id, 0)
        assert len(dm_msgs['messages']) == 0

        message_sendlaterdm_v1(token_0, dm_0_id, "Here is message 03.", time_sent_1 + 2)['message_id']
        message_sendlaterdm_v1(token_0, dm_0_id, "Here is message 04.", time_sent_1 + 8)['message_id']
        message_sendlaterdm_v1(token_0, dm_0_id, "Here is message 05.", time_sent_1 + 5)['message_id']

        dm_msgs = dm_messages_v1(token_0, dm_0_id, 0)
        assert len(dm_msgs['messages']) == 0

        # for i in data['threads']:
        #     i.join()
        #
        # dm_msgs = dm_messages_v1(token_0, dm_0_id, 0)
        # assert len(dm_msgs['messages']) == 5
        # assert dm_msgs['messages'][0]['message'] == "Here is message 04."
        # assert dm_msgs['messages'][1]['message'] == "Here is message 05."
        # assert dm_msgs['messages'][2]['message'] == "Here is message 03."
        #
        # assert message_id_3 == 2
        # assert message_id_4 == 3
        # assert message_id_5 == 4

    # ----------------------------testing------------------------------------
    # InputError Tests
    test_invalid_dm_id()
    test_invalid_message()
    test_invalid_time_sent()

    # AccessError Tests
    test_invalid_token()

    test_user_isnot_member_of_dm()

    # normal tests
    test_normal_case01()
    test_normal_case02()

    clear_v1()


#############################################################################
#                                                                           #
#                        Test for message_react_v1                          #
#                                                                           #
#############################################################################
"""
Author: Shi Tong Yuan

message/react/v1

Background:
Given a message within a channel or DM the authorised user is part of, add a "react" to that particular message

Parameters: (token, message_id, react_id)
Return Type: {}
HTTP Method: POST

InputError:
    - message_id is not a valid message within a channel or DM that the authorised user has joined
    - react_id is not a valid React ID. The only valid react ID the frontend has is 1
    - Message with ID message_id already contains an active React with ID react_id from the authorised user
AccessError:
    - The authorised user is not a member of the channel or DM that the message is within

"""


def test_message_react_v1():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")
    token_2 = auth_register_v1("test_email2@gmail.com", "password", "First2", "Last2")["token"]

    auth_login_v1("test_email0@gmail.com", "password")
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")["auth_user_id"]

    dm_0_id = dm_create_v1(token_0, [u_id_1])["dm_id"]
    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    channel_invite_v1(token_0, channel_0_id, u_id_1)

    dm_message_0 = message_senddm_v1(token_0, dm_0_id, "I am message.")
    dm_message_0_message_id = dm_message_0["message_id"]
    dm_message_1 = message_senddm_v1(token_0, dm_0_id, "@first1last1 I am message.")
    dm_message_1_message_id = dm_message_1["message_id"]

    channel_message_0 = message_send_v2(token_0, channel_0_id, "I am message.")
    channel_message_0_message_id = channel_message_0["message_id"]
    channel_message_1 = message_send_v2(token_0, channel_0_id, "@first0last0 I am message.")
    channel_message_1_message_id = channel_message_1["message_id"]

    # test for the inputs checking
    def test_invalid_token():
        with pytest.raises(AccessError):
            message_react_v1("string token", dm_message_0_message_id, 1)  # token's type is incorrect
        with pytest.raises(AccessError):
            message_react_v1(111000, dm_message_0_message_id, 1)  # token's range is incorrect
        with pytest.raises(AccessError):
            message_react_v1(None, dm_message_0_message_id, 1)  # token is None

    def test_invalid_message_id():
        with pytest.raises(InputError):
            message_react_v1(token_0, "string message_id", 1)  # message_id's type is incorrect
        with pytest.raises(InputError):
            message_react_v1(token_0, 99999999, 1)  # message_id's range is incorrect
        with pytest.raises(InputError):
            message_react_v1(token_0, None, 1)  # message_id is None

    def test_invalid_react_id():
        with pytest.raises(InputError):
            message_react_v1(token_0, dm_message_0_message_id, "string react_id")  # react_id type is incorrect
        with pytest.raises(InputError):
            message_react_v1(token_0, dm_message_0_message_id, 9999)  # react_id is int, but not 1
        with pytest.raises(InputError):
            message_react_v1(token_0, dm_message_0_message_id, None)  # react_id is None

    # InputError : React_id is already contained in the message
    def test_react_id_already_in_message():
        message_react_v1(token_0, dm_message_0_message_id, 1)
        with pytest.raises(AccessError):
            message_react_v1(token_0, dm_message_0_message_id, 1)
        message_unreact_v1(token_0, dm_message_0_message_id, 1)

    # AccessError: The authorised user is not a member of the channel or DM
    def test_user_isnot_member_of_channel():
        with pytest.raises(AccessError):
            message_react_v1(token_2, channel_message_0_message_id, 1)
        with pytest.raises(AccessError):
            message_react_v1(token_2, channel_message_1_message_id, 1)

    def test_user_isnot_member_of_dm():
        with pytest.raises(AccessError):
            message_react_v1(token_2, dm_message_0_message_id, 1)
        with pytest.raises(AccessError):
            message_react_v1(token_2, dm_message_1_message_id, 1)

    # normal tests
    def test_normal_test01():
        message_react_v1(token_0, channel_message_0_message_id, 1)
        message_react_v1(token_0, channel_message_1_message_id, 1)
        message_react_v1(token_0, dm_message_0_message_id, 1)
        message_react_v1(token_0, dm_message_1_message_id, 1)

    # ----------------------------testing------------------------------------
    # InputError Tests
    test_invalid_message_id()
    test_invalid_react_id()
    test_react_id_already_in_message()

    # AccessError Tests
    test_invalid_token()

    test_user_isnot_member_of_channel()
    test_user_isnot_member_of_dm()

    # normal tests
    test_normal_test01()

    clear_v1()


#############################################################################
#                                                                           #
#                       Test for message_unreact_v1                         #
#                                                                           #
#############################################################################
"""
Author: Shi Tong Yuan

message/unreact/v1

Background:
Given a message within a channel or DM the authorised user is part of, remove a "react" to that particular message.

Parameters: (token, message_id, react_id)
Return Type: {}
HTTP Method: POST

InputError:
    - message_id is not a valid message within a channel or DM that the authorised user has joined
    - react_id is not a valid React ID
    - Message with ID message_id does not contain an active React with ID react_id from the authorised user
AccessError:
    - The authorised user is not a member of the channel or DM that the message is within

"""


def test_message_unreact_v1():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    token_1 = auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")["token"]
    token_2 = auth_register_v1("test_email2@gmail.com", "password", "First2", "Last2")["token"]

    auth_login_v1("test_email0@gmail.com", "password")
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")["auth_user_id"]

    dm_0_id = dm_create_v1(token_0, [u_id_1])["dm_id"]
    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    channel_invite_v1(token_0, channel_0_id, u_id_1)

    dm_message_0 = message_senddm_v1(token_0, dm_0_id, "I am message.")
    dm_message_0_message_id = dm_message_0["message_id"]
    dm_message_1 = message_senddm_v1(token_0, dm_0_id, "@first1last1 I am message.")
    dm_message_1_message_id = dm_message_1["message_id"]

    channel_message_0 = message_send_v2(token_0, channel_0_id, "I am message.")
    channel_message_0_message_id = channel_message_0["message_id"]
    channel_message_1 = message_send_v2(token_0, channel_0_id, "@first0last0 I am message.")
    channel_message_1_message_id = channel_message_1["message_id"]

    # test for the inputs checking
    def test_invalid_token():
        with pytest.raises(AccessError):
            message_unreact_v1("string token", dm_message_0_message_id, 1)  # token's type is incorrect
        with pytest.raises(AccessError):
            message_unreact_v1(111000, dm_message_0_message_id, 1)  # token's range is incorrect
        with pytest.raises(AccessError):
            message_unreact_v1(None, dm_message_0_message_id, 1)  # token is None

    def test_invalid_message_id():
        with pytest.raises(InputError):
            message_unreact_v1(token_0, "string message_id", 1)  # message_id's type is incorrect
        with pytest.raises(InputError):
            message_unreact_v1(token_0, 99999999, 1)  # message_id's range is incorrect
        with pytest.raises(InputError):
            message_unreact_v1(token_0, None, 1)  # message_id is None

    def test_invalid_react_id():
        with pytest.raises(InputError):
            message_unreact_v1(token_0, dm_message_0_message_id, "string react_id")  # react_id type is incorrect
        with pytest.raises(InputError):
            message_unreact_v1(token_0, dm_message_0_message_id, 9999)  # react_id is int, but not 1
        with pytest.raises(InputError):
            message_unreact_v1(token_0, dm_message_0_message_id, None)  # react_id is None

    # InputError : React_id is not contained in the message
    def test_react_id_not_in_message():
        message_react_v1(token_0, dm_message_0_message_id, 1)
        message_unreact_v1(token_0, dm_message_0_message_id, 1)
        with pytest.raises(AccessError):
            message_unreact_v1(token_0, dm_message_0_message_id, 1)

    # AccessError: The authorised user is not a member of the channel or DM
    def test_user_isnot_member_of_channel():
        message_react_v1(token_0, channel_message_0_message_id, 1)
        message_react_v1(token_0, channel_message_1_message_id, 1)
        with pytest.raises(AccessError):
            message_unreact_v1(token_2, channel_message_0_message_id, 1)
        with pytest.raises(AccessError):
            message_unreact_v1(token_2, channel_message_1_message_id, 1)
        message_unreact_v1(token_0, channel_message_0_message_id, 1)
        message_unreact_v1(token_0, channel_message_1_message_id, 1)

    def test_user_isnot_member_of_dm():
        message_react_v1(token_0, dm_message_0_message_id, 1)
        message_react_v1(token_0, dm_message_1_message_id, 1)
        with pytest.raises(AccessError):
            message_unreact_v1(token_2, dm_message_0_message_id, 1)
        with pytest.raises(AccessError):
            message_unreact_v1(token_2, dm_message_1_message_id, 1)
        message_unreact_v1(token_0, dm_message_0_message_id, 1)
        message_unreact_v1(token_0, dm_message_1_message_id, 1)

    # normal tests
    def test_normal_test01():
        message_react_v1(token_0, channel_message_0_message_id, 1)
        message_react_v1(token_0, channel_message_1_message_id, 1)
        message_react_v1(token_0, dm_message_0_message_id, 1)
        message_react_v1(token_0, dm_message_1_message_id, 1)

        message_unreact_v1(token_0, channel_message_0_message_id, 1)
        message_unreact_v1(token_0, channel_message_1_message_id, 1)
        message_unreact_v1(token_0, dm_message_0_message_id, 1)
        message_unreact_v1(token_0, dm_message_1_message_id, 1)

    def test_normal_test02():
        message_react_v1(token_1, channel_message_0_message_id, 1)
        message_react_v1(token_1, channel_message_1_message_id, 1)
        message_react_v1(token_1, dm_message_0_message_id, 1)
        message_react_v1(token_1, dm_message_1_message_id, 1)

        message_unreact_v1(token_1, channel_message_0_message_id, 1)
        message_unreact_v1(token_1, channel_message_1_message_id, 1)
        message_unreact_v1(token_1, dm_message_0_message_id, 1)
        message_unreact_v1(token_1, dm_message_1_message_id, 1)

    # ----------------------------testing------------------------------------
    # InputError Tests
    test_invalid_message_id()
    test_invalid_react_id()
    test_react_id_not_in_message()

    # AccessError Tests
    test_invalid_token()

    test_user_isnot_member_of_channel()
    test_user_isnot_member_of_dm()

    # normal tests
    test_normal_test01()
    test_normal_test02()

    clear_v1()


#############################################################################
#                                                                           #
#                          Test for message_pin_v1                          #
#                                                                           #
#############################################################################
"""
Author: Shi Tong Yuan

message/pin/v1

Background:
Given a message within a channel or DM, mark it as "pinned" to be given special display treatment by the frontend

Parameters: (token, message_id)
Return Type: {}
HTTP Method: POST

InputError:
    - message_id is not a valid message
    - Message with ID message_id is already pinned
AccessError:
    - The authorised user is not a member of the channel or DM that the message is within
    - The authorised user is not an owner of the channel or DM

"""


def test_message_pin_v1():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    token_1 = auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")["token"]
    token_2 = auth_register_v1("test_email2@gmail.com", "password", "First2", "Last2")["token"]

    auth_login_v1("test_email0@gmail.com", "password")
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")["auth_user_id"]
    auth_login_v1("test_email2@gmail.com", "password")

    dm_0_id = dm_create_v1(token_0, [u_id_1])["dm_id"]
    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    channel_invite_v1(token_0, channel_0_id, u_id_1)

    dm_message_0 = message_senddm_v1(token_0, dm_0_id, "I am message.")
    dm_message_0_message_id = dm_message_0["message_id"]
    dm_message_1 = message_senddm_v1(token_0, dm_0_id, "@first1last1 I am message.")
    dm_message_1_message_id = dm_message_1["message_id"]

    channel_message_0 = message_send_v2(token_0, channel_0_id, "I am message.")
    channel_message_0_message_id = channel_message_0["message_id"]
    channel_message_1 = message_send_v2(token_0, channel_0_id, "@first0last0 I am message.")
    channel_message_1_message_id = channel_message_1["message_id"]

    # test for the inputs checking
    def test_invalid_token():
        with pytest.raises(AccessError):
            message_pin_v1("string token", dm_message_0_message_id)  # token's type is incorrect
        with pytest.raises(AccessError):
            message_pin_v1(111000, dm_message_0_message_id)  # token's range is incorrect
        with pytest.raises(AccessError):
            message_pin_v1(None, dm_message_0_message_id)  # token is None

    def test_invalid_message_id():
        with pytest.raises(InputError):
            message_pin_v1(token_0, "string message_id")  # message_id's type is incorrect
        with pytest.raises(InputError):
            message_pin_v1(token_0, 99999999)  # message_id's range is incorrect
        with pytest.raises(InputError):
            message_pin_v1(token_0, None)  # message_id is None

    # InputError : Message with ID message_id is already pinned
    def test_message_id_already_pinned():
        message_pin_v1(token_0, dm_message_0_message_id)
        with pytest.raises(InputError):
            message_pin_v1(token_0, dm_message_0_message_id)
        message_unpin_v1(token_0, dm_message_0_message_id)

    # AccessError: The authorised user is not a member of the channel or DM
    def test_user_isnot_member_of_channel():
        with pytest.raises(AccessError):
            message_pin_v1(token_2, channel_message_0_message_id)
        with pytest.raises(AccessError):
            message_pin_v1(token_2, channel_message_1_message_id)

    def test_user_isnot_member_of_dm():
        with pytest.raises(AccessError):
            message_pin_v1(token_2, dm_message_0_message_id)
        with pytest.raises(AccessError):
            message_pin_v1(token_2, dm_message_1_message_id)

    # AccessError: The authorised user is not an owner of the channel or DM

    def test_user_isnot_owner_of_channel():
        with pytest.raises(AccessError):
            message_pin_v1(token_1, channel_message_0_message_id)

    def test_user_isnot_owner_of_dm():
        with pytest.raises(AccessError):
            message_pin_v1(token_1, dm_message_1_message_id)

    # normal tests
    def test_normal_test01():
        message_pin_v1(token_0, channel_message_0_message_id)
        message_pin_v1(token_0, channel_message_1_message_id)
        message_pin_v1(token_0, dm_message_0_message_id)
        message_pin_v1(token_0, dm_message_1_message_id)
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

    # normal tests
    test_normal_test01()

    clear_v1()


#############################################################################
#                                                                           #
#                        Test for message_unpin_v1                          #
#                                                                           #
#############################################################################
"""
Author: Shi Tong Yuan

message/unpin/v1

Background:
Given a message within a channel or DM, remove it's mark as unpinned

Parameters: (token, message_id)
Return Type: {}
HTTP Method: POST

InputError:
    - message_id is not a valid message
    - Message with ID message_id is already unpinned
AccessError:
    - The authorised user is not a member of the channel or DM that the message is within
    - The authorised user is not an owner of the channel or DM

"""


def test_message_unpin_v1():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    token_1 = auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")["token"]
    token_2 = auth_register_v1("test_email2@gmail.com", "password", "First2", "Last2")["token"]

    auth_login_v1("test_email0@gmail.com", "password")
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")["auth_user_id"]
    auth_login_v1("test_email2@gmail.com", "password")

    dm_0_id = dm_create_v1(token_0, [u_id_1])["dm_id"]
    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]
    channel_invite_v1(token_0, channel_0_id, u_id_1)

    dm_message_0 = message_senddm_v1(token_0, dm_0_id, "I am message.")
    dm_message_0_message_id = dm_message_0["message_id"]
    dm_message_1 = message_senddm_v1(token_0, dm_0_id, "@first1last1 I am message.")
    dm_message_1_message_id = dm_message_1["message_id"]

    channel_message_0 = message_send_v2(token_0, channel_0_id, "I am message.")
    channel_message_0_message_id = channel_message_0["message_id"]
    channel_message_1 = message_send_v2(token_0, channel_0_id, "@first0last0 I am message.")
    channel_message_1_message_id = channel_message_1["message_id"]

    # test for the inputs checking

    def test_invalid_token():
        with pytest.raises(AccessError):
            message_unpin_v1("string token", dm_message_0_message_id)  # token's type is incorrect
        with pytest.raises(AccessError):
            message_unpin_v1(111000, dm_message_0_message_id)  # token's range is incorrect
        with pytest.raises(AccessError):
            message_unpin_v1(None, dm_message_0_message_id)  # token is None

    def test_invalid_message_id():
        with pytest.raises(InputError):
            message_unpin_v1(token_0, "string message_id")  # message_id's type is incorrect
        with pytest.raises(InputError):
            message_unpin_v1(token_0, 99999999)  # message_id's range is incorrect
        with pytest.raises(InputError):
            message_unpin_v1(token_0, None)  # message_id is None

    # InputError : Message with ID message_id is already unpinned
    def test_message_id_already_unpinned():
        message_pin_v1(token_0, dm_message_0_message_id)
        message_unpin_v1(token_0, dm_message_0_message_id)
        with pytest.raises(InputError):
            message_unpin_v1(token_0, dm_message_0_message_id)

    # AccessError: The authorised user is not a member of the channel or DM
    def test_user_isnot_member_of_channel():
        message_pin_v1(token_0, channel_message_0_message_id)
        message_pin_v1(token_0, channel_message_1_message_id)
        with pytest.raises(AccessError):
            message_unpin_v1(token_2, channel_message_0_message_id)
        with pytest.raises(AccessError):
            message_unpin_v1(token_2, channel_message_1_message_id)
        message_unpin_v1(token_0, channel_message_0_message_id)
        message_unpin_v1(token_0, channel_message_1_message_id)

    def test_user_isnot_member_of_dm():
        message_pin_v1(token_0, dm_message_0_message_id)
        message_pin_v1(token_0, dm_message_1_message_id)
        with pytest.raises(AccessError):
            message_unpin_v1(token_2, dm_message_0_message_id)
        with pytest.raises(AccessError):
            message_unpin_v1(token_2, dm_message_1_message_id)
        message_unpin_v1(token_0, dm_message_0_message_id)
        message_unpin_v1(token_0, dm_message_1_message_id)

    # AccessError: The authorised user is not an owner of the channel or DM
    def test_user_isnot_owner_of_channel():
        message_pin_v1(token_0, channel_message_0_message_id)
        message_pin_v1(token_0, channel_message_1_message_id)
        with pytest.raises(AccessError):
            message_unpin_v1(token_1, channel_message_0_message_id)
        with pytest.raises(AccessError):
            message_unpin_v1(token_1, channel_message_1_message_id)
        message_unpin_v1(token_0, channel_message_0_message_id)
        message_unpin_v1(token_0, channel_message_1_message_id)

    def test_user_isnot_owner_of_dm():
        message_pin_v1(token_0, dm_message_0_message_id)
        message_pin_v1(token_0, dm_message_1_message_id)
        with pytest.raises(AccessError):
            message_unpin_v1(token_1, dm_message_0_message_id)
        with pytest.raises(AccessError):
            message_unpin_v1(token_1, dm_message_1_message_id)
        message_unpin_v1(token_0, dm_message_0_message_id)
        message_unpin_v1(token_0, dm_message_1_message_id)

    # normal tests
    def test_normal_test01():
        message_pin_v1(token_0, channel_message_0_message_id)
        message_pin_v1(token_0, channel_message_1_message_id)
        message_pin_v1(token_0, dm_message_0_message_id)
        message_pin_v1(token_0, dm_message_1_message_id)

        message_unpin_v1(token_0, channel_message_0_message_id)
        message_unpin_v1(token_0, channel_message_1_message_id)
        message_unpin_v1(token_0, dm_message_0_message_id)
        message_unpin_v1(token_0, dm_message_1_message_id)
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

    # normal tests
    test_normal_test01()

    clear_v1()
#############################################################################
#                                                                           #
#                              Helper functions                             #
#                                                                           #
#############################################################################
