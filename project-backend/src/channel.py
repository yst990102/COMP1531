from src.data_file import Channel, User, data, Permission, Notification, current_time
from src.error import InputError, AccessError
from src.auth import session_to_token, token_to_session, get_user_by_token, auth_register_v1, \
    auth_login_v1
from typing import Dict, Union
#############################################################################
#                                                                           #
#                           Interface function                              #
#                                                                           #
#############################################################################

"""
Author: Emir Aditya Zen

Background
Invites a user (with user id u_id) to join a channel with ID channel_id.
Once invited the user is added to the channel immediately

Parameters: (auth_user_id, channel_id, u_id)
Return Type: {}

InputError:
- channel_id does not refer to a valid channel.
- u_id does not refer to a valid user

AccessError:
- the authorised user is not already a member of the channel

"""


def channel_invite_v1(token: str, channel_id: int, u_id: int) -> Dict:
    # Case 1 error checks
    # Checks for cases of InputError indicated by invalid channel_id or u_id
    # In addition, checks for cases of AccessError indicated by authorised user calling
    # channel_invite_v1 function into a channel he is not part in
    error_check(channel_id, u_id, token)
    inviter = get_user_by_token(token)
    # Case 2 no error occurs but user invited is already part of channel
    # Expected outcome is channel_invite_v1 function will just ignore the second
    # invitation call
    invitee = get_user_by_u_id(u_id)
    channel = get_channel_by_channel_id(channel_id)
    if channel not in invitee.part_of_channel:
        # Case 3 succesfull function calling
        # Expected outcome is invited user is now a member of the channel specified
        add_user_into_channel(channel, invitee)

    # add notification
    notification_message = f"{inviter.handle_str} added you to {channel.name}"
    notification = Notification(channel.channel_id, -1, notification_message)
    invitee.notifications.append(notification)

    # update user's stats
    update_channel_user_stat(invitee)
    return {}


"""
Author : Emir Aditya Zen

Background
Given a Channel with ID channel_id that the authorised user
is part of, provide basic details about the channel

Parameters: (auth_user_id, channel_id)
Return Type: {name, owner_members, all_members}

InputError:
- channel_id does not refer to a valid channel.

AccessError:
- Authorised user is not a member of channel with channel_id

"""


def channel_details_v1(token: str, channel_id: int) -> Dict:
    # Case 1 InputError checks
    # Checks for cases of InputError indicated by invalid channel_id
    channel = get_channel_by_channel_id(channel_id)
    if channel is None:
        raise InputError(description="Channel_id does not refer to a valid channel")

    # Case 2 AccessError checks
    # Checks for cases of AccessError indicated by authorised user calling
    # channel_invite_v1 function into a channel he is not part in
    sender = get_user_by_token(token)
    if sender is None:
        # the token given is invalid
        raise AccessError(description="token is invalid")

    # check if the sender is in the channel
    sender_in_channel = is_user_in_channel(channel_id, sender.auth_user_id)
    if sender_in_channel is None:
        raise AccessError(description="The authorised user is not a member of the channel")

    # Case 3 succesfull function calling
    # Expected outcome is function return basic details on the channel
    # he/she is in through a dictionary form
    owner_list = []
    member_list = []
    for owner in channel.owner_members:
        owner_list.append(owner.return_type_user_v2())

    for member in channel.all_members:
        member_list.append(member.return_type_user_v2())

    return {
        'name': channel.name,
        'is_public': channel.is_public,
        'owner_members': owner_list,
        'all_members': member_list
    }


"""
Author : Shi Tong Yuan

Background
Given a Channel with ID channel_id that the authorised user is part of, return up to 50 messages between index "start" and "start + 50". Message with index 0 is the most recent message in the channel. This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the channel, returns -1 in "end" to indicate there are no more messages to load after this return.

Parameters: (auth_user_id, channel_id, start)
Return Type: {messages, start, end}

InputError:
- Channel ID is not a valid channel
- start is greater than the total number of messages in the channel

AccessError:
- Authorised user is not a member of channel with channel_id

"""


def channel_messages_v1(token: str, channel_id: int, start: int) -> Dict:
    # Input error when channel_id does not refer to an existing channel.
    channel = get_channel_by_channel_id(channel_id)
    if channel is None:
        raise InputError(description="channel_id does not refer to a valid or exising dm")
    # Input error when start is greater than the total number of messages in the channel
    if start > len(channel.messages):
        raise InputError(description="start is greater than the total number of messages in the channel")

    # Access error when Authorised user is not a member of channel with channel_id
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token is invalid")
    elif channel not in user.part_of_channel:
        raise AccessError(description="The authorised user is not already a member of the channel")

    return_message = []
    counter_start = len(channel.messages) - start - 1
    if (counter_start + 1) - 50 > 0:
        counter_end = (counter_start + 1) - 50
        end = start + 50
    else:
        counter_end = 0
        end = -1
    while counter_start >= counter_end:
        msg = channel.messages[counter_start].return_type_message_v2()
        if user.u_id in msg['reacts'][0]['u_ids']:
            msg['reacts'][0]['is_this_user_reacted'] = True
        else:
            msg['reacts'][0]['is_this_user_reacted'] = False
        return_message.append(msg)
        counter_start -= 1

    return {
        'messages': return_message,
        'start': start,
        'end': end
    }


"""
Author : Shi Tong Yuan

Background
Given a channel_id of a channel that the authorised user can join, adds them to that channel

Parameters: (auth_user_id, channel_id)
Return Type: {}

InputError:
- Channel ID is not a valid channel

AccessError:
- channel_id refers to a channel that is private (when the authorised user is not a global owner)

"""


def channel_join_v1(token: str, channel_id: int) -> Dict:
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token passed in is invalid")

    target_channel = get_channel_by_channel_id(channel_id)
    if target_channel is None:
        raise (InputError(description="channel_join_v1 : invalid channel_id."))

    if target_channel.is_public is False and user.permission_id != Permission.global_owner:
        raise (AccessError(description="channel_join_v1 : channel is PRIVATE."))

    add_user_into_channel(target_channel, user)

    # update user's stats
    update_channel_user_stat(user)
    return {}


"""
Author : Emir Aditya Zen

Background
Given a channel ID, the user removed as a member of this channel. 
Their messages should remain in the channel

Parameters: (token, channel_id)
Return Type: {}

InputError:
- channel_id does not refer to a valid channel.

AccessError:
- Authorised user is not a member of channel with channel_id
- token is invalid

"""


def channel_leave_v1(token: str, channel_id: int) -> Dict:
    # Get channel and user
    channel = get_channel_by_channel_id(channel_id)
    user = get_user_by_token(token)
    u_id = token_into_u_id(token)

    # Case 1 InputError checks
    # Checks for cases of InputError indicated by invalid channel_id
    if channel is None:
        raise InputError(description="Channel_id does not refer to a valid channel")

    # Case 2 AccessError checks
    # Checks if token is invalid and user is in channel specified
    if user is None:
        raise AccessError(description="token is invalid")
    else:
        if is_user_in_channel(channel_id, u_id) is None:
            raise AccessError(description="User is not in channel specified")

    # Case 3 succesfull function calling
    # Expected outcome is user leaves channel
    user_leaves_channel(channel, user, u_id, channel_id)

    # update user's stats
    update_channel_user_stat(user)
    return {}


"""
Author : Emir Aditya Zen

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


def channel_addowner_v1(token: str, channel_id: int, u_id: int) -> Dict:
    # Case 1 InputError checks
    # Checks for cases of InputError indicated by invalid channel_id
    channel = get_channel_by_channel_id(channel_id)
    if channel is None:
        raise InputError(description="Channel_id does not refer to a valid channel")

    # Checks for cases of InputError indicated by user with u_id being an owner already
    if is_user_owner_channel(channel_id, u_id) is not None:
        raise InputError(description="User is already an owner")
    # Check if the user to be added as owner is in the channel
    if is_user_in_channel(channel_id, u_id) is None:
        raise InputError(description="The user to be added as owner is not in the channel")

    # Case 2 AccessError checks
    # Checks if token is invalid
    sender = get_user_by_token(token)
    if sender is None:
        # the token given is invalid
        raise AccessError(description="token is invalid")

    # check if the sender is owner of the channel or a global owner
    sender_in_channel = is_user_owner_channel(channel_id, sender.auth_user_id)
    if sender_in_channel is None and sender.permission_id != Permission.global_owner:
        raise AccessError(description="The authorised user is not an owner of the channel, and not the global owner")

    # Case 3 succesfull function calling
    # Expected outcome is user with u_id becomes an owner of the channel
    owner_added = get_user_by_u_id(u_id)
    add_user_into_owner_channel(channel, owner_added)

    return {}


"""
Author : Emir Aditya Zen

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


def channel_removeowner_v1(token: str, channel_id: int, u_id: int) -> Dict:
    # Case 1 InputError checks
    # Checks for cases of InputError indicated by invalid channel_id
    channel = get_channel_by_channel_id(channel_id)
    if channel is None:
        raise InputError(description="Channel_id does not refer to a valid channel")

    # Checks for cases of InputError indicated by user with u_id is not an owner of channel
    if is_user_owner_channel(channel_id, u_id) is None:
        raise InputError(description="User is not an owner")

    # Checks if the user is currently the only owner
    if len(channel.owner_members) == 1:
        raise InputError(description="User is the only owner")

    # Case 2 AccessError checks
    # Checks if token is invalid
    sender = get_user_by_token(token)
    if sender is None:
        # the token given is invalid
        raise AccessError(description="token is invalid")

    # check if the sender is owner of the channel or a global owner
    sender_in_channel = is_user_owner_channel(channel_id, sender.auth_user_id)
    if sender_in_channel is None and sender.permission_id != Permission.global_owner:
        raise AccessError(description="The authorised user is not an owner of the channel")

    # Case 3 succesfull function calling
    # Expected outcome is user with u_id becomes an owner of the channel
    owner_remove = get_user_by_u_id(u_id)
    remove_user_from_owner_channel(channel, owner_remove)
    return {}


#############################################################################
#                                                                           #
#                              Helper function                              #
#                                                                           #
#############################################################################


def get_channel_by_channel_id(channel_id: int) -> Union[Channel, None]:

    if (not isinstance(channel_id, int)) or channel_id >= data['channel_num']:
        return None
    for channel in data['class_channels']:
        if channel.channel_id == channel_id:
            return channel

    return None


# Function checking if user exists in current data
# Return user dictionary if it exists and if not return None
def get_user_by_u_id(u_id: int) -> Union[User, None]:
    for user in data["class_users"]:
        if u_id == user.u_id:
            return user
    else:
        return None


# check if the user is a member of channel
def is_user_in_channel(channel_id: int, auth_user_id: int) -> Union[User, None]:
    channel = get_channel_by_channel_id(channel_id)
    for user in channel.all_members:
        if auth_user_id == user.auth_user_id:
            return user
    return None


# Checks if function channel_invite_v1 will generate an error
def error_check(channel_id: int, u_id: int, token: str) -> None:
    # Checking for InputError
    # error_test1 and error_test2 checks if channel and user is valid or not
    # if user or channel is invalid throw inputError
    channel_ = get_channel_by_channel_id(channel_id)
    if channel_ is None:
        raise InputError(description="Channel_id does not refer to a valid channel")

    invitee = get_user_by_u_id(u_id)
    if invitee is None:
        raise InputError(description="u_id does not refer to a valid user")

    # Checking for AccessError
    # error_test3 checks if user inviting the other user is in the channel
    sender = get_user_by_token(token)
    if sender is None:
        # the token given is invalid
        raise AccessError(description="token is invalid")

    # check if the sender is in the channel
    sender_in_channel = is_user_in_channel(channel_id, sender.auth_user_id)
    if sender_in_channel is None:
        raise AccessError(description="The authorised user is not a member of the channel")


# Function adding user into specified channel and adds that channel into user class
def add_user_into_channel(channel: Channel, invitee: User) -> None:
    invitee.part_of_channel.append(channel)
    channel.all_members.append(invitee)


# check if the user is an owner of channel
def is_user_owner_channel(channel_id: int, auth_user_id: int) -> Union[User, None]:
    channel = get_channel_by_channel_id(channel_id)
    for owner in channel.owner_members:
        if auth_user_id == owner.auth_user_id:
            return owner
    return None


# Function making user into specified channel owner and adds that channel into user class
def add_user_into_owner_channel(channel: Channel, owner: User) -> None:
    owner.channel_owns.append(channel)
    channel.owner_members.append(owner)


# Function making user into specified channel member from owner
def remove_user_from_owner_channel(channel: Channel, owner: User) -> None:
    owner.channel_owns.remove(channel)
    channel.owner_members.remove(owner)
    # If the leaving owner is the only one owner and there is still member in the dm
    # Then first availble person in member become owner
    if len(channel.owner_members) == 0 and len(channel.all_members) > 0:
        next_owner = channel.all_members[0]
        channel.owner_members.append(next_owner)
        next_owner.channel_owns.append(channel)


def user_leaves_channel(channel: Channel, user: User, u_id: int, channel_id: int) -> None:
    user.part_of_channel.remove(channel)
    channel.all_members.remove(user)
    if is_user_owner_channel(channel_id, u_id) is not None:
        remove_user_from_owner_channel(channel, user)


def token_into_u_id(token: str) -> Union[int, None]:
    user = get_user_by_token(token)
    if user is None:
        return None
    u_id = user.u_id
    return u_id


# update user's stats about channel joined
def update_channel_user_stat(user: User) -> None:
    stat_channel_user = {
        'num_channels_joined': len(user.part_of_channel),
        'time_stamp': current_time()
    }
    user.channels_joined.append(stat_channel_user)


# update Dreams stats about channels
def update_channel_dreams_stat() -> None:
    stat_channel = {
        'num_channels_exist': len(data['class_channels']),
        'time_stamp': current_time()
    }
    data['channels_exist'].append(stat_channel)
