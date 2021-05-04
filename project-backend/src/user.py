from src.data_file import Channel, DM, Message, Permission, data
from src.auth import get_user_by_uid, session_to_token, token_to_session, get_user_by_token, \
    is_email_valid, auth_register_v1
from src.error import InputError, AccessError
from PIL import Image
import requests
import os
import io
from typing import Dict

"""
user.py
Auther: Lan Lin
"""


def user_profile_v1(token: str, u_id: int) -> Dict:
    # find the user to show the profile
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token passed in is invalid")

    user2 = get_user_by_uid(u_id)
    if user2 is None:
        raise InputError(description="User with u_id is not a valid user")

    result = user2.return_type_user_v2()
    return {
        'user': result
    }


def user_profile_setname_v1(token: str, name_first: str, name_last: str) -> Dict:
    # find the user to update the name
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token passed in is invalid")

    # if name_first is not between 1 and 50 characters
    if not (1 <= len(name_first) <= 50):
        raise InputError(description='name_first is not between 1 and 50 characters')

    # is name_last is not between 1 and 50 characters
    if not (1 <= len(name_last) <= 50):
        raise InputError(description='name_last is not between 1 and 50 characters')

    user.name_first = name_first
    user.name_last = name_last
    return {}


def user_profile_setemail_v1(token: str, email: str) -> Dict:
    # find the user to update the email
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token passed in is invalid")

    # if the email address is invalid
    if not is_email_valid(email):
        raise InputError(description='Email address is not valid')

    # if the user has regiestered before
    # which means the email address is already used by another user
    for u in data['class_users']:
        if email == u.email:
            raise InputError(description='Email address is already being used')

    user.email = email
    return {}


def user_profile_sethandle_v1(token: str, handle_str: str) -> Dict:
    # find the user to update the handle
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token passed in is invalid")

    # is handle_str is not between 3 and 20 characters
    if not (3 <= len(handle_str) <= 20):
        raise InputError(description='handle_str is not between 3 and 52 characters')

    # if the handle_str is already used by another user
    for u in data['class_users']:
        if handle_str == u.handle_str:
            raise InputError(description='handle_str is already being used')

    user.handle_str = handle_str
    return {}


def users_all(token: str) -> Dict:
    # Pull the data of user from data_file
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="user does not refer to a vaild user")

    list_return = []
    for i in data['class_users']:
        list_return.append(i.return_type_user_v2())
    return {
        'users': list_return
    }


def admin_user_remove(token: str, u_id: int) -> Dict:
    # find the owner to implement the remove
    owner = get_user_by_token(token)
    if owner is None:
        raise AccessError(description="Token passed in is invalid")
    if owner.permission_id != Permission.global_owner:
        raise AccessError(description="The authorised user is not a Dream owner")

    # find the user to be removed
    user = get_user_by_uid(u_id)
    if user is None:
        raise InputError(description="User with u_id is not a valid user")

    # if the user is the only owner, the user cannot be removed
    num_dream_owners = count_dream_owner()
    if user.permission_id == Permission.global_owner and num_dream_owners == 1:
        raise InputError(description="The user is currently the only owner")

    # the user first name and last name is replaced by 'Remove user'
    # if the user can be removed successfully
    user.name_first = 'Removed'
    user.name_last = 'user'
    # deal with the messages the removed user sent in channels
    for channel in data['class_channels']:
        for msg in channel.messages:
            if msg.u_id == user.u_id:
                msg.message = 'Removed user'

    # deal with the messages the removed user sent in channels
    for dm in data['class_dms']:
        for msg in dm.dm_messages:
            if msg.u_id == user.u_id:
                msg.message = 'Removed user'

    return {}


def admin_userpermission_change(token: str, u_id: int, permission_id: int) -> Dict:
    owner = get_user_by_token(token)
    if owner is None:
        raise AccessError(description="Token passed in is invalid")
    if owner.permission_id != Permission.global_owner:
        raise AccessError(description="The authorised user is not a Dream owner")
    user = get_user_by_uid(u_id)
    if user is None:
        raise InputError(description="User with u_id is not a valid user")
    if not (permission_id == Permission.global_owner or permission_id == Permission.global_member):
        raise InputError(description="permission_id does not refer to a value permission")

    user.permission_id = permission_id
    return {}


def user_stats_v1(token: str) -> Dict:
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token passed in is invalid")

    num1 = len(user.part_of_channel) + len(user.part_of_dm) + len(user.messages)
    num2 = len(data['class_channels']) + len(data['class_dms']) + len(data['class_messages'])
    if num2 == 0:
        involvement_rate = 0
    else:
        involvement_rate = num1 / num2

    user_stats = {
        'channels_joined': user.channels_joined,
        'dms_joined': user.dms_joined,
        'messages_sent': user.messages_sent,
        'involvement_rate': involvement_rate
    }

    return {
        'user_stats': user_stats
    }


def users_stats_v1(token: str) -> Dict:
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token passed in is invalid")

    num1 = num_user_in_channel_dm()
    num2 = count_active_users()
    if num2 == 0:
        utilization_rate = 0
    else:
        utilization_rate = num1 / num2

    dreams_stats = {
        'channels_exist': data['channels_exist'],
        'dms_exist': data['dms_exist'],
        'messages_exist': data['messages_exist'],
        'utilization_rate': utilization_rate
    }

    return {
        'dreams_stats': dreams_stats
    }


def user_profile_uploadphoto_v1(token: str, img_url: str, x_start: int, y_start: int, x_end: int, y_end: int) -> Dict:
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token passed in is invalid")

    # get the image from url
    try:
        response = requests.get(img_url, stream=True)
    except requests.ConnectionError as e:
        raise InputError(description="The input is not url") from e
    if response.status_code != 200:
        raise InputError(description="img_url returns an HTTP status other than 200.")

    # check the format of the image
    # image = Image.open(response.raw)
    image = Image.open(io.BytesIO(response.content))
    if image.format != 'JPEG':
        raise InputError(description="Image uploaded is not a JPG")

    # check whether the input bounds are valid
    width, height = image.size
    if x_start > width or x_end > width or x_start < 0 or x_end < 0 or x_start >= x_end:
        raise InputError(description="x_start or x_end are not within the dimensions of the image")
    if y_start > height or y_end > height or y_start < 0 or y_end < 0 or y_start >= y_end:
        raise InputError(description="y_start or y_end are not within the dimensions of the image")

    # save the original image locally
    path = 'src/static/'
    if not os.path.exists(path):
        os.mkdir(path)
    path = path + str(user.u_id) + '.jpg'
    user.image_path = path
    # urllib.request.urlretrieve(img_url, path)

    # crop the image
    image_cropped = image.crop((x_start, y_start, x_end, y_end))
    # overwrite the original image by the cropped image
    image_cropped.save(path, format='JPEG')

    # generate the image_url
    user.image_url = 'http://127.0.0.1:8080/static/' + str(user.u_id) + '.jpg'
    return {}


#############################################################################
#                                                                           #
#                              Helper function                              #
#                                                                           #
#############################################################################


def count_active_users() -> int:
    count = 0
    for user in data['class_users']:
        if f"{user.name_first} {user.name_last}" != "Removed user":
            count += 1
    return count


def count_dream_owner() -> int:
    count = 0
    for user in data['class_users']:
        if user.permission_id == Permission.global_owner:
            count += 1
    return count


def num_user_in_channel_dm() -> int:
    count = 0
    for user in data['class_users']:
        num_channel_dm = len(user.part_of_channel) + len(user.part_of_dm)
        if num_channel_dm > 0:
            count += 1
    return count
