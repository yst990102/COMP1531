# Imports the necessary function implementations
from src.auth import auth_login_v1, auth_register_v1
from src.channel import channel_invite_v1, channel_details_v1, channel_messages_v1, channel_join_v1, \
    channel_addowner_v1, channel_removeowner_v1, channel_leave_v1
from src.channels import channels_list_v1, channels_listall_v1, channels_create_v1
from src.other import clear_v1
from src.message import message_send_v2

# Imports the possible error output
from src.error import InputError, AccessError

# Imports pytest
import pytest

"""
Author: Emir Aditya Zen

This file is for testing channel_invite_v1 function implementation

Background
Invites a user (with user id u_id) to join a channel with ID channel_id.
Once invited the user is added to the channel immediately

HTTP Method: POST

Parameters: (token, channel_id, u_id)
Return Type: {}

InputError:
- channel_id does not refer to a valid channel.
- u_id does not refer to a valid user

AccessError:
- The authorised user is not a member of the channel
- The function is called with an invalid token
"""


#############################################################################
#                                                                           #
#                       Test for channel_invite_v1                          #
#                                                                           #
#############################################################################

# Case 1 - tests for valid function implementation (no errors expected)
#          expected outcome is user gets invited to a channel and gets added to it
# Occurs when channel is valid and user is valid whilst having not been invited before
def test_channel_invite_v1_success():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]
    u_id2 = token_id_dict2["auth_user_id"]

    # Create Channel_1 made by user_1 and get its id
    create_channel1 = channels_create_v1(token1, "channelone", True)
    channel_1_id = create_channel1["channel_id"]

    # Calls invite function for testing
    # Expected output is user_2 joins the Channel_1
    channel_invite_v1(token1, channel_1_id, u_id2)

    # Hence checks that Channel_1 exists, has 2 members, and the members are
    # user_1 and user_2
    channel_info = channel_details_v1(token1, channel_1_id)
    channel_members = channel_info['all_members']
    channel_owners = channel_info['owner_members']
    user1 = channel_members[0]
    user2 = channel_members[1]
    owner1 = channel_owners[0]
    assert user1['email'] == 'haha@gmail.com'
    assert user2['email'] == 'test@testexample.com'
    assert owner1['email'] == 'haha@gmail.com'
    assert len(channel_members) == 2
    assert len(channel_owners) == 1


# Case 2 - tests for repeated invite instances
#          expected outcome is recognizes user invited is already in the channel and does nothing
# Occurs when channel is valid and user is already inside the channel
def test_channel_invite_v1_repeated():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]
    u_id2 = token_id_dict2["auth_user_id"]

    # Create Channel_1 made by user_1 and get its id
    create_channel1 = channels_create_v1(token1, "channelone", True)
    channel_1_id = create_channel1["channel_id"]

    # Calls invite function twice targeting the same user for testing repetition
    # Expected output is user_2 joins the Channel_1 once
    channel_invite_v1(token1, channel_1_id, u_id2)
    channel_invite_v1(token1, channel_1_id, u_id2)

    # Hence checks that Channel_1 exists, has 2 members, and the members are
    # user_1 and user_2
    channel_info = channel_details_v1(token1, channel_1_id)
    channel_members = channel_info['all_members']
    channel_owners = channel_info['owner_members']
    user1 = channel_members[0]
    user2 = channel_members[1]
    owner1 = channel_owners[0]
    assert user1['email'] == 'haha@gmail.com'
    assert user2['email'] == 'test@testexample.com'
    assert owner1['email'] == 'haha@gmail.com'
    assert len(channel_members) == 2
    assert len(channel_owners) == 1


# Case 3 - tests for input error due to invalid channel
#          expected outcome is input error
# Occurs when channel_id does not refer to a valid channel.
def test_channel_invite_v1_inputErrorChannel():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]
    u_id2 = token_id_dict2["auth_user_id"]

    # Create Channel_1 made by user_1 and get its id
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]

    # Made an invalid channel id for testing
    channel_1_invalid_id = channel_1_id + 300

    # Test conditions leading to an input error outcome due to invalid channel_id
    with pytest.raises(InputError):
        channel_invite_v1(token1, channel_1_invalid_id, u_id2)


# Case 4 - tests for input error due to invalid user
#          expected outcome is input error
# Occurs when u_id does not refer to a valid user.
def test_channel_invite_v1_inputErrorUser():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]
    u_id2 = token_id_dict2["auth_user_id"]

    # Create Channel_1 made by user_1 and get its id
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]

    # Made an invalid user id for user 2
    u_invalid_id2 = u_id2 + 300

    # Test conditions leading to an input error outcome due to invalid u_id
    with pytest.raises(InputError):
        channel_invite_v1(token1, channel_1_id, u_invalid_id2)


# Case 5 - tests for access error due to inviter not part of channel
#          expected outcome is access error
# Occurs when the authorised user is not already a member of the channel
def test_channel_invite_v1_accessError():
    # Clears data and registers and logins user_1, user_2, and user_3
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")
    auth_register_v1("hah2@gmail.com", "9uisbxh83h", "Tom", "Green")

    # login the three registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token_id_dict3 = auth_login_v1("hah2@gmail.com", "9uisbxh83h")
    token1 = token_id_dict1["token"]
    token2 = token_id_dict2["token"]
    u_id3 = token_id_dict3["auth_user_id"]

    # Create Channel_1 made by user_1 and get its id
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]

    # Test conditions leading to an access error outcome
    with pytest.raises(AccessError):
        channel_invite_v1(token2, channel_1_id, u_id3)


# Case 6 - tests for access error due to invalid token
#          expected outcome is access error
# Occurs when channel_invite is called when token used is invalid
def test_channel_invite_v1_accessError_token():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]
    u_id2 = token_id_dict2["auth_user_id"]

    # Create Channel_1 made by user_1 and get its id
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]

    # Made an invalid token for user 1
    invalid_token = token1 + "rkbgesorgbv#$%"

    # Test conditions leading to an access error outcome
    with pytest.raises(AccessError):
        channel_invite_v1(invalid_token, channel_1_id, u_id2)
    with pytest.raises(AccessError):
        channel_invite_v1(None, channel_1_id, u_id2)


def test_channel_invite_v1_invalid_channel_id():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]
    u_id2 = token_id_dict2["auth_user_id"]

    # Create Channel_1 made by user_1 and get its id
    channels_create_v1(token1, "channelone", True)

    with pytest.raises(InputError):
        channel_invite_v1(token1, 123456, u_id2)
    with pytest.raises(InputError):
        channel_invite_v1(token1, None, u_id2)
    with pytest.raises(InputError):
        channel_invite_v1(token1, "invalid channel_id", u_id2)


"""
Author : Emir Aditya Zen

This file is for testing channel_details_v1 function implementation

Background
Given a Channel with ID channel_id that the authorised user
is part of, provide basic details about the channel

Parameters: (token, channel_id)
Return Type: {name, is_public, owner_members, all_members}

InputError:
- channel_id does not refer to a valid channel.

AccessError:
- The authorised user is not a member of the channel
- The function is called with an invalid token
"""


#############################################################################
#                                                                           #
#                       Test for channel_detail_v1                           #
#                                                                           #
#############################################################################

# Case 1 - tests for valid function implementation with a single group member
#          expected outcome is output of {name, is_public, owner_members, all_members}
# Occurs when channel is valid and there is only 1 member in that group
def test_channel_details_v1_success1():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered user
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Create Channel_1 made by user_1 and get its id
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]

    # Calls details function for testing
    output = channel_details_v1(token1, channel_1_id)

    assert output["all_members"][0]["name_first"] == 'Peter'
    assert output["owner_members"][0]["name_first"] == 'Peter'
    assert output["name"] == "channelone"
    assert output["is_public"] == True
    assert len(output["all_members"]) == 1
    assert len(output["owner_members"]) == 1


# Case 2 - tests for valid function implementation with multiple group member
#          expected outcome is output of {name, is_public, owner_members, all_members}
# Occurs when channel is valid and there are multiple members in that group
def test_channel_details_v1_success2():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]
    u_id2 = token_id_dict2["auth_user_id"]

    # Create Channel_1 made by user_1 and get its id
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]
    channel_invite_v1(token1, channel_1_id, u_id2)

    # Calls details function for testing
    output = channel_details_v1(token1, channel_1_id)

    assert output["all_members"][0]["name_first"] == 'Peter'
    assert output["all_members"][1]["name_first"] == 'Tom'
    assert output["owner_members"][0]["name_first"] == 'Peter'
    assert output["name"] == "channelone"
    assert output["is_public"] == True
    assert len(output["all_members"]) == 2
    assert len(output["owner_members"]) == 1


# Case 3 - tests for input error due to invalid channel
#          expected outcome is input error
# Occurs when channel_id does not refer to a valid channel.
def test_channel_details_v1_inputError():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered user
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Create Channel_1 made by user_1 and get its id
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]

    # Made an invalid channel id for testing
    channel_1_invalidid = channel_1_id + 300

    # Conditions leads to an input error outcome and tests for it
    with pytest.raises(InputError):
        channel_details_v1(token1, channel_1_invalidid)


# Case 4 - tests for access error due to inviter not part of channel
#          expected outcome is access error
# Occurs when the authorised user is not already a member of the channel
def test_channel_details_v1_accessError():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]
    token2 = token_id_dict2["token"]

    # Create Channel_1 made by user_1 and get its id
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]

    # Test conditions leading to an access error outcome
    with pytest.raises(AccessError):
        channel_details_v1(token2, channel_1_id)


# Case 5 - tests for access error due to invalid token
#          expected outcome is access error
# Occurs when channel_invite is called when token used is invalid
def test_channel_details_v1_accessErrortoken():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered user
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Create Channel_1 made by user_1 and get its id
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]

    # Made an invalid token for user 1
    invalid_token = token1 + "rkbgesorgbv#$%"

    # Conditions leads to an access error outcome and tests for it
    with pytest.raises(AccessError):
        channel_details_v1(invalid_token, channel_1_id)


"""
Author : Shi Tong Yuan
Updated for iteration 2 by : Emir Aditya Zen

This file is for testing channel_messages_v1 function implementation

Background
Given a Channel with ID channel_id that the authorised user is part of, 
return up to 50 messages between index "start" and "start + 50". 
Message with index 0 is the most recent message in the channel. This 
function returns a new index "end" which is the value of "start + 50", or, if 
this function has returned the least recent messages in the channel, 
returns -1 in "end" to indicate there are no more messages to load after this return.

Parameters: (token, channel_id, start)
Return Type: {messages, start, end}

InputError:
- Channel ID is not a valid channel
- start is greater than the total number of messages in the channel

AccessError:
- Authorised user is not a member of channel with channel_id
- The function is called with an invalid token
"""


#############################################################################
#                                                                           #
#                       Test for channel_messages_v1                        #
#                                                                           #
#############################################################################

def test_channel_messages_v1_invalid_channel_id():
    clear_v1()

    # create 2 users
    auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")
    user1 = auth_login_v1("user1@test.com", "user1password")

    auth_register_v1("user2@test.com", "user2password", "Lan", "Lin")
    user2 = auth_login_v1("user2@test.com", "user2password")

    # create channel for testing
    Testing_channel_id = channels_create_v1(user1["token"], "channel_test", True)
    channel_invite_v1(user1["token"], Testing_channel_id["channel_id"], user2["auth_user_id"])

    # testing for channel message function for invalid channel id inputError
    with pytest.raises(InputError):
        channel_messages_v1(user1['token'], "invalid channel_id", 0)
    with pytest.raises(InputError):
        channel_messages_v1(user1['token'], None, 0)


def test_invalid_token():
    clear_v1()

    # create 2 users
    auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")
    user1 = auth_login_v1("user1@test.com", "user1password")

    auth_register_v1("user2@test.com", "user2password", "Lan", "Lin")
    auth_login_v1("user2@test.com", "user2password")

    # create channel for testing
    Testing_channel_id = channels_create_v1(user1["token"], "channel_test", True)

    with pytest.raises(AccessError):
        channel_messages_v1("invalid token", Testing_channel_id["channel_id"], 0)
    with pytest.raises(AccessError):
        channel_messages_v1(None, Testing_channel_id["channel_id"], 0)


def test_auth_missing():
    clear_v1()

    # create 2 users and author people
    auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")
    user1 = auth_login_v1("user1@test.com", "user1password")

    auth_register_v1("user2@test.com", "user2password", "Lan", "Lin")
    user2 = auth_login_v1("user2@test.com", "user2password")

    auth_register_v1("user3@test.com", "user3password", "ShiTong", "Yuan")
    user3 = auth_login_v1("user3@test.com", "user3password")

    # create channel by user1 for testing
    Testing_channel_id = channels_create_v1(user1["token"], "channel_test", True)
    channel_invite_v1(user1["token"], Testing_channel_id["channel_id"], user2["auth_user_id"])

    # testing for channel message function for invalid channel id inputError
    with pytest.raises(AccessError):
        channel_messages_v1(user3["token"], Testing_channel_id["channel_id"], 0)


def test_no_msg():
    clear_v1()

    # create 2 users
    auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")
    user1 = auth_login_v1("user1@test.com", "user1password")

    auth_register_v1("user2@test.com", "user2password", "Lan", "Lin")
    user2 = auth_login_v1("user2@test.com", "user2password")

    # create channel for testing
    Testing_channel_id = channels_create_v1(user1["token"], "channel_test", True)
    channel_invite_v1(user1["token"], Testing_channel_id["channel_id"], user2["auth_user_id"])

    # 1. return -1 : for no more message after start
    message_stored = channel_messages_v1(user1["token"], Testing_channel_id["channel_id"], 0)["messages"]
    assert message_stored == [], "test_no_msg failed!!"


def test_less_than_50_msg():
    clear_v1()

    # create 2 users
    auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")
    user1 = auth_login_v1("user1@test.com", "user1password")

    # create channel for testing
    Testing_channel_id = channels_create_v1(user1["token"], "channel_test", True)

    # send testing message into channel chat
    for i in range(1, 3):
        message_send_v2(user1["token"], Testing_channel_id["channel_id"], f"This is a testing message{i}.")

    # 1. return -1 : for no more message after start
    message_stored = channel_messages_v1(user1["token"], Testing_channel_id["channel_id"], 0)["messages"]
    assert len(message_stored) == 2


def test_more_than_50_msg():
    clear_v1()

    # create 2 users
    auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")
    user1 = auth_login_v1("user1@test.com", "user1password")

    # create channel for testing
    Testing_channel_id = channels_create_v1(user1["token"], "channel_test", True)

    # send testing message into channel chat
    for i in range(1, 99):
        message_send_v2(user1["token"], Testing_channel_id["channel_id"], f"This is a testing message{i}.")

    # 1. return -1 : for no more message after start
    message_stored = channel_messages_v1(user1["token"], Testing_channel_id["channel_id"], 0)["messages"]
    assert len(message_stored) == 50


def test_great_starter():
    clear_v1()

    # create 2 users
    auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")
    user1 = auth_login_v1("user1@test.com", "user1password")

    # create channel for testing
    Testing_channel_id = channels_create_v1(user1["token"], "channel_test", True)

    with pytest.raises(InputError):
        channel_messages_v1(user1['token'], Testing_channel_id['channel_id'], 100)


"""
Author : Shi Tong Yuan
Updated for iteration 2 by : Emir Aditya Zen

This file is for testing channel_join_v1 function implementation

Background
Given a channel_id of a channel that the authorised user can join, adds them to that channel

Parameters: (token, channel_id)
Return Type: {}

InputError:
- Channel ID is not a valid channel

AccessError:
- channel_id refers to a channel that is private (when the authorised user is not a global owner)
- The function is called with an invalid token
"""


#############################################################################
#                                                                           #
#                         Test for channel_join_v1                          #
#                                                                           #
#############################################################################

# Case 1 - tests for valid function implementation
#          expected outcome is joiner joins the channel with output {}
# Occurs when token and channel id is valid, plus channel is public
def test_channel_join_normal():
    # Clears data and registers and logins owner and joiner
    clear_v1()
    auth_register_v1("TheOwner@test.com", "thisispassword", "ShiTong", "Yuan")
    auth_register_v1("TheJoiner@test.com", "joinerpassword", "Roger", "Luo")

    # login the two registered users
    owner = auth_login_v1("TheOwner@test.com", "thisispassword")
    joiner = auth_login_v1("TheJoiner@test.com", "joinerpassword")
    token_owner = owner["token"]
    token_joiner = joiner["token"]

    # Test owner is correct
    assert type(owner) is dict
    owner_u_id = owner["auth_user_id"]
    owner_auth_user_id = owner["auth_user_id"]
    assert owner_u_id is not None
    assert type(owner_u_id) is int
    assert type(owner_auth_user_id) is int
    assert type(token_owner) is str

    # Test joiner is correct
    assert type(joiner) is dict
    joiner_u_id = joiner["auth_user_id"]
    joiner_auth_id = joiner["auth_user_id"]
    assert joiner_u_id is not None
    assert type(joiner_u_id) is int
    assert type(joiner_auth_id) is int
    assert type(token_joiner) is str

    # create testing channel
    channel_id = channels_create_v1(token_owner, "Testing Channel", True)
    assert channel_id is not None
    assert type(channel_id["channel_id"]) is int

    # Test for correctly executed
    assert channel_join_v1(token_joiner, channel_id["channel_id"]) == {}

    # Calls details function for checking that joiner joins the channel
    output = channel_details_v1(token_owner, channel_id["channel_id"])

    assert output["all_members"][0]["name_first"] == 'ShiTong'
    assert output["all_members"][1]["name_first"] == 'Roger'
    assert output["owner_members"][0]["name_first"] == 'ShiTong'
    assert output["name"] == "Testing Channel"
    assert output["is_public"] is True
    assert len(output["all_members"]) == 2
    assert len(output["owner_members"]) == 1


# Case 2 - tests for input error due to invalid channel
#          expected outcome is input error
# Occurs when channel id used is invalid
def test_channel_join_v1_invalid_channel_id2():
    # Clears data and registers and logins owner and joiner
    clear_v1()
    auth_register_v1("TheOwner@test.com", "thisispassword", "ShiTong", "Yuan")
    auth_register_v1("TheJoiner@test.com", "joinerpassword", "Roger", "Luo")

    # login the two registered users
    owner = auth_login_v1("TheOwner@test.com", "thisispassword")
    joiner = auth_login_v1("TheJoiner@test.com", "joinerpassword")
    token_owner = owner["token"]
    token_joiner = joiner["token"]

    # Test owner is correct
    assert type(owner) is dict
    owner_u_id = owner["auth_user_id"]
    owner_auth_user_id = owner["auth_user_id"]
    assert owner_u_id is not None
    assert type(owner_u_id) is int
    assert type(owner_auth_user_id) is int
    assert type(token_owner) is str

    # Test joiner is correct
    assert type(joiner) is dict
    joiner_u_id = joiner["auth_user_id"]
    joiner_auth_id = joiner["auth_user_id"]
    assert joiner_u_id is not None
    assert type(joiner_u_id) is int
    assert type(joiner_auth_id) is int
    assert type(token_joiner) is str

    # create testing channel
    channel_id = channels_create_v1(token_owner, "Testing Channel", True)
    assert channel_id is not None
    assert type(channel_id["channel_id"]) is int

    # Test for invalid channel id
    invalid_id = {"channel_id": 999999}
    with pytest.raises(InputError):
        channel_join_v1(token_joiner, invalid_id["channel_id"])


# Case 3 - tests for access error due to private channel
#          expected outcome is access error
# Occurs when channel is private and joiner is not global owner
def test_join_private_channel():
    # Clears data and registers and logins owner and joiner
    clear_v1()
    auth_register_v1("TheOwner@test.com", "thisispassword", "ShiTong", "Yuan")
    auth_register_v1("TheJoiner@test.com", "joinerpassword", "Roger", "Luo")

    # login the two registered users
    owner = auth_login_v1("TheOwner@test.com", "thisispassword")
    joiner = auth_login_v1("TheJoiner@test.com", "joinerpassword")
    token_owner = owner["token"]
    token_joiner = joiner["token"]

    # Test owner is correct
    assert type(owner) is dict
    owner_u_id = owner["auth_user_id"]
    owner_auth_user_id = owner["auth_user_id"]
    assert owner_u_id is not None
    assert type(owner_u_id) is int
    assert type(owner_auth_user_id) is int
    assert type(token_owner) is str

    # Test joiner is correct
    assert type(joiner) is dict
    joiner_u_id = joiner["auth_user_id"]
    joiner_auth_id = joiner["auth_user_id"]
    assert joiner_u_id is not None
    assert type(joiner_u_id) is int
    assert type(joiner_auth_id) is int
    assert type(token_joiner) is str

    # create testing private channel
    channel_id_2 = channels_create_v1(token_owner, "Testing Channel_2", False)
    assert channel_id_2 is not None
    assert type(channel_id_2["channel_id"]) is int

    # Test for private channel
    with pytest.raises(AccessError):
        channel_join_v1(token_joiner, channel_id_2["channel_id"])


# Case 4 - tests for global owner calling function
#          expected outcome is global owner joins channel
# Occurs when channel is private and joiner is global owner
def test_join_global_owner():
    # Clears data and registers and logins global owner and owner
    clear_v1()
    auth_register_v1("TheGlobalOwner@test.com", "thisispassword", "ShiTong", "Yuan")
    auth_register_v1("TheOwner@test.com", "ownerpassword", "Roger", "Luo")

    # login the two registered users
    global_owner = auth_login_v1("TheGlobalOwner@test.com", "thisispassword")
    owner = auth_login_v1("TheOwner@test.com", "ownerpassword")
    token_global_owner = global_owner["token"]
    token_owner = owner["token"]

    # Test global owner is correct
    assert type(global_owner) is dict
    global_owner_u_id = owner["auth_user_id"]
    global_owner_auth_user_id = owner["auth_user_id"]
    assert global_owner_u_id is not None
    assert type(global_owner_u_id) is int
    assert type(global_owner_auth_user_id) is int
    assert type(token_global_owner) is str

    # Test owner is correct
    assert type(owner) is dict
    owner_u_id = owner["auth_user_id"]
    owner_auth_id = owner["auth_user_id"]
    assert owner_u_id is not None
    assert type(owner_u_id) is int
    assert type(owner_auth_id) is int
    assert type(token_owner) is str

    # create testing private channel
    channel_id_2 = channels_create_v1(token_owner, "Testing Channel_2", False)
    assert channel_id_2 is not None
    assert type(channel_id_2["channel_id"]) is int

    # Test for correctly executed
    assert channel_join_v1(token_global_owner, channel_id_2["channel_id"]) == {}

    # Calls details function for checking that joiner joins the channel
    output = channel_details_v1(token_owner, channel_id_2["channel_id"])

    assert output["all_members"][0]["name_first"] == 'Roger'
    assert output["all_members"][1]["name_first"] == 'ShiTong'
    assert output["owner_members"][0]["name_first"] == 'Roger'
    assert output["name"] == "Testing Channel_2"
    assert output["is_public"] is False
    assert len(output["all_members"]) == 2
    assert len(output["owner_members"]) == 1


# Case 5 - tests for access error due to invalid token
#          expected outcome is access error
# Occurs when channel_join is called when token used is invalid
def test_join_invalid_token():
    # Clears data and registers and logins owner and joiner
    clear_v1()
    auth_register_v1("TheOwner@test.com", "thisispassword", "ShiTong", "Yuan")
    auth_register_v1("TheJoiner@test.com", "joinerpassword", "Roger", "Luo")

    # login the two registered users
    owner = auth_login_v1("TheOwner@test.com", "thisispassword")
    joiner = auth_login_v1("TheJoiner@test.com", "joinerpassword")
    token_owner = owner["token"]
    token_joiner = joiner["token"]

    # Test owner is correct
    assert type(owner) is dict
    owner_u_id = owner["auth_user_id"]
    owner_auth_user_id = owner["auth_user_id"]
    assert owner_u_id is not None
    assert type(owner_u_id) is int
    assert type(owner_auth_user_id) is int
    assert type(token_owner) is str

    # Test joiner is correct
    assert type(joiner) is dict
    joiner_u_id = joiner["auth_user_id"]
    joiner_auth_id = joiner["auth_user_id"]
    assert joiner_u_id is not None
    assert type(joiner_u_id) is int
    assert type(joiner_auth_id) is int
    assert type(token_joiner) is str

    # create testing private channel
    channel_id_2 = channels_create_v1(token_owner, "Testing Channel_2", False)
    assert channel_id_2 is not None
    assert type(channel_id_2["channel_id"]) is int

    # Made an invalid token for joiner
    invalid_token = token_joiner + "rkbgesorgbv#$%"

    # Test for private channel
    with pytest.raises(AccessError):
        channel_join_v1(invalid_token, channel_id_2["channel_id"])


"""
Author : Emir Aditya Zen

This file is for testing channel_addowner_v1 function implementation

Background
Make user with user id u_id an owner of this channel

Parameters: (token, channel_id, u_id)
Return Type: {}

InputError:
- channel_id does not refer to a valid channel.
- user with u_id is already an owner of the channel

AccessError:
- The authorised user is not owner of dreams or channel
- The function is called with an invalid token
"""


#############################################################################
#                                                                           #
#                      Test for channel_addowner_v1                         #
#                                                                           #
#############################################################################

# Case 1 - tests for valid function implementation
#          expected outcome is user becomes owner and output is {}
# Occurs when channel and token is valid, user calling function is authorised
def test_channel_addowner_v1_success():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]
    u_id2 = token_id_dict2["auth_user_id"]

    # Create Channel_1 made by user_1, get its id, and invite user2
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]
    channel_invite_v1(token1, channel_1_id, u_id2)

    # Calls addowner function for testing
    # Expected output is user_2 becomes owner
    channel_addowner_v1(token1, channel_1_id, u_id2)

    # Calls details function for testing
    output = channel_details_v1(token1, channel_1_id)

    assert output["all_members"][0]["name_first"] == 'Peter'
    assert output["all_members"][1]["name_first"] == 'Tom'
    assert output["owner_members"][0]["name_first"] == 'Peter'
    assert output["owner_members"][1]["name_first"] == 'Tom'
    assert output["name"] == "channelone"
    assert output["is_public"] is True
    assert len(output["all_members"]) == 2
    assert len(output["owner_members"]) == 2


# Case 2 - tests for input error due to invalid channel
#          expected outcome is input error
# Occurs when channel id used is invalid
def test_channel_addowner_v1_inputErrorChannel():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]
    u_id2 = token_id_dict2["auth_user_id"]

    # Create Channel_1 made by user_1, get its id, and invite user2
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]
    channel_invite_v1(token1, channel_1_id, u_id2)

    # Made an invalid channel id for testing
    channel_1_invalidid = channel_1_id + 300

    # Conditions leads to an input error outcome and tests for it
    with pytest.raises(InputError):
        channel_addowner_v1(token1, channel_1_invalidid, u_id2)


# Case 3 - tests for input error due to function called for an owner
#          expected outcome is input error
# Occurs when add owner function is called to an existing owner
def test_channel_addowner_v1_inputErrorOwner():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]
    u_id2 = token_id_dict2["auth_user_id"]

    # Create Channel_1 made by user_1, get its id, and invite user2
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]
    channel_invite_v1(token1, channel_1_id, u_id2)

    # Conditions leads to an input error outcome and tests for it
    channel_addowner_v1(token1, channel_1_id, u_id2)
    with pytest.raises(InputError):
        channel_addowner_v1(token1, channel_1_id, u_id2)


def test_channel_addowner_v1_inputError_UserNotIn_channel():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]
    u_id2 = token_id_dict2["auth_user_id"]

    # Create Channel_1 made by user_1, get its id, and invite user2
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]

    # Conditions leads to an input error outcome and tests for it
    with pytest.raises(InputError):
        channel_addowner_v1(token1, channel_1_id, u_id2)


# Case 4 - tests for access error due to non authorised user
#          expected outcome is input error
# Occurs when add owner function is by a member of channel who is not a global owner
def test_channel_addowner_v1_accessError():
    # Clears data and registers and logins user_1, user_2, and user_3
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")
    auth_register_v1("hah2@gmail.com", "9uisbxh83h", "Tom", "Green")

    # login the three registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token_id_dict3 = auth_login_v1("hah2@gmail.com", "9uisbxh83h")
    token1 = token_id_dict1["token"]
    token2 = token_id_dict2["token"]
    u_id2 = token_id_dict2["auth_user_id"]
    u_id3 = token_id_dict3["auth_user_id"]

    # Create Channel_1 made by user_1, get its id, and invite user2
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]
    channel_invite_v1(token1, channel_1_id, u_id2)
    channel_invite_v1(token1, channel_1_id, u_id3)

    # Conditions leads to an access error outcome and tests for it
    with pytest.raises(AccessError):
        channel_addowner_v1(token2, channel_1_id, u_id3)


# Case 5 - tests for access error due invalid token
#          expected outcome is access error
# Occurs when add owner function is called using invalid token
def test_channel_addowner_v1_accessErrorToken():
    # Clears data and registers and logins user_1, user_2, and user_3
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the three registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]
    u_id2 = token_id_dict2["auth_user_id"]

    # Create Channel_1 made by user_1, get its id, and invite user_2
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]
    channel_invite_v1(token1, channel_1_id, u_id2)

    # Made an invalid token for joiner
    invalid_token = token1 + "rkbgesorgbv#$%"

    # Conditions leads to an access error outcome and tests for it
    with pytest.raises(AccessError):
        channel_addowner_v1(invalid_token, channel_1_id, u_id2)


# Case 6 - tests for global owner exception
#          expected outcome is user with u_id becomes owner
# Occurs when add owner function is called by global owner
def test_channel_addowner_v1_globalOwner():
    # Clears data and registers and logins user_1, user_2, and user_3
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")
    auth_register_v1("hah2@gmail.com", "9uisbxh83h", "Tom", "Green")

    # login the three registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token_id_dict3 = auth_login_v1("hah2@gmail.com", "9uisbxh83h")
    token1 = token_id_dict1["token"]
    token2 = token_id_dict2["token"]
    u_id3 = token_id_dict3["auth_user_id"]

    # Create Channel_1 made by user_2, get its id, and invite user_3
    channel_1_id = channels_create_v1(token2, "channelone", True)["channel_id"]
    channel_invite_v1(token2, channel_1_id, u_id3)

    # Calls addowner function for testing by global owner
    # Expected output is user_3 becomes owner
    channel_addowner_v1(token1, channel_1_id, u_id3)

    # Calls details function for testing
    output = channel_details_v1(token2, channel_1_id)

    assert output["all_members"][0]["name_first"] == 'Tom'
    assert output["all_members"][1]["name_first"] == 'Tom'
    assert output["owner_members"][0]["name_first"] == 'Tom'
    assert output["owner_members"][1]["name_first"] == 'Tom'
    assert output["name"] == "channelone"
    assert output["is_public"] == True
    assert len(output["all_members"]) == 2
    assert len(output["owner_members"]) == 2


"""
Author : Emir Aditya Zen

This file is for testing channel_removeowner_v1 function implementation

Background
Remove user with user id u_id an owner of this channel

Parameters: (token, channel_id, u_id)
Return Type: {}

InputError:
- channel_id does not refer to a valid channel.
- user with u_id is not an owner of the channel.
- user is currently the only owner

AccessError:
- The authorised user is not owner of dreams or channel
- The function is called with an invalid token
"""


#############################################################################
#                                                                           #
#                    Test for channel_removeowner_v1                        #
#                                                                           #
#############################################################################

# Case 1 - tests for valid function implementation
#          expected outcome is user becomes member and output is {}
# Occurs when channel and token is valid, user calling function is authorised
def test_channel_removeowner_v1_success():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]
    u_id2 = token_id_dict2["auth_user_id"]

    # Create Channel_1 made by user_1, get its id, and invite user2
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]
    channel_invite_v1(token1, channel_1_id, u_id2)

    # Calls addowner followed by remove owner function for testing
    # Expected output is user_2 becomes owner then back to member
    channel_addowner_v1(token1, channel_1_id, u_id2)
    channel_removeowner_v1(token1, channel_1_id, u_id2)

    # Calls details function for testing
    output = channel_details_v1(token1, channel_1_id)

    assert output["all_members"][0]["name_first"] == 'Peter'
    assert output["all_members"][1]["name_first"] == 'Tom'
    assert output["owner_members"][0]["name_first"] == 'Peter'
    assert output["name"] == "channelone"
    assert output["is_public"] == True
    assert len(output["all_members"]) == 2
    assert len(output["owner_members"]) == 1


# Case 2 - tests for input error due to invalid channel
#          expected outcome is input error
# Occurs when channel id used is invalid
def test_channel_removeowner_v1_inputErrorChannel():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]
    u_id2 = token_id_dict2["auth_user_id"]

    # Create Channel_1 made by user_1, get its id, and invite user2 and make him owner
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]
    channel_invite_v1(token1, channel_1_id, u_id2)
    channel_addowner_v1(token1, channel_1_id, u_id2)

    # Made an invalid channel id for testing
    channel_1_invalidid = channel_1_id + 300

    # Conditions leads to an input error outcome and tests for it
    with pytest.raises(InputError):
        channel_removeowner_v1(token1, channel_1_invalidid, u_id2)


# Case 3 - tests for input error due to function called for a member
#          expected outcome is input error
# Occurs when remove owner function is called to an existing member
def test_channel_removeowner_v1_inputErrorMember():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]
    u_id2 = token_id_dict2["auth_user_id"]

    # Create Channel_1 made by user_1, get its id, and invite user2
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]
    channel_invite_v1(token1, channel_1_id, u_id2)

    # Conditions leads to an input error outcome and tests for it
    with pytest.raises(InputError):
        channel_removeowner_v1(token1, channel_1_id, u_id2)


# Case 4 - tests for input error due to function called for single owner
#          expected outcome is input error
# Occurs when remove owner function is called to a channel with single owner
def test_channel_removeowner_v1_inputErrorOnlyOwner():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]
    token2 = token_id_dict2["token"]
    u_id2 = token_id_dict2["auth_user_id"]

    # Create Channel_1 made by user_2, get its id
    channel_1_id = channels_create_v1(token2, "channelone", True)["channel_id"]

    # Conditions leads to an input error outcome and tests for it
    with pytest.raises(InputError):
        channel_removeowner_v1(token1, channel_1_id, u_id2)


# Case 5 - tests for access error due to non authorised user
#          expected outcome is input error
# Occurs when remove owner function is by a member of channel who is not a global owner
def test_channel_removeowner_v1_accessError1():
    # Clears data and registers and logins user_1, user_2, and user_3
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")
    auth_register_v1("hah2@gmail.com", "9uisbxh83h", "Tom", "Green")

    # login the three registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token_id_dict3 = auth_login_v1("hah2@gmail.com", "9uisbxh83h")
    token1 = token_id_dict1["token"]
    token3 = token_id_dict3["token"]
    u_id2 = token_id_dict2["auth_user_id"]
    u_id3 = token_id_dict3["auth_user_id"]

    # Create Channel_1 made by user_1, get its id, and invite user2
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]
    channel_invite_v1(token1, channel_1_id, u_id2)
    channel_invite_v1(token1, channel_1_id, u_id3)
    channel_addowner_v1(token1, channel_1_id, u_id2)

    # Conditions leads to an access error outcome and tests for it
    with pytest.raises(AccessError):
        channel_removeowner_v1(token3, channel_1_id, u_id2)


# Case 6 - tests for access error due invalid token
#          expected outcome is access error
# Occurs when add owner function is called using invalid token
def test_channel_removeowner_v1_accessErrorToken1():
    # Clears data and registers and logins user_1, user_2, and user_3
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the three registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]
    u_id2 = token_id_dict2["auth_user_id"]

    # Create Channel_1 made by user_1, get its id, and invite user_2
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]
    channel_invite_v1(token1, channel_1_id, u_id2)
    channel_addowner_v1(token1, channel_1_id, u_id2)

    # Made an invalid token for joiner
    invalid_token = token1 + "rkbgesorgbv#$%"

    # Conditions leads to an access error outcome and tests for it
    with pytest.raises(AccessError):
        channel_removeowner_v1(invalid_token, channel_1_id, u_id2)
    with pytest.raises(AccessError):
        channel_removeowner_v1("invalid_token", channel_1_id, u_id2)
    with pytest.raises(AccessError):
        channel_removeowner_v1(None, channel_1_id, u_id2)


# Case 7 - tests for global owner exception
#          expected outcome is user with u_id becomes owner
# Occurs when add owner function is called by global owner
def test_channel_removeowner_v1_accessError2():
    # Clears data and registers and logins user_1, user_2, and user_3
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")
    auth_register_v1("test2@testexample.com", "wp01^#$dp1o23", "Tom2", "Green2")

    # login the three registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token_id_dict3 = auth_login_v1("test2@testexample.com", "wp01^#$dp1o23")

    token1 = token_id_dict1["token"]
    token3 = token_id_dict3["token"]

    u_id2 = token_id_dict2["auth_user_id"]

    # Create Channel_1 made by user_1, get its id, and invite user_2
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]
    channel_invite_v1(token1, channel_1_id, u_id2)
    channel_addowner_v1(token1, channel_1_id, u_id2)

    with pytest.raises(AccessError):
        channel_removeowner_v1(token3, channel_1_id, u_id2)


"""
Author : Emir Aditya Zen

This file is for testing channel_leave_v1 function implementation

Background
Given a channel ID, the user removed as a member of this channel.
Their messages should remain in the channel

HTTP Method: POST
Parameters: (token, channel_id)
Return Type: {}

InputError:
- channel_id does not refer to a valid channel.

AccessError:
- The authorised user is not a member of channel with channel_id
- Function is called with an invalid token
"""


#############################################################################
#                                                                           #
#                       Test for channel_leave_v1                           #
#                                                                           #
#############################################################################

# Case 1 - tests for valid function implementation
#          expected outcome is user leaves channel with output {}
# Occurs when channel and token is valid, user calling function is inside channel
def test_channel_leave_joined_user():
    # Clears data and registers user1 and user2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    dict_user1 = auth_login_v1("haha@gmail.com", "123123123")
    dict_user2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = dict_user1["token"]
    token2 = dict_user2["token"]
    u_id2 = dict_user2["auth_user_id"]

    # Create channel made by user1, get its id, and invite user2
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]
    channel_invite_v1(token1, channel_1_id, u_id2)

    # Calls channel_leave for testing
    # Expected output is user2 leaves channel
    channel_leave_v1(token2, channel_1_id)

    # Calls details function for checking user 2 is not a channel member
    output = channel_details_v1(token1, channel_1_id)
    assert output["all_members"][0]["name_first"] == 'Peter'
    assert output["owner_members"][0]["name_first"] == 'Peter'
    assert output["name"] == "channelone"
    assert output["is_public"] is True
    assert len(output["all_members"]) == 1
    assert len(output["owner_members"]) == 1


def test_channel_leave_owner():
    # Clears data and registers user1 and user2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    dict_user1 = auth_login_v1("haha@gmail.com", "123123123")
    dict_user2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = dict_user1["token"]
    token2 = dict_user2["token"]
    u_id2 = dict_user2["auth_user_id"]

    # Create channel made by user1, get its id, and invite user2
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]
    channel_invite_v1(token1, channel_1_id, u_id2)

    # Calls channel_leave for testing
    # Expected output is user2 leaves channel
    channel_leave_v1(token1, channel_1_id)

    output = channel_details_v1(token2, channel_1_id)
    assert output["all_members"][0]["name_first"] == 'Tom'
    assert output["owner_members"][0]["name_first"] == 'Tom'
    assert output["name"] == "channelone"
    assert output["is_public"] is True
    assert len(output["all_members"]) == 1
    assert len(output["owner_members"]) == 1


# Case 2 - tests for input error due to invalid channel
#          expected outcome is input error
# Occurs when channel id used is invalid
def test_channel_leave_v1_inputErrorChannel():
    # Clears data and registers user1 and user2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    dict_user1 = auth_login_v1("haha@gmail.com", "123123123")
    dict_user2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = dict_user1["token"]
    token2 = dict_user2["token"]
    u_id2 = dict_user2["auth_user_id"]

    # Create channel made by user1, get its id and invites user2
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]
    channel_invite_v1(token1, channel_1_id, u_id2)

    # Made invalid channel id and test for input error when it is used
    channel_1_invalidid = channel_1_id + 300
    with pytest.raises(InputError):
        channel_leave_v1(token2, channel_1_invalidid)


# Case 3 - tests for access error due to user not in channel
#          expected outcome is access error
# Occurs when channel_leave is called by a user not in the specified channel
def test_channel_leave_v1_accessError():
    # Clears data and registers user1 and user2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    dict_user1 = auth_login_v1("haha@gmail.com", "123123123")
    dict_user2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = dict_user1["token"]
    token2 = dict_user2["token"]

    # Create channel made by user1, get its id
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]

    # Tests for access error when function is called by a non member
    with pytest.raises(AccessError):
        channel_leave_v1(token2, channel_1_id)


# Case 4 - tests for access error due to invalid token
#          expected outcome is access error
# Occurs when channel_leave is called with an invalid token
def test_channel_leave_v1_accessErrorToken():
    # Clears data and registers user1 and user2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    dict_user1 = auth_login_v1("haha@gmail.com", "123123123")
    dict_user2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = dict_user1["token"]
    token2 = dict_user2["token"]
    u_id2 = dict_user2["auth_user_id"]

    # Create channel made by user1, get its id
    channel_1_id = channels_create_v1(token1, "channelone", True)["channel_id"]
    channel_invite_v1(token1, channel_1_id, u_id2)

    # Made invalid token and test for access error when it is used
    invalid_token = token2 + "rkbgesorgbv#$%"
    with pytest.raises(AccessError):
        channel_leave_v1(invalid_token, channel_1_id)
    clear_v1()
