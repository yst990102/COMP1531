from threading import Timer
import re
from src.data_file import Channel, DM, User, data, Message, Permission, current_time
from src.error import InputError, AccessError
from src.auth import get_user_by_token, get_user_by_handle, get_user_by_uid
from src.channel import get_channel_by_channel_id, is_user_owner_channel, is_user_in_channel
from src.dm import is_user_owner_dm, get_dm_by_dm_id, is_user_in_dm
from src.other import Notification
from typing import Dict, Union
#############################################################################
#                                                                           #
#                           Interface function                              #
#                                                                           #
#############################################################################
"""
Author: Shi Tong Yuan

message/send/v2

Background:
Send a message from authorised_user to the channel specified by channel_id. Note: Each message should have it's own unique ID. I.E. No messages should share an ID with another message, even if that other message is in a different channel.

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


def message_send_v2(token: str, channel_id: int, message: str) -> Dict:
    # error check
    auth_user, message, channel = helper_message_send_v2(token, channel_id, message)

    # if error check passed, create a new message id
    new_message_id = create_message_id()

    # bonus : replace <..> with asciimoji
    for i in auth_user.asciimoji.keys():
        message = message.replace(i, auth_user.asciimoji[i])

    # bonus: auth_user nudged a user in the channel by '#<user.handle_str>'
    message = return_nudged_user_in_channel_message(message, channel_id, auth_user)

    # send message to the channel
    helper2_message_send_v2(new_message_id, auth_user, message, channel)

    return {
        'message_id': new_message_id,
    }


"""
Author: Shi Tong Yuan

message/senddm/v1

Background:
Send a message from authorised_user to the DM specified by dm_id. Note: Each message should have it's own unique ID. 
I.E. No messages should share an ID with another message, even if that other message is in a different channel or DM.

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


def message_senddm_v1(token: str, dm_id: int, message: str) -> Dict:
    # error check
    auth_user, message, dm = helper_message_senddm_v1(token, dm_id, message)

    # if error check passed, create a new message id
    new_message_id = create_message_id()

    # bonus : replace <..> with asciimoji
    for i in auth_user.asciimoji.keys():
        message = message.replace(i, auth_user.asciimoji[i])

    # bonus: auth_user nudged a user in the channel by '#<user.handle_str>'
    message = return_nudged_user_in_dm_message(message, dm_id, auth_user)

    # send message to the dm
    helper2_message_senddm_v1(new_message_id, auth_user, message, dm)

    return {
        'message_id': new_message_id,
    }


"""
Author: Shi Tong Yuan

message/edit/v2

Background:
Given a message, update its text with new text. If the new message is an empty string, the message is deleted.

Parameters: (token, message_id, message)
Return Type: {}
HTTP Method: PUT

InputError:
    - (Added) Invalid token.
    - Length of message is over 1000 characters message_id refers to a deleted message
AccessError:
    - Message with message_id was sent by the authorised user making this request
    - The authorised user is an owner of this channel (if it was sent to a channel) or the **Dreams**

"""


def message_edit_v2(token: str, message_id: int, message: str) -> Dict:
    # InputError 1: invalid token.
    auth_user = get_user_by_token(token)
    if auth_user is None:
        raise AccessError(description='message_edit_v2 : Invalid token.')

    # InputError 1: Message is more than 1000 characters
    if len(message) > 1000:
        raise InputError(description='message_edit_v2 : Message is more than 1000 characters.')

    # if cannot find the channel or dm
    channel_dm = get_channel_dm_by_message_id(message_id)
    check_owner = None
    if channel_dm is None:
        raise InputError(description="The message is not in any channel or dm")
    if channel_dm[1] == 0:
        channel = channel_dm[0]
        check_owner = is_user_owner_channel(channel.channel_id, auth_user.u_id)
    if channel_dm[1] == 1:
        dm = channel_dm[0]
        check_owner = is_user_owner_dm(dm.dm_id, auth_user.u_id)

    # AccessError 1: Message editted by neither auth_user nor owner nor global owner.
    if auth_user.u_id != get_u_id_by_message_id(message_id) and check_owner is None and \
            auth_user.permission_id != Permission.global_owner:
        raise AccessError(description='message_edit_v2 : Message editted by neither auth_user nor owner '
                                      'nor global_owner.')

    # Case 1: if new message is empty string, delete it
    if message == "":
        message_remove_v1(token, message_id)
    # Case 2: else edit message
    else:
        # bonus : replace <..> with asciimoji
        message1 = message
        for _i in auth_user.asciimoji.keys():
            message1 = message.replace(_i, auth_user.asciimoji[_i])

        # bonus: auth_user nudged a user in the channel by '#<user.handle_str>'
        # tagging user
        if channel_dm[1] == 0:
            message1 = return_nudged_user_in_channel_message(message1, channel_dm[0].channel_id, auth_user)
            tagging_user(message, channel_dm[0].channel_id, -1, auth_user)
        if channel_dm[1] == 1:
            message1 = return_nudged_user_in_dm_message(message1, channel_dm[0].dm_id, auth_user)
            tagging_user(message, -1, channel_dm[0].dm_id, auth_user)

        get_message_by_message_id(message_id).message = message1

    return {}


"""
Author: Shi Tong Yuan

message/remove/v1

Background:
Given a message_id for a message, this message is removed from the channel/DM

Parameters: (token, message_id)
Return Type: {}
HTTP Method: DELETE

InputError:
    - (Added) Invalid token.
    - Message (based on ID) no longer exists
AccessError:
    - Message with message_id was sent by the authorised user making this request
    - The authorised user is an owner of this channel (if it was sent to a channel) or the **Dreams**

"""


def message_remove_v1(token: str, message_id: int) -> Dict:
    # InputError 1: invalid token.
    auth_user = get_user_by_token(token)
    if auth_user is None:
        raise AccessError(description='message_remove_v1 : Invalid token.')

    # InputError 2: Message (based on ID) no longer exists
    target_message = get_message_by_message_id(message_id)
    if target_message is None:
        raise InputError(description='message_remove_v1 : Message (based on ID) no longer exists.')

    # if cannot find the channel or dm
    channel_dm = get_channel_dm_by_message_id(message_id)
    print("channel_dm == ", channel_dm)
    check_owner = None
    if channel_dm is None:
        raise InputError(description="The message is not in any channel or dm")
    # if the message is in a channel
    elif channel_dm[1] == 0:
        channel = channel_dm[0]
        # check if the authorised user is the owner of the channel
        check_owner = is_user_owner_channel(channel.channel_id, auth_user.u_id)
    # if the message is in a dm
    elif channel_dm[1] == 1:
        dm = channel_dm[0]
        # check if the authorised user is the owner of the dm
        check_owner = is_user_owner_dm(dm.dm_id, auth_user.u_id)

    # AccessError 1: Message editted by neither auth_user nor owner nor global owner.
    if (auth_user.u_id != get_u_id_by_message_id(message_id) and check_owner is None and
            auth_user.permission_id != Permission.global_owner):
        raise AccessError(description='message_edit_v2 : Message editted by neither auth_user nor owner '
                                      'nor global_owner.')
    # delete_message_by_message_id(message_id)
    if channel_dm[1] == 0:
        channel_dm[0].messages.remove(target_message)
    if channel_dm[1] == 1:
        channel_dm[0].dm_messages.remove(target_message)

    auth_user.messages.remove(target_message)
    data['class_messages'].remove(target_message)

    # update Dreams stats about message
    update_message_dreams_stat()
    # update user's stats about message
    update_message_user_stat(auth_user)

    return {}


"""
Author: Shi Tong Yuan

message/share/v1

Background:
og_message_id is the original message. channel_id is the channel that the message is being shared to, 
and is -1 if it is being sent to a DM. dm_id is the DM that the message is being shared to, and is -1 if it is being
 sent to a channel. message is the optional message in addition to the shared message, and will be an empty string '' 
 if no message is given

Parameters: (token, og_message_id, message, channel_id, dm_id)
Return Type: {shared_message_id}
HTTP Method: POST

InputError:
    - (Added) if neither channel_id nor dm_id is -1 or both are -1

AccessError: 
    - the authorised user has not joined the channel or DM they are trying to share the message to

"""


def message_share_v1(token: str, og_message_id: int, message: str, channel_id: int, dm_id: int) -> Dict:
    if channel_id == -1 and dm_id != -1:
        mem_list = get_dm_by_dm_id(dm_id).dm_members
    elif channel_id != -1 and dm_id == -1:
        mem_list = get_channel_by_channel_id(channel_id).all_members
    elif channel_id != -1 and dm_id != -1:
        raise InputError(description="message_share_v1 : neither channel_id nor dm_id is -1.")
    elif channel_id == -1 and dm_id == -1:
        raise InputError(description="message_share_v1 : both channel_id and dm_id is -1.")

    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token is invalid")
    if user not in mem_list:
        raise AccessError(description="message_share_v1 : user need to be authorized.")

    og_message = get_message_by_message_id(og_message_id)
    message_added = f'{message}' \
                    f'"""' \
                    f'{og_message.message}' \
                    f'"""'

    # send shared message to the channel or dm
    message_id = None
    if channel_id != -1:
        message_id = message_send_v2(token, channel_id, message_added)['message_id']
    if dm_id != -1:
        message_id = message_senddm_v1(token, dm_id, message_added)['message_id']

    return {
        'shared_message_id': message_id
    }


"""
Auther: Lan Lin

Background: 
Send a message from authorised_user to the channel specified 
by channel_id automatically at a specified time in the future
"""


def message_sendlater_v1(token: str, channel_id: int, message: str, time_sent: int) -> Dict:
    # Type checking
    if type(channel_id) != int or type(message) != str or type(time_sent) != int:
        raise InputError(description="message_sendlater_v1 : incorrect type for your inputs.")

    auth_user = get_user_by_token(token)
    if auth_user is None:
        raise AccessError(description='Invalid token.')
    # InputError 1: Message is more than 1000 characters
    if len(message) > 1000:
        raise InputError(description='message_send_v2 : Message is more than 1000 characters.')

    # AccessError 1: invalid channel_id
    channel = get_channel_by_channel_id(channel_id)
    if type(channel_id) != int or channel is None:
        raise InputError(description='message_send_v2 : Invalid channel_id.')

    # AccessError 2: the authorised user has not joined the channel they are trying to post to
    if auth_user not in channel.all_members:
        raise AccessError(description='message_send_v2 : the authorised user has not joined the channel.')

    # error check
    auth_user, message, channel = helper_message_send_v2(token, channel_id, message)
    # check if time_sent is after current time
    cur_time = current_time()
    if time_sent < cur_time:
        raise InputError(description="Time sent is a time in the past")

    # if all inputs are valid, create a new message id
    new_message_id = create_message_id()

    timer = Timer((time_sent - cur_time), helper2_message_send_v2, [new_message_id, auth_user, message, channel])
    timer.start()

    return {
        'message_id': new_message_id
    }


"""
Auther: Lan Lin

Background: 
Send a message from authorised_user to the dm specified 
by dm_id automatically at a specified time in the future
"""


def message_sendlaterdm_v1(token: str, dm_id: int, message: str, time_sent: int) -> Dict:
    # Type checking
    if type(dm_id) != int or type(message) != str or type(time_sent) != int:
        raise InputError(description="message_sendlaterdm_v1 : incorrect type for your inputs.")

    # InputError 1: invalid token.
    auth_user = get_user_by_token(token)
    if auth_user is None:
        raise AccessError(description='message_send_v2 : Invalid token.')

    # InputError 1: Message is more than 1000 characters
    if len(message) > 1000:
        raise InputError(description='message_send_v2 : Message is more than 1000 characters.')

    # AccessError 1: invalid dm_id
    dm = get_dm_by_dm_id(dm_id)
    if type(dm_id) != int or dm is None:
        raise InputError(description='message_send_v2 : Invalid dm_id.')

    # AccessError 2: the authorised user has not joined the channel they are trying to post to
    if auth_user not in dm.dm_members:
        raise AccessError(description='message_send_v2 : the authorised user has not joined the channel.')

    # error check
    auth_user, message, dm = helper_message_senddm_v1(token, dm_id, message)
    # check if time_sent is after current time
    cur_time = current_time()
    if time_sent < cur_time:
        raise InputError(description="Time sent is a time in the past")

    # if all inputs are valid, create a new message id
    new_message_id = create_message_id()

    timer = Timer((time_sent - cur_time), helper2_message_senddm_v1, [new_message_id, auth_user, message, dm])
    timer.start()

    return {
        'message_id': new_message_id
    }


"""
Auther: Lan Lin

Background: 
Given a message within a channel or DM the authorised user is part of, 
add a "react" to that particular message
"""


def message_react_v1(token: str, message_id: int, react_id: int) -> Dict:
    message, user, channel_dm = return_message_if_valid(token, message_id, react_id, 0)
    message.reacted_users.append(user)

    notification = None
    if channel_dm[1] == 0:
        channel = channel_dm[0]
        notification_message = f"{user.handle_str} reacted to your message in {channel.name}"
        notification = Notification(channel.channel_id, -1, notification_message)
    if channel_dm[1] == 1:
        dm = channel_dm[0]
        notification_message = f"{user.handle_str} reacted to your message in {dm.dm_name}"
        notification = Notification(-1, dm.dm_id, notification_message)

    sender = get_user_by_message_id(message_id)
    sender.notifications.append(notification)
    return {}


"""
Auther: Lan Lin

Background: 
Given a message within a channel or DM the authorised user is part of, 
remove a "react" to that particular message
"""


def message_unreact_v1(token: str, message_id: int, react_id: int) -> Dict:
    message, user, _channel_dm = return_message_if_valid(token, message_id, react_id, 1)
    message.reacted_users.remove(user)
    return {}


"""
Auther: Lan Lin

Background: 
Given a message within a channel or DM, mark it as "pinned" 
to be given special display treatment by the frontend
"""


def message_pin_v1(token: str, message_id: int) -> Dict:
    # Type checking
    if type(message_id) != int:
        raise InputError(description="message_pin_v1 : incorrect type for your inputs.")

    message = return_message_to_pin(token, message_id, 0)
    message.is_pinned = True
    return {}


"""
Auther: Lan Lin

Background: 
Given a message within a channel or DM, remove it's mark as unpinned
"""


def message_unpin_v1(token: str, message_id: int) -> Dict:
    # Type checking
    if type(message_id) != int:
        raise InputError(description="message_pin_v1 : incorrect type for your inputs.")

    message = return_message_to_pin(token, message_id, 1)
    message.is_pinned = False
    return {}
#############################################################################
#                                                                           #
#                              Helper function                              #
#                                                                           #
#############################################################################


# generate a new session id
def create_message_id() -> int:
    new_id = data['message_num']
    data['message_num'] = data['message_num'] + 1
    return new_id


# get the sender's uid by message id
def get_u_id_by_message_id(message_id: int) -> int:
    return get_message_by_message_id(message_id).u_id


def get_user_by_message_id(message_id: int) -> User:
    uid = get_u_id_by_message_id(message_id)
    user = get_user_by_uid(uid)
    return user


# get the class Message by message id
def get_message_by_message_id(message_id: int) -> Union[Message, None]:
    for i in data['class_channels']:
        for j in i.messages:
            if j.message_id == message_id:
                return j
    for i in data['class_dms']:
        for j in i.dm_messages:
            if j.message_id == message_id:
                return j
    return None


# return class channel or dm by message id
def get_channel_dm_by_message_id(message_id: int) -> Union[list, None]:
    for i in data['class_channels']:
        for j in i.messages:
            if j.message_id == message_id:
                return [i, 0]
    for i in data['class_dms']:
        for j in i.dm_messages:
            if j.message_id == message_id:
                return [i, 1]
    return None


# find the class Message by message id
# delete the Message
def delete_message_by_message_id(message_id: int):
    target_msg = get_message_by_message_id(message_id)
    for i in data['class_channels']:
        for j in i.messages:
            if j.message_id == target_msg.message_id:
                i.messages.remove(j)
                return
    for i in data['class_dms']:
        for j in i.dm_messages:
            if j.message_id == target_msg.message_id:
                i.dm_messages.remove(j)
                return
    return None


# tagging user if the message include @handle
def tagging_user(message: str, channel_id: int, dm_id: int, sender: User):
    channel = None
    dm = None
    if channel_id != -1:
        channel = get_channel_by_channel_id(channel_id)

    if dm_id != -1:
        dm = get_dm_by_dm_id(dm_id)

    if dm is None and channel is None:
        return

    if len(message) >= 20:
        first_20_char = message[:20]
    else:
        first_20_char = message[:]

    split_msg = message.split()
    for word in split_msg:
        if re.search('@', word) is not None:
            handle = word[1:]
            # print("handle == ", handle)
            invitee = get_user_by_handle(handle)
            if invitee is None:
                continue

            if channel_id != -1:
                if is_user_in_channel(channel_id, invitee.u_id) is None:
                    continue
                # add notification
                notification_message = f"{sender.handle_str} tagged you in {channel.name}: {first_20_char}"
                notification = Notification(channel.channel_id, -1, notification_message)
                invitee.notifications.append(notification)

            if dm_id != -1:
                if is_user_in_dm(dm_id, invitee.u_id) is None:
                    continue
                # add notification
                notification_message = f"{sender.handle_str} tagged you in {dm.dm_name}: {first_20_char}"
                notification = Notification(-1, dm_id, notification_message)
                invitee.notifications.append(notification)


def return_message_if_valid(token: str, message_id: int, react_id: int, flag: int) -> list:
    if react_id != 1:
        raise InputError(description="react_id is not valid")

    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description='message_send_v2 : Invalid token.')

    message = get_message_by_message_id(message_id)
    if message is None:
        raise InputError(description="message_id is invalid")

    if flag == 0:
        if user in message.reacted_users:
            raise AccessError(description="Message with ID message_id already contains an active React with ID "
                                          "react_id from the authorised user")
    if flag == 1:
        if user not in message.reacted_users:
            raise AccessError(description="Message with ID message_id does not contain an active React with ID "
                                          "react_id from the authorised user")

    channel_dm = get_channel_dm_by_message_id(message_id)
    if channel_dm is None:
        raise InputError(description="The message is not in any channel or dm")
    if channel_dm[1] == 0:
        channel = channel_dm[0]
        if is_user_in_channel(channel.channel_id, user.u_id) is None:
            raise AccessError(description="The authorised user is not a member of the channel that the message "
                                          "is within")
    if channel_dm[1] == 1:
        dm = channel_dm[0]
        if is_user_in_dm(dm.dm_id, user.u_id) is None:
            raise AccessError(description="The authorised user is not a member of the DM that the message is within")

    return [message, user, channel_dm]


def return_message_to_pin(token: str, message_id: int, flag: int) -> Message:
    # InputError 1: invalid token.
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description='Invalid token.')

    # InputError 2: message_id is invalid
    message = get_message_by_message_id(message_id)
    if message is None:
        raise InputError(description="message_id is invalid")

    # InputError 2: Message with ID message_id is already pinned
    if flag == 0:
        if message.is_pinned is True:
            raise InputError(description="The message is already pinned")
    if flag == 1:
        if message.is_pinned is False:
            raise InputError(description="The message is already unppined")

    channel_dm = get_channel_dm_by_message_id(message_id)
    if channel_dm is None:
        raise InputError(description="The message is not in any channel or dm")
    if channel_dm[1] == 0:
        channel = channel_dm[0]
        if is_user_in_channel(channel.channel_id, user.u_id) is None:
            raise AccessError(description="The authorised user is not the member of the channel that the message "
                                          "is within")
        if is_user_owner_channel(channel.channel_id, user.u_id) is None:
            raise AccessError(description="The authorised user is not the owner of the channel that the message "
                                          "is within")
    if channel_dm[1] == 1:
        dm = channel_dm[0]
        if is_user_in_dm(dm.dm_id, user.u_id) is None:
            raise AccessError(description="The authorised user is not the member of the DM that the message is within")
        if is_user_owner_dm(dm.dm_id, user.u_id) is None:
            raise AccessError(description="The authorised user is not the owner of the DM that the message is within")

    return message


# update user's stats about channel joined
def update_message_user_stat(user: User) -> None:
    stat_message_user = {
        'num_messages_sent': len(user.messages),
        'time_stamp': current_time()
    }
    user.messages_sent.append(stat_message_user)


# update Dreams stats about channels
def update_message_dreams_stat() -> None:
    stat_message = {
        'num_messages_exist': len(data['class_messages']),
        'time_stamp': current_time()
    }
    data['messages_exist'].append(stat_message)


def helper_message_send_v2(token: str, channel_id: int, message: str) -> list:
    if type(channel_id) != int or type(message) != str:
        raise InputError(description="incorrect type for your inputs.")

    # InputError 1: invalid token.
    auth_user = get_user_by_token(token)
    if auth_user is None:
        raise AccessError(description='message_send_v2 : Invalid token.')

    # InputError 1: Message is more than 1000 characters
    if len(message) > 1000:
        raise InputError(description='message_send_v2 : Message is more than 1000 characters.')

    # AccessError 1: invalid channel_id
    channel = get_channel_by_channel_id(channel_id)
    if type(channel_id) != int or channel is None:
        raise InputError(description='message_send_v2 : Invalid channel_id.')

    # AccessError 2: the authorised user has not joined the channel they are trying to post to
    if auth_user not in channel.all_members:
        raise AccessError(description='message_send_v2 : the authorised user has not joined the channel.')

    return [auth_user, message, channel]


def helper2_message_send_v2(message_id: int, auth_user: User, message: str, channel: Channel) -> None:
    time_created = current_time()
    message_created = Message(message_id, auth_user.u_id, message, time_created, channel.channel_id, -1)
    channel.messages.append(message_created)
    auth_user.messages.append(message_created)
    data['class_messages'].append(message_created)

    # update Dreams stats about message
    update_message_dreams_stat()
    # update user's stats about message
    update_message_user_stat(auth_user)

    # check and tag user
    tagging_user(message, channel.channel_id, -1, auth_user)


def helper_message_senddm_v1(token: str, dm_id: int, message: str) -> list:
    if type(dm_id) != int or type(message) != str:
        raise InputError(description="incorrect type for your inputs.")

    # InputError 1: invalid token.
    auth_user = get_user_by_token(token)
    if auth_user is None:
        raise AccessError(description='message_send_v2 : Invalid token.')

    # InputError 1: Message is more than 1000 characters
    if len(message) > 1000:
        raise InputError(description='message_send_v2 : Message is more than 1000 characters.')

    # AccessError 1: invalid dm_id
    dm = get_dm_by_dm_id(dm_id)
    if type(dm_id) != int or dm is None:
        raise InputError(description='message_send_v2 : Invalid dm_id.')

    # AccessError 2: the authorised user has not joined the channel they are trying to post to
    if auth_user not in dm.dm_members:
        raise AccessError(description='message_send_v2 : the authorised user has not joined the channel.')

    return [auth_user, message, dm]


def helper2_message_senddm_v1(message_id: int, auth_user: User, message: str, dm: DM) -> None:
    created_time = current_time()
    message_created = Message(message_id, auth_user.u_id, message, created_time, -1, dm.dm_id)
    dm.dm_messages.append(message_created)
    auth_user.messages.append(message_created)
    data['class_messages'].append(message_created)

    # update Dreams stats about message
    update_message_dreams_stat()
    # update user's stats about message
    update_message_user_stat(auth_user)

    # check and tag user
    tagging_user(message, -1, dm.dm_id, auth_user)


# bonus
def return_nudged_user_in_channel_message(message: str, channel_id: int, sender: User) -> str:

    split_msg = message.split()
    nudged_message_list = [message]
    for word in split_msg:
        if re.search('#', word) is not None:
            handle = word[1:]
            receiver = get_user_by_handle(handle)
            if receiver is None:
                continue

            if is_user_in_channel(channel_id, receiver.u_id) is None:
                continue
            nudged_message = f"{sender.name_first} {sender.name_last} nudged {receiver.name_first} {receiver.name_last}"
            nudged_message_list.append(nudged_message)

    if len(nudged_message_list) == 1:
        return message
    else:
        return_message = '\n'.join(nudged_message_list)
        return return_message


# bonus
def return_nudged_user_in_dm_message(message: str, dm_id: int, sender: User) -> str:

    split_msg = message.split()
    nudged_message_list = [message]
    for word in split_msg:
        if re.search('#', word) is not None:
            handle = word[1:]
            receiver = get_user_by_handle(handle)
            if receiver is None:
                continue

            if is_user_in_dm(dm_id, receiver.u_id) is None:
                continue
            nudged_message = f"{sender.name_first} {sender.name_last} nudged {receiver.name_first} {receiver.name_last}"
            nudged_message_list.append(nudged_message)

    if len(nudged_message_list) == 1:
        return message
    else:
        return_message = '\n'.join(nudged_message_list)
        return return_message
