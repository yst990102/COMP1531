# channels.py is used to implement the functions for channels
# including channels_list and chennels_listall
# for 21T1 COMP1531 project
from src.auth import auth_login_v1, auth_register_v1, session_to_token, token_to_session, \
    get_user_by_token
from src.error import InputError, AccessError
from src.data_file import Channel, data
from src.channel import update_channel_user_stat, update_channel_dreams_stat
from typing import Dict
#############################################################################
#                                                                           #
#                               Channels_list_v1                            #
#                                                                           #
#############################################################################
"""
Author: Zheng Roger Luo
Background :
Provide a list of all channels (both public and private channels)
(and their associated details) that the authorised user is part of.

Parameters:(auth_user_id)
Return Type:{channels}

"""


def channels_list_v1(token: str) -> Dict:
    # Pull the data of user from data_file
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="user does not refer to a vaild user")
    # Call return_type_channel(self) in order to get dictionary return
    list_return = []
    for channel in user.part_of_channel:
        list_return.append(channel.return_type_channel())
    return {
        'channels': list_return
    }


#############################################################################
#                                                                           #
#                           Channels_listall_v1                             #
#                                                                           #
#############################################################################
"""
Author: Zheng Roger Luo
Background :
Provide a list of all channels (and their associated details) 
regardless who calls, or owns it.

Parameters:(auth_user_id)
Return Type:{channels}
"""


def channels_listall_v1(token: str) -> Dict:
    # Pull the data of user from data_file
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="user does not refer to a vaild user")
    list_return = []
    for i in data['class_channels']:
        list_return.append(i.return_type_channel())
    return {
        'channels': list_return
    }

#############################################################################
#                                                                           #
#                           channels_create_v1                             #
#                                                                           #
#############################################################################


"""
Author: Lan Lin
Background :
Creates a new channel with that name that is either a public or private channel

Parameters: auth_user_id, name, is_public
Return Type: { channel_id }
"""


def create_channel_id() -> int:
    new_id = data['channel_num']
    data['channel_num'] = data['channel_num'] + 1
    return new_id


def channels_create_v1(token: str, name: str, is_public: bool) -> Dict:
    # error check that the name is more than 20 characters
    if len(name) > 20:
        raise InputError(description='Error! Name is more than 20 characters')
    if not isinstance(is_public, bool):
        raise InputError(description='is_public has to be bool')
    # error check if the owner has registered
    owner = get_user_by_token(token)
    if owner is None:
        raise AccessError(description='The token is invalid, or the owner has not registered')

    # get the owner who creates the channel by auth_user_id
    channel_id = create_channel_id()
    channel = Channel(name, channel_id, is_public)
    data['class_channels'].append(channel)
    owner.part_of_channel.append(channel)
    owner.channel_owns.append(channel)
    channel.owner_members.append(owner)
    channel.all_members.append(owner)

    # update user's stats
    update_channel_user_stat(owner)
    # update Dreams' stats
    update_channel_dreams_stat()

    return {
        'channel_id': channel_id
    }
