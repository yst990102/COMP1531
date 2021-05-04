import pytest
import requests
import json
from src import config

"""
http server tests of dm.py
Auther: Zheng Luo
"""


@pytest.fixture
def parameters0():
    parameters0 = {
        "email": "ZhengRogerLuo@gmail.com",
        "password": "TrimesterIsTheBest2021!",
        "name_first": "Aheng",
        "name_last": "Luo"
    }
    return parameters0


@pytest.fixture
def parameters1():
    parameters1 = {
        "email": "z5206267@gmail.com",
        "password": "IHateSemester2019!",
        "name_first": "Roger",
        "name_last": "Luo"
    }
    return parameters1


@pytest.fixture
def parameters2():
    parameters2 = {
        "email": "hahahaah2@gmail.com",
        "password": "IHateSemester2020!",
        "name_first": "James",
        "name_last": "Brown"
    }
    return parameters2


#############################################################################
#                                                                           #
#                     Http Test for dm_create_v1 Error                      #
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


# Invalid input invitee
def test_dm_create_v1_nonexist_invitee_http(parameters0):
    requests.delete(config.url + 'clear/v1')
    # Create(register) two users: user0 and user1.
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    incorrect_input = {
        'token': token0,
        'u_ids': [5]
    }
    status = requests.post(config.url + 'dm/create/v1', json=incorrect_input).status_code
    assert status == 400


#############################################################################
#                                                                           #
#                     Http Test for dm_invite_v1 Error                      #
#                                                                           #
#############################################################################
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


# Invaild input u_id
def test_dm_invite_v1_invaild_uid_http(parameters0, parameters1):
    requests.delete(config.url + 'clear/v1')
    # Create(register) two users: user0 and user1.
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    u_id_1 = json.loads(user1.text).get('auth_user_id')
    input0 = {
        'token': token0,
        'u_ids': [u_id_1]
    }
    dm_info = requests.post(config.url + 'dm/create/v1', json=input0)
    dm_id = json.loads(dm_info.text).get('dm_id')
    incorrect_input = {
        'token': token0,
        'dm_id': dm_id,
        'u_id': '12'
    }
    status = requests.post(config.url + 'dm/invite/v1', json=incorrect_input).status_code
    assert status == 400


# Invaild input dm_id
def test_dm_invite_v1_invaild_dm_id_http(parameters0, parameters1, parameters2):
    requests.delete(config.url + 'clear/v1')
    # Create(register) two users: user0 and user1.
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    user2 = requests.post(config.url + 'auth/register/v2', json=parameters2)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    u_id_1 = json.loads(user1.text).get('auth_user_id')
    u_id_2 = json.loads(user2.text).get('auth_user_id')
    input0 = {
        'token': token0,
        'u_ids': [u_id_1]
    }
    requests.post(config.url + 'dm/create/v1', json=input0)
    incorrect_input = {
        'token': token0,
        'dm_id': 'incorrect_dm_id',
        'u_id': u_id_2
    }
    status = requests.post(config.url + 'dm/invite/v1', json=incorrect_input).status_code
    assert status == 400


# Access error already a user
def test_dm_invite_v1_already_user_http(parameters0, parameters1):
    requests.delete(config.url + 'clear/v1')
    # Create(register) two users: user0 and user1.
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    u_id_1 = json.loads(user1.text).get('auth_user_id')
    input0 = {
        'token': token0,
        'u_ids': [u_id_1]
    }
    dm_info = requests.post(config.url + 'dm/create/v1', json=input0)
    dm_id = json.loads(dm_info.text).get('dm_id')
    incorrect_input = {
        'token': token0,
        'dm_id': dm_id,
        'u_id': u_id_1
    }
    status = requests.post(config.url + 'dm/invite/v1', json=incorrect_input).status_code
    assert status == 403


#############################################################################
#                                                                           #
#                     Http Test for dm_remove_v1 Error                      #
#                                                                           #
#############################################################################
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


# Invaild input dm_id
def test_dm_remove_v1_invaild_dm_id_http(parameters0, parameters1):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    u_id_1 = json.loads(user1.text).get('auth_user_id')
    input0 = {
        'token': token0,
        'u_ids': [u_id_1]
    }
    requests.post(config.url + 'dm/create/v1', json=input0)
    incorrect_input = {
        'token': token0,
        'dm_id': 'incorrect_value'
    }
    status = requests.delete(config.url + 'dm/remove/v1', json=incorrect_input).status_code
    assert status == 400


# Case: Not the original creator to remove the dm.
def test_dm_remove_v1_incorrect_token_http(parameters0, parameters1):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    token1 = json.loads(user1.text).get('token')
    u_id_1 = json.loads(user1.text).get('auth_user_id')
    input0 = {
        'token': token0,
        'u_ids': [u_id_1]
    }
    dm_info = requests.post(config.url + 'dm/create/v1', json=input0)
    dm_id = json.loads(dm_info.text).get('dm_id')
    incorrect_input = {
        'token': token1,
        'dm_id': dm_id
    }
    status = requests.delete(config.url + 'dm/remove/v1', json=incorrect_input).status_code
    assert status == 403


#############################################################################
#                                                                           #
#                     Http Test for dm_leave_v1 Error                      #
#                                                                           #
#############################################################################
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


# Invalid dm_id => inputError => 400
def test_dm_leave_v1_invaild_dm_id_http(parameters0, parameters1):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    u_id_1 = json.loads(user1.text).get('auth_user_id')
    input0 = {
        'token': token0,
        'u_ids': [u_id_1]
    }
    requests.post(config.url + 'dm/create/v1', json=input0)
    incorrect_input = {
        'token': token0,
        'dm_id': "invalid_dm_id"
    }
    status = requests.post(config.url + 'dm/leave/v1', json=incorrect_input).status_code
    assert status == 400


# The test user is not in the dm yet => accessError => 403
# user0 invite user1
# error when user2 want to leave dm_id 0
def test_dm_leave_v1_invaild_dm_id_http1(parameters0, parameters1, parameters2):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    user2 = requests.post(config.url + 'auth/register/v2', json=parameters2)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    u_id_1 = json.loads(user1.text).get('auth_user_id')
    token2 = json.loads(user2.text).get('token')
    input0 = {
        'token': token0,
        'u_ids': [u_id_1]
    }
    dm_info = requests.post(config.url + 'dm/create/v1', json=input0)
    dm_id = json.loads(dm_info.text).get('dm_id')
    incorrect_input = {
        'token': token2,
        'dm_id': dm_id
    }
    status = requests.post(config.url + 'dm/leave/v1', json=incorrect_input).status_code
    assert status == 403


#############################################################################
#                                                                           #
#                     Http Test for dm_detail_v1 Error                      #
#                                                                           #
#############################################################################
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


# dm_id is not a valid dm
def test_dm_details_v1_invaild_dm_id_http(parameters0, parameters1):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    u_id_1 = json.loads(user1.text).get('auth_user_id')
    input0 = {
        'token': token0,
        'u_ids': [u_id_1]
    }
    assert requests.post(config.url + 'dm/create/v1', json=input0).status_code == 200
    status = requests.get(config.url + 'dm/details/v1?token=' + token0 + '&dm_id=invalid_token').status_code
    assert status == 400



# Authorised user is not a member of this DM with dm_id
def test_dm_detail_v1_unauth_user_http(parameters0, parameters1, parameters2):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    user2 = requests.post(config.url + 'auth/register/v2', json=parameters2)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    token2 = json.loads(user2.text).get('token')

    u_id_1 = json.loads(user1.text).get('auth_user_id')
    input0 = {
        'token': token0,
        'u_ids': [u_id_1]
    }
    dm_info = requests.post(config.url + 'dm/create/v1', json=input0)
    dm_id = json.loads(dm_info.text).get('dm_id')
    status = requests.get(config.url + 'dm/details/v1?token=' + token2 + '&dm_id=' + str(dm_id)).status_code
    assert status == 403


#############################################################################
#                                                                           #
#                     Http Test for dm_list_v1 Error                      #
#                                                                           #
#############################################################################
"""
dm_list_v1():

Returns the list of DMs that the user is a member of.

Parameters:(token)
Return Type:{ dms }
HTTP Method: GET

TEST CASES:
N/A
"""

#############################################################################
#                                                                           #
#                     Http Test for dm_message_v1 Error                      #
#                                                                           #
#############################################################################
"""
Author: Zheng Luo

dm/messages/v1

Background:
Given a DM with ID dm_id that the authorised user is part of,
return up to 50 messages between index "start" and "start + 50". Message with index 0 is the most recent message in the channel. This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the channel, returns -1 in "end" to indicate there are no more messages to load after this return.

Parameters: (token, dm_id, start)
Return Type: { messages, start, end }
HTTP Method: GET

InputError when any of:
DM ID is not a valid DM

start is greater than the total number of messages in the channel

AccessError when any of:
Authorised user is not a member of DM with dm_id
"""


# dm_id is not a valid dm
def test_dm_message_v1_invaild_dm_id_http(parameters0):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    status = requests.get(config.url + 'dm/messages/v1?token=' + token0 + '&dm_id=invalid_dm_id&start=0').status_code
    assert status == 400


# oversize start
def test_dm_message_v1_invaild_dm_id_http1(parameters0, parameters1):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    u_id_1 = json.loads(user1.text).get('auth_user_id')
    input0 = {
        'token': token0,
        'u_ids': [u_id_1]
    }
    dm_info = requests.post(config.url + 'dm/create/v1', json=input0)
    dm_id = json.loads(dm_info.text).get('dm_id')
    status = requests.get(
        config.url + 'dm/messages/v1?token=' + token0 + '&dm_id=' + str(dm_id) + '&start=999').status_code
    assert status == 400


# Test user not in
def test_dm_message_v1_test_user_not_in_http(parameters0, parameters1, parameters2):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    user2 = requests.post(config.url + 'auth/register/v2', json=parameters2)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    token2 = json.loads(user2.text).get('token')
    u_id_1 = json.loads(user1.text).get('auth_user_id')
    input0 = {
        'token': token0,
        'u_ids': [u_id_1]
    }
    dm_info = requests.post(config.url + 'dm/create/v1', json=input0)
    dm_id = json.loads(dm_info.text).get('dm_id')
    status = requests.get(
        config.url + 'dm/messages/v1?token=' + token2 + '&dm_id=' + str(dm_id) + '&start=0').status_code
    assert status == 403
#############################################################################
#                                                                           #
#                     Http Test for normal cases                            #
#                                                                           #
#############################################################################


def test_dm_all_normal_cases_http(parameters0, parameters1, parameters2):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    user2 = requests.post(config.url + 'auth/register/v2', json=parameters2)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    token1 = json.loads(user1.text).get('token')
    token2 = json.loads(user2.text).get('token')
    assert token0 == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uSUQiOjB9.luCeqtVJ2ZTm-XXyKAY1xjityV36gZLvOCArCwam1rU"
    assert token1 == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uSUQiOjF9.BrsJT9qSW90mU4VWJMuQ0QEEkz58kwfvQ1PbkrXspOA"
    assert token2 == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uSUQiOjJ9.3Mmom--Q72L0chR2xd74Wm6IUmJyvipXQy5FLqagMCU"

    u_id_0 = json.loads(user0.text).get('auth_user_id')
    u_id_1 = json.loads(user1.text).get('auth_user_id')
    u_id_2 = json.loads(user2.text).get('auth_user_id')
    assert u_id_0 == 0
    assert u_id_1 == 1
    assert u_id_2 == 2
    # Testing Create function
    input0 = {
        'token': token0,
        'u_ids': [u_id_1]
    }
    dm_info = requests.post(config.url + 'dm/create/v1', json=input0)
    dm_id = json.loads(dm_info.text).get('dm_id')
    assert dm_id == 0
    dm_name = json.loads(dm_info.text).get('dm_name')
    assert dm_name == 'ahengluo, rogerluo'

    # Testing list function
    dm_list = requests.get(config.url + 'dm/list/v1?token=' + token0)
    list_of_dm = json.loads(dm_list.text).get('dms')
    assert len(list_of_dm) == 1

    # Testing detail function
    dm_detail = requests.get(config.url + 'dm/details/v1?token=' + token0 + '&dm_id=' + str(dm_id))
    dm_detail_name = json.loads(dm_detail.text).get('name')
    assert dm_detail_name == 'ahengluo, rogerluo'
    dm_detail_members = json.loads(dm_detail.text).get('members')
    assert len(dm_detail_members) == 2

    # Testing invite function
    invite_input = {
        'token': token0,
        'dm_id': dm_id,
        'u_id': u_id_2
    }
    requests.post(config.url + 'dm/invite/v1', json=invite_input)

    dm_detail = requests.get(config.url + 'dm/details/v1?token=' + token0 + '&dm_id=' + str(dm_id))
    dm_detail_members = json.loads(dm_detail.text).get('members')
    assert len(dm_detail_members) == 3

    # Testing leave function
    leave_input = {
        'token': token2,
        'dm_id': dm_id
    }
    requests.post(config.url + 'dm/leave/v1', json=leave_input)
    dm_detail = requests.get(config.url + 'dm/details/v1?token=' + token0 + '&dm_id=' + str(dm_id))
    dm_detail_members = json.loads(dm_detail.text).get('members')
    assert len(dm_detail_members) == 2

    # Testing remove dm
    remove_input = {
        'token': token0,
        'dm_id': 0
    }
    status = requests.delete(config.url + 'dm/remove/v1', json=remove_input).status_code
    assert status == 200
    requests.delete(config.url + 'clear/v1')