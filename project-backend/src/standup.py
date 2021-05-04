from threading import Timer
from src.data_file import Channel, data, Message, Permission, current_time
from src.error import InputError, AccessError
from src.auth import get_user_by_token, get_user_by_handle, get_user_by_uid
from src.channel import get_channel_by_channel_id, is_user_owner_channel, is_user_in_channel
from src.message import message_send_v2
from typing import Dict

"""
Auther: Lan Lin
"""
#############################################################################
#                                                                           #
#                           Interface function                              #
#                                                                           #
#############################################################################


def standup_start_v1(token: str, channel_id: int, length: int) -> Dict:
    if isinstance(length, int) is False or length < 0 or length is None:
        raise InputError(description='length is invalid')

    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description='Invalid token.')

    channel = get_channel_by_channel_id(channel_id)
    if type(channel_id) != int or channel is None:
        raise InputError(description='Invalid channel_id.')

    if user not in channel.all_members:
        raise AccessError(description='message_send_v2 : the authorised user has not joined the channel.')

    if channel.is_standup_active() is True:
        raise InputError(description='An active standup is currently running in this channel')

    cur_time = current_time()
    finish_time = cur_time + length
    channel.activate_standup()
    channel.set_time_finish(finish_time)

    timer = Timer(length, standup_send_packaged_message, [token, channel])
    timer.start()

    return {
        'time_finish': finish_time
    }


def standup_active_v1(token: str, channel_id: int) -> Dict:
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description='Invalid token.')

    if type(channel_id) != int:
        raise InputError(description='Invalid channel_id.')
    channel = get_channel_by_channel_id(channel_id)
    if channel is None:
        raise InputError(description='Invalid channel_id.')

    return channel.standup


def standup_send_v1(token: str, channel_id: int, message: str) -> Dict:
    if type(channel_id) != int or type(message) != str:
        raise InputError(description="incorrect type for your inputs.")

    if len(message) > 1000:
        raise InputError(description='Message is more than 1000 characters.')

    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description='Invalid token.')

    channel = get_channel_by_channel_id(channel_id)
    if channel is None:
        raise InputError(description='Invalid channel_id.')

    if user not in channel.all_members:
        raise AccessError(description='message_send_v2 : the authorised user has not joined the channel.')

    if channel.is_standup_active() is False:
        raise InputError(description='An active standup is not currently running in this channel')

    p_message = f"{user.handle_str}: {message}"
    channel.packaged_messages.append(p_message)

    return {}
#############################################################################
#                                                                           #
#                              Helper function                              #
#                                                                           #
#############################################################################


def standup_send_packaged_message(token: str, channel: Channel) -> None:
    if len(channel.packaged_messages) > 0:
        packaged_message = "\n".join(channel.packaged_messages)
        message_send_v2(token, channel.channel_id, packaged_message)

    channel.deactivate_standup()
    channel.clear_packaged_messages()
    channel.clear_time_finish()
