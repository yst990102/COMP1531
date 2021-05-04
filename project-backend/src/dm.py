from typing import Dict, Union
from src.data_file import data, Permission, DM, User, Notification, current_time
from src.error import InputError, AccessError
from src.auth import get_user_by_uid, session_to_token, token_to_session, get_user_by_token
#############################################################################
#                                                                           #
#                           Interface function                              #
#                                                                           #
#############################################################################

"""
Author: Zheng Luo

dm/create/v1

Background:
[u_id] is the user(s) that this DM is directed to, and will not include the creator. The creator is the owner of the DM. name should be automatically generated based on the user(s) that is in this dm. The name should be an alphabetically-sorted, comma-separated list of user handles, e.g. 'handle1, handle2, handle3'.

Parameters: (token, [u_id])
Return Type: { dm_id, dm_name }
HTTP Method: POST

InputError when any of:
u_id does not refer to a valid user

"""


def dm_create_v1(token: str, u_id_list: list) -> Dict:
    list_dm_handles = []
    list_dm_invitee = []

    # input error if token does not refer to a valid token
    inviter = get_user_by_token(token)
    if inviter is None:
        raise AccessError(description='The token is invalid, or the inviter has not registered')
    list_dm_handles.append(inviter.handle_str)

    if not isinstance(u_id_list, list):
        raise InputError(description='The u_id_list is not a list')

    for uid in u_id_list:
        invitee = get_user_by_uid(uid)
        # input error if u_id does not refer to a valid user
        if invitee is None:
            raise InputError(description='The u_id is invalid, u_id does not refer to a vaild user')

        list_dm_invitee.append(invitee)
        list_dm_handles.append(invitee.handle_str)

    list_dm_handles.sort()
    dm_name = ", ".join(list_dm_handles)
    dm_id = create_dm_id()

    dm = DM(dm_name, dm_id)
    # Update data
    data['class_dms'].append(dm)

    # Update members and owners inside class DM
    # Note: inviter is also part of member.
    # As well as,
    # Update part_of_dm and dm_owns inside class User
    time_join = current_time()
    update_dm_dreams_stat(time_join)

    for invitee in list_dm_invitee:
        dm.dm_members.append(invitee)
        invitee.part_of_dm.append(dm)

        # update invitees' stats about dm
        update_dm_user_stat(invitee, time_join)

        # add notification
        notification_message = f"{inviter.handle_str} added you to {dm.dm_name}"
        notification = Notification(-1, dm.dm_id, notification_message)
        invitee.notifications.append(notification)

    dm.dm_members.append(inviter)
    inviter.part_of_dm.append(dm)

    dm.dm_owners.append(inviter)
    inviter.dm_owns.append(dm)

    # update inviter's stats about dm
    update_dm_user_stat(inviter, time_join)

    return {
        'dm_id': dm_id,
        'dm_name': dm_name,
    }


"""
Author: Zheng Luo

dm/invite/v1

Background:
Inviting a user to an existing dm

Parameters: (token, dm_id, u_id)
Return Type: {}
HTTP Method: POST

InputError when any of: 
          dm_id does not refer to an existing dm.
          u_id does not refer to a valid user. 

AccessError when: 
        the authorised user is already a member of the DM.

"""


def dm_invite_v1(token: str, dm_id: int, u_id: int) -> Dict:
    # Input error when dm_id does not refer to an existing dm.
    dm = get_dm_by_dm_id(dm_id)
    if dm is None:
        raise InputError(description="dm_id does not refer to a valid or exising dm")

    # Input error when u_id does not refer to a valid user.
    invitee = get_user_by_uid(u_id)
    if invitee is None:
        raise InputError(description="u_id does not refer to a valid or exising user")

    # Access error when the authorised user is not already a member of the DM.
    inviter = get_user_by_token(token)
    if inviter is None:
        raise AccessError(description="The authorised user is not already a member of the DM")

    # Expect invitee is not part of member yet
    if invitee in dm.dm_members:
        raise AccessError(description="The invitee is already a member of the DM")
    else:
        dm.dm_members.append(invitee)
        invitee.part_of_dm.append(dm)
        # add notification
        notification_message = f"{inviter.handle_str} added you to {dm.dm_name}"
        notification = Notification(-1, dm.dm_id, notification_message)
        invitee.notifications.append(notification)

    # update inviter's stats about dm
    update_dm_user_stat(invitee, current_time())

    return {}


"""
Author: Zheng Luo

dm/remove/v1

Background:
Remove an existing DM. This can only be done by the original creator of the DM.

Parameters: (token, dm_id)
Return Type: {}
HTTP Method: DELETE

InputError when:   
    dm_id does not refer to a valid DM 

AccessError when:  
    the user is not the original DM creator

"""


def dm_remove_v1(token: str, dm_id: int) -> Dict:
    # Input error when dm_id does not refer to an existing dm.
    dm = get_dm_by_dm_id(dm_id)
    if dm is None:
        raise InputError(description="dm_id does not refer to a valid or exising dm")

    # AccessError when the user is not the original DM creator.
    inviter = get_user_by_token(token)
    if inviter is None:
        raise AccessError(description="The token is not valid")
    elif inviter not in dm.dm_owners:
        raise AccessError(description="The user is not the original DM creator")

    # Remove the current dm for all users in User.part_of_dm and dm_owns
    # Then remove dm in data class
    for member in dm.dm_members:
        member.part_of_dm.remove(dm)

    for owner in dm.dm_owners:
        owner.dm_owns.remove(dm)

    data['class_dms'].remove(dm)
    # update Dream's dm stats
    update_dm_dreams_stat(current_time())

    return {}


"""
Author: Zheng Luo

dm/leave/v1

Background:
Given a DM ID, the user is removed as a member of this DM

Parameters: (token, dm_id)
Return Type: {}
HTTP Method: POST

InputError when any of:
    dm_id is not a valid DM

AccessError when
    Authorised user is not a member of DM with dm_id

"""


def dm_leave_v1(token: str, dm_id: int) -> Dict:
    # Input error when dm_id does not refer to an existing dm.
    dm = get_dm_by_dm_id(dm_id)
    if dm is None:
        raise InputError(description="dm_id does not refer to a valid or exising dm")

    # Access error when the authorised user is not already a member of the DM.
    leaver = get_user_by_token(token)
    if leaver is None:
        raise AccessError(description="The token is invalid")
    elif dm not in leaver.part_of_dm:
        raise AccessError(description="The authorised user is not already a member of the DM")

    # Remove member from dm
    dm.dm_members.remove(leaver)
    leaver.part_of_dm.remove(dm)
    # Considering the owner leaving dm
    if leaver in dm.dm_owners:
        dm.dm_owners.remove(leaver)
        leaver.dm_owns.remove(dm)
        # If the leaving owner is the only one owner and there is still member in the dm
        # Then first availble person in member become owner
        if len(dm.dm_owners) == 0 and len(dm.dm_members) > 0:
            dm_next_owner = dm.dm_members[0]
            dm.dm_owners.append(dm_next_owner)
            dm_next_owner.dm_owns.append(dm)

    # update leaver's stats about dm
    update_dm_user_stat(leaver, current_time())

    return {}


"""
Author: Zheng Luo

dm/details/v1

Background:
Users that are part of this direct message can view basic information about the DM

Parameters: (token, dm_id)
Return Type: { name, members }
HTTP Method: GET

InputError when any of:
    DM ID is not a valid DM

AccessError when
    Authorised user is not a member of this DM with dm_id
"""


def dm_details_v1(token: str, dm_id: int) -> Dict:
    # Input error when dm_id does not refer to an existing dm.
    dm = get_dm_by_dm_id(dm_id)
    if dm is None:
        raise InputError(description="dm_id does not refer to a valid or exising dm")

    # Access error when the authorised user is not already a member of the DM.
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token is invalid")
    elif dm not in user.part_of_dm:
        raise AccessError(description="The authorised user is not already a member of the DM")

    member_list = []
    for member in dm.dm_members:
        member_list.append(member.return_type_user_v2())
    return {
        'name': dm.dm_name,
        'members': member_list,
    }


"""
Author: Zheng Luo

dm/list/v1

Background:
Returns the list of DMs that the user is a member of

Parameters: (token)
Return Type: { dms }
HTTP Method: GET

N/A
"""


def dm_list_v1(token: str) -> Dict:
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token is invalid")
    list_return = []
    for DMs in user.part_of_dm:
        list_return.append(DMs.return_type_dm())
    return {
        'dms': list_return
    }


"""
Author: Zheng Luo

dm/messages/v1

Background:
Given a DM with ID dm_id that the authorised user is part of,
return up to 50 messages between index "start" and "start + 50". Message with index 0 is the most recent message in the dm. This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the dm, returns -1 in "end" to indicate there are no more messages to load after this return.

Parameters: (token, dm_id, start)
Return Type: { messages, start, end }
HTTP Method: GET

InputError when any of:
    DM ID is not a valid DM

    start is greater than the total number of messages in the dm

AccessError when any of:
    Authorised user is not a member of DM with dm_id
"""


def dm_messages_v1(token: str, dm_id: int, start: int) -> Dict:
    # Input error when dm_id does not refer to an existing dm.
    dm = get_dm_by_dm_id(dm_id)
    if dm is None:
        raise InputError(description="dm_id does not refer to a valid or exising dm")

    # Input error when start is greater than the total number of messages in the dm
    if start > len(dm.dm_messages):
        raise InputError(description="start is greater than the total number of messages in the dm")

    # Access error when Authorised user is not a member of DM with dm_id
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token is invalid")
    elif dm not in user.part_of_dm:
        raise AccessError(description="The authorised user is not already a member of the DM")

    return_message = []
    counter_start = len(dm.dm_messages) - start - 1
    if (counter_start + 1) - 50 > 0:
        counter_end = (counter_start + 1) - 50
        end = start + 50
    else:
        counter_end = 0
        end = -1
    while counter_start >= counter_end:
        msg = dm.dm_messages[counter_start].return_type_message_v2()
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


#############################################################################
#                                                                           #
#                              Helper function                              #
#                                                                           #
#############################################################################

def get_dm_by_dm_id(dm_id: int) -> Union[DM, None]:
    if (not isinstance(dm_id, int)) or dm_id >= data['dm_num']:
        return None
    for dm in data['class_dms']:
        if dm.dm_id == dm_id:
            return dm

    return None


# check if the user is an owner of dm
def is_user_owner_dm(dm_id: int, u_id: int) -> Union[User, None]:
    dm = get_dm_by_dm_id(dm_id)
    for owner in dm.dm_owners:
        if owner.u_id == u_id:
            return owner
    return None


def create_dm_id() -> int:
    new_id = data['dm_num']
    data['dm_num'] = data['dm_num'] + 1
    return new_id


# check if the user is a member of dm
def is_user_in_dm(dm_id: int, u_id: int) -> Union[User, None]:
    dm = get_dm_by_dm_id(dm_id)
    for user in dm.dm_members:
        if u_id == user.u_id:
            return user
    return None


# update user's stats about dm joined
def update_dm_user_stat(user: User, time: int) -> None:
    stat_dm_user = {
        'num_dms_joined': len(user.part_of_dm),
        'time_stamp': time
    }
    user.dms_joined.append(stat_dm_user)


# update Dreams stats about dms
def update_dm_dreams_stat(time: int) -> None:
    stat_dm = {
        'num_dms_exist': len(data['class_dms']),
        'time_stamp': time
    }
    data['dms_exist'].append(stat_dm)
