from src.data_file import data, DATA, dump_data, Notification, Message
from src.auth import get_user_by_uid, get_user_by_token
from src.error import InputError, AccessError
import re
from typing import Dict
"""
Author: Lan Lin

Background
Resets the internal data of the application to it's initial state
"""


def clear_v1():
    data['class_users'] = []
    data['class_channels'] = []
    data['class_dms'] = []
    data['class_messages'] = []
    data['channels_exist'] = []
    data['dms_exist'] = []
    data['messages_exist'] = []
    data['session_num'] = 0
    data['message_num'] = 0
    data['channel_num'] = 0
    data['dm_num'] = 0
    data['secret'] = 'THIS_IS_SECRET'
    dump_data(DATA)
    return {}


"""
Author: Lan Lin

Background: 
Given a query string, return a collection of messages in all of the channels/DMs 
that the user has joined that match the query

Input Error: query_str is above 1000 characters
Access Error: Token is invalid
"""


def search_v1(token: str, query_str: str) -> Dict:
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token is invalid")

    if len(query_str) > 1000:
        raise InputError(description="query_str is above 1000 characters")

    return_list = []
    for channel in user.part_of_channel:
        for chaneel_message in channel.messages:
            if check_contain_query(query_str, chaneel_message) is True:
                msg = chaneel_message.return_type_message_v2()
                if user.u_id in msg['reacts'][0]['u_ids']:
                    msg['reacts'][0]['is_this_user_reacted'] = True
                else:
                    msg['reacts'][0]['is_this_user_reacted'] = False
                return_list.append(msg)

    for dm in user.part_of_dm:
        for dm_message in dm.dm_messages:
            if check_contain_query(query_str, dm_message) is True:
                msg = dm_message.return_type_message_v2()
                if user.u_id in msg['reacts'][0]['u_ids']:
                    msg['reacts'][0]['is_this_user_reacted'] = True
                else:
                    msg['reacts'][0]['is_this_user_reacted'] = False
                return_list.append(msg)

    return {
        'messages': return_list
    }


"""
Author: Lan Lin
Background: Return the user's most recent 20 notifications
Access Error: Token is invalid
"""


def notification_get_v1(token: str) -> Dict:
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token is invalid")

    noti_list = user.notifications
    return_list = []
    index = len(noti_list) - 1
    if len(noti_list) >= 20:
        for _i in range(20):
            return_list.append(noti_list[index].return_type_notification())
            index -= 1
    else:
        while index >= 0:
            return_list.append(noti_list[index].return_type_notification())
            index -= 1

    return {
        'notifications': return_list
    }
#############################################################################
#                                                                           #
#                              Helper function                              #
#                                                                           #
#############################################################################


# check if the query is contained in the message
# it is case insensitive
def check_contain_query(query: str, _message: Message) -> bool:
    if re.search(query, _message.message, re.IGNORECASE):
        return True
    else:
        return False
