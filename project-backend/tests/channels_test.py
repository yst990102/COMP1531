# channels_test.py is used to test the file called channels
# for 21T1 COMP1531 project
# Written by Zheng Luo (z5206267@ad.unsw.edu.au) on 28/Feb/2021
# Updated for iteration 2 by : Emir Aditya Zen

import pytest
from src.auth import auth_login_v1, auth_register_v1
from src.channel import channel_invite_v1, channel_details_v1, channel_join_v1, channel_messages_v1
from src.channels import channels_list_v1, channels_create_v1, channels_listall_v1
from src.error import InputError, AccessError
from src.other import clear_v1

#############################################################################
#                                                                           #
#                       Test for channels_list_v1                           #
#                                                                           #
#############################################################################
"""
This file is for testing channels_list_v1 function implementation

Background
Provide a list of all channels (and their associated details) that the 
authorised user is a part of

Parameters:(token)
Return Type:{channels}

TEST CASES:
	-check the correctness of channel that the authorised user is belonged to.
	-check the detail and amount of channels for return

AccessError:
- The function is called with an invalid token
"""


def test_channels_correct_channel():
    clear_v1()
    # Initiate a user
    auth_register_v1("ZhengRogerLuo@gmail.com", "happysheepQAQ", "Zheng", "Luo")
    login1 = auth_login_v1("ZhengRogerLuo@gmail.com", "happysheepQAQ")
    token1 = login1['token']

    # Create a channel and get its ID
    channels_create_v1(token1, "SheepChannel", is_public=True)

    # List the channel of this user belongs to
    channel_list = channels_list_v1(token1)

    # Check the information of authorised user is correct
    assert (channel_list['channels'][0]['name'] == 'SheepChannel')


def test_channels_multiple_channels():
    clear_v1()
    # Initiate a user
    auth_register_v1("UNSWIsTheBest@gmail.com", "happyEveryday!", "Ian", "J")
    login1 = auth_login_v1("UNSWIsTheBest@gmail.com", "happyEveryday!")
    token1 = login1['token']

    # Create multiple channels and get its id
    channels_create_v1(token1, "EngineeringChannel", is_public=True)
    channels_create_v1(token1, "BussinessChannel", is_public=True)
    channels_create_v1(token1, "LawChannel", is_public=True)

    # List the channel of this user belongs to
    channel_list = channels_list_v1(token1)

    # Check the information of authorised user is correct
    assert (channel_list['channels'][0]['name'] == "EngineeringChannel")
    assert (channel_list['channels'][1]['name'] == "BussinessChannel")
    assert (channel_list['channels'][2]['name'] == "LawChannel")


def test_channels_multiple_users():
    clear_v1()
    # Initiate multiple users
    auth_register_v1("ILoveTrimester@gmail.com", "NoStressAtAll", "Iannnn", "J")
    auth_register_v1("IHateSemester@gmail.com", "BreakIsTooLong", "Ben", "A")
    login1 = auth_login_v1("ILoveTrimester@gmail.com", "NoStressAtAll")
    login2 = auth_login_v1("IHateSemester@gmail.com", "BreakIsTooLong")
    token1 = login1['token']
    token2 = login2['token']
    u_id2 = login2['auth_user_id']

    # Create a channel by register 1 and invites register 2
    channel_id1 = channels_create_v1(token1, "mesterChannel", is_public=True)['channel_id']
    channel_invite_v1(token1, channel_id1, u_id2)

    # List the channel of first user belongs to
    channel_user1 = channels_list_v1(token1)
    # List the channel of second user belongs to
    channel_user2 = channels_list_v1(token2)

    # Check the information of authorised user is correct
    assert (channel_user1['channels'][0]['name'] == "mesterChannel")
    assert (channel_user2['channels'][0]['name'] == "mesterChannel")


def test_channels_oneUser_multiple_private_channels():
    clear_v1()
    # Initiate a user
    auth_register_v1("ILoveTrimester@gmail.com", "NoStressAtAll", "Iannnn", "J")
    login1 = auth_login_v1("ILoveTrimester@gmail.com", "NoStressAtAll")
    token1 = login1['token']
    # Create 2 private channels and 2 public channels
    channels_create_v1(token1, "ChannelAPublic", is_public=True)
    channels_create_v1(token1, "ChannelBPublic", is_public=True)
    channels_create_v1(token1, "ChannelCPrivate", is_public=False)
    channels_create_v1(token1, "ChannelDPrivate", is_public=False)
    # List all the public channel of the user belongs to
    channel_user1 = channels_list_v1(token1)
    # Check the information of authorised user is correct
    assert len(channel_user1['channels']) == 4


def test_channels_invalidToken():
    clear_v1()
    # Initiate a user
    auth_register_v1("ILoveTrimester@gmail.com", "NoStressAtAll", "Iannnn", "J")
    login1 = auth_login_v1("ILoveTrimester@gmail.com", "NoStressAtAll")
    token1 = login1['token']

    # Create a channel and get its ID
    channels_create_v1(token1, "SheepChannel", is_public=True)

    # Made an invalid token for user 1
    invalid_token = ''.join([token1, "rkbgesorgbv#$%"])

    # Test conditions leading to an access error outcome
    with pytest.raises(AccessError):
        channels_list_v1(invalid_token)


#############################################################################
#                                                                           #
#                       Test for channels_listall_v1                        #
#                                                                           #
#############################################################################
"""
This file is for testing channels_listall_v1 function implementation

Background:
Provide a list of all channels (and their associated details)

Explaination:
channel_listall_v1 should list all channels, 
including those that are private, regardless of who calls it.

Parameters:(token)
Return Type:{channels}

TEST CASES:
	-check the correctness of channel that the authorised user is belonged to.
	-check the detail and amount of channels for return

AccessError:
- The function is called with an invalid token
"""


def test_allchannels_correct_channel():
    clear_v1()
    # Initiate a user
    auth_register_v1("ZhengRogerLuo@gmail.com", "happysheepQAQ", "Zheng", "Luo")
    login1 = auth_login_v1("ZhengRogerLuo@gmail.com", "happysheepQAQ")
    token1 = login1['token']

    # Create a channel and get its ID
    channels_create_v1(token1, "SheepChannel", is_public=True)

    # List all the channels and check
    assert (len(channels_listall_v1(token1)) == 1)


def test_allchannels_multiple_channels():
    clear_v1()
    # Initiate a user
    auth_register_v1("UNSWIsTheBest@gmail.com", "happyEveryday!", "Ian", "J")
    login1 = auth_login_v1("UNSWIsTheBest@gmail.com", "happyEveryday!")
    token1 = login1['token']

    # Create multiple channels
    channels_create_v1(token1, "EngineeringChannel", is_public=True)
    channels_create_v1(token1, "BussinessChannel", is_public=True)
    channels_create_v1(token1, "LawChannel", is_public=True)

    # List all the channels and check
    channel_user = channels_listall_v1(token1)
    assert channel_user['channels'][0]['name'] == "EngineeringChannel"
    assert channel_user['channels'][1]['name'] == "BussinessChannel"
    assert channel_user['channels'][2]['name'] == "LawChannel"
    assert len(channels_listall_v1(token1)['channels']) == 3

def test_invalid_token():
    clear_v1()
    with pytest.raises(AccessError):
        channels_listall_v1("invalid token")


def test_allchannels_multiple_users():
    clear_v1()
    # Initiate multiple users
    auth_register_v1("ILoveTrimester@gmail.com", "NoStressAtAll", "Iannnn", "J")
    auth_register_v1("IHateSemester@gmail.com", "BreakIsTooLong", "Ben", "A")
    login1 = auth_login_v1("ILoveTrimester@gmail.com", "NoStressAtAll")
    login2 = auth_login_v1("IHateSemester@gmail.com", "BreakIsTooLong")
    token1 = login1['token']
    token2 = login2['token']

    # Create two channels
    channels_create_v1(token1, "mesterChannel", is_public=True)
    channels_create_v1(token1, "mesterChannel2", is_public=True)

    # List all the channels and check it is correct from 2 user perspective
    # regardless if they are a member or not
    assert len(channels_listall_v1(token1)['channels']) == 2
    assert len(channels_listall_v1(token2)['channels']) == 2


def test_allchannels_private():
    clear_v1()
    # Initiate a user
    auth_register_v1("UNSWIsTheBest@gmail.com", "happyEveryday!", "Ian", "J")
    login1 = auth_login_v1("UNSWIsTheBest@gmail.com", "happyEveryday!")
    token1 = login1['token']

    # Create multiple channels both private and public
    channels_create_v1(token1, "EngineeringChannel", is_public=True)
    channels_create_v1(token1, "BussinessChannel", is_public=False)
    channels_create_v1(token1, "LawChannel", is_public=False)

    # List all the channels and check
    channel_user1 = channels_listall_v1(token1)
    assert channel_user1['channels'][0]['name'] == "EngineeringChannel"
    assert channel_user1['channels'][1]['name'] == "BussinessChannel"
    assert channel_user1['channels'][2]['name'] == "LawChannel"
    assert len(channels_listall_v1(token1)['channels']) == 3


# Test if the function will raise error
# if the token input is invalid
def test_listall_invalid_token():
    clear_v1()
    auth_register_v1("UNSWIsTheBest@gmail.com", "happyEveryday!", "Ian", "J")
    login1 = auth_login_v1("UNSWIsTheBest@gmail.com", "happyEveryday!")
    token1 = login1['token']

    # Create multiple channels both public and private
    channels_create_v1(token1, "EngineeringChannel", is_public=True)
    channels_create_v1(token1, "BussinessChannel", is_public=False)
    channels_create_v1(token1, "LawChannel", is_public=False)

    # Made an invalid token for user 1
    invalid_token = ''.join([token1, "rkbgesorgbv#$%"])

    # Test conditions leading to an access error outcome
    with pytest.raises(AccessError):
        channels_list_v1(invalid_token)


"""
Author: Lan Lin
Updated for iteration 2 by : Emir Aditya Zen

Tests for channels_create_v1 function implementation

Background:
Provide a list of all channels (and their associated details)

Explaination:
Creates a new channel with that name that is either a public
or private channel

Parameters:(token, name, is_public)
Return Type:{channel_id}

Tests content:
1. Channel's name is more than 20 characters
2. The input of is_public is bool
3. The function can successfully create channels
4. Access error due to invalid token
"""


#############################################################################
#                                                                           #
#                        Test for Channels_create_v1                        #
#                                                                           #
#############################################################################


# test if the name of the channel to be created is less than 20 characters
def test_channels_create_length_of_name():
    clear_v1()
    auth_register_v1('shaozhen@gmail.com', 'qwe1212', 'shaozhen', 'yan')
    user1 = auth_login_v1('shaozhen@gmail.com', 'qwe1212')
    token1 = user1['token']
    # check the length of name is more than 20 characters raises input error
    with pytest.raises(InputError):
        channels_create_v1(token1, 'A name clearly more than 20 characters', True)


# check the is_public is boolean or not
def test_channels_create_is_public_bool():
    clear_v1()
    auth_register_v1('shaozhen@gmail.com', 'qwe1212', 'shaozhen', 'yan')
    user1 = auth_login_v1('shaozhen@gmail.com', 'qwe1212')
    token1 = user1['token']
    with pytest.raises(InputError):
        channels_create_v1(token1, 'good_channel', 'not_a_bool')


# test if the channel has been created successfully
def test_channels_create_valid():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    login = auth_login_v1('haha@gmail.com', '123123123')
    token = login['token']

    channel1_id = channels_create_v1(token, "public_channel", True)['channel_id']
    channel2_id = channels_create_v1(token, "private_channel", False)['channel_id']

    channel_detail1 = channel_details_v1(token, channel1_id)
    channel_detail2 = channel_details_v1(token, channel2_id)
    assert channel_detail1['name'] == 'public_channel'
    assert channel_detail2['name'] == 'private_channel'
    owner1 = channel_detail1['owner_members'][0]
    member1 = channel_detail1['all_members'][0]
    owner2 = channel_detail1['owner_members'][0]
    member2 = channel_detail1['all_members'][0]
    assert owner1['email'] == owner2['email'] == member1['email'] == member2['email'] == 'haha@gmail.com'
    assert len(channels_list_v1(token)['channels']) == 2


# test if the function is called by invalid token causing access error
def test_channels_create_invalid_token():
    clear_v1()
    auth_register_v1('shaozhen@gmail.com', 'qwe1212', 'shaozhen', 'yan')
    user1 = auth_login_v1('shaozhen@gmail.com', 'qwe1212')
    token1 = user1['token']

    # Made an invalid token for user 1
    invalid_token = ''.join([token1, "rkbgesorgbv#$%"])

    # Test conditions leading to an access error outcome
    with pytest.raises(AccessError):
        channels_create_v1(invalid_token, "public_channel", True)
    clear_v1()
