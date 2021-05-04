import pytest
from src.other import clear_v1
from src.auth import auth_login_v1, auth_register_v1, auth_logout
from src.error import InputError, AccessError
from src.channel import channel_details_v1, channel_invite_v1, channel_join_v1
from src.channels import channels_create_v1
from src.dm import dm_create_v1
from src.message import message_send_v2, message_senddm_v1, message_remove_v1
from src.user import user_profile_v1, user_profile_setname_v1, user_profile_setemail_v1, user_profile_sethandle_v1, \
    users_all, admin_user_remove, admin_userpermission_change, user_stats_v1, users_stats_v1, user_profile_uploadphoto_v1, admin_user_remove
from src.data_file import Permission

"""
Author: Emir Aditya Zen

This file is for testing user_profile_v1 function implementation

Background
For a valid user, returns information about their user_id, email, first name,
last name, and handle

HTTP Method: GET

Parameters: (token, u_id)
Return Type: { user }

InputError:
- u_id does not refer to a valid user

AccessError:
- The function is called with an invalid token
"""


#############################################################################
#                                                                           #
#                        Test for user_profile_v1                           #
#                                                                           #
#############################################################################


# Case 1 - tests for valid function implementation (no errors expected)
#          expected outcome is function returns user details
# Occurs when user and token is valid
def test_user_profile_v1_success():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]
    u_id1 = token_id_dict1["auth_user_id"]

    # Calls the user_profile_v1 function for testing
    user1 = user_profile_v1(token1, u_id1)['user']

    # Check output if correct
    assert user1['email'] == "haha@gmail.com"
    assert user1['u_id'] == u_id1
    assert user1['name_first'] == "Peter"
    assert user1['name_last'] == "White"
    assert user1['handle_str'] == "peterwhite"


# Case 2 - tests for multiple valid function implementation (no errors expected)
#          expected outcome is function returns multiple users details
# Occurs when user and token is valid
def test_user_profile_v1_successMultiple():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]
    token2 = token_id_dict2["token"]
    u_id1 = token_id_dict1["auth_user_id"]
    u_id2 = token_id_dict2["auth_user_id"]

    # Calls the user_profile_v1 function for testing
    user1 = user_profile_v1(token1, u_id1)['user']
    user2 = user_profile_v1(token2, u_id2)['user']

    # Check output if correct
    assert user1['email'] == "haha@gmail.com"
    assert user1['u_id'] == u_id1
    assert user1['name_first'] == "Peter"
    assert user1['name_last'] == "White"
    assert user1['handle_str'] == "peterwhite"
    assert user2['email'] == "test@testexample.com"
    assert user2['u_id'] == u_id2
    assert user2['name_first'] == "Tom"
    assert user2['name_last'] == "Green"
    assert user2['handle_str'] == "tomgreen"


# Case 3 - tests for input error outcome
#          expected outcome is input error
# Occurs when user id is invalid
def test_user_profile_v1_inputError():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]
    u_id1 = token_id_dict1["auth_user_id"]

    # Made an invalid user id for testing
    invalid_id = u_id1 + 300

    # Test conditions leading to an input error outcome due to invalid user_id
    with pytest.raises(InputError):
        user_profile_v1(token1, invalid_id)


# Case 4 - tests for access error outcome
#          expected outcome is access error
# Occurs when token is invalid
def test_user_profile_v1_accessError():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]
    u_id1 = token_id_dict1["auth_user_id"]

    # Made an invalid token for testing
    invalid_token = token1 + "rkbgesorgbv#$%"

    # Test conditions leading to an access error outcome due to invalid token
    with pytest.raises(AccessError):
        user_profile_v1(invalid_token, u_id1)


def test_user_profile_v1_token_not_match_u_id():
    clear_v1()
    token_0 = auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")['token']
    auth_register_v1("990102@gmail.com", "123123123", "ShiTong", "Yuan")
    auth_login_v1("haha@gmail.com", "123123123")
    u_id_1 = auth_login_v1("990102@gmail.com", "123123123")['auth_user_id']

    user_profile_v1(token_0, u_id_1)


"""
Author: Emir Aditya Zen

This file is for testing user_profile_setname_v1 function implementation

Background
Update the authorised users first and last name

HTTP Method: PUT

Parameters: (token, name_first, name_last)
Return Type: {}

InputError:
- name_first is not between 1-50 characters inclusively in length
- name_last is not between 1-50 characters inclusively in length

AccessError:
- The function is called with an invalid token
"""


#############################################################################
#                                                                           #
#                    Test for user_profile_setname_v1                       #
#                                                                           #
#############################################################################


# Case 1 - tests for valid function implementation (no errors expected)
#          expected outcome is function changes user name and outputs nothing
# Occurs when token, name_first, and name_last is valid
def test_user_profile_setname_v1_success():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]
    u_id1 = token_id_dict1["auth_user_id"]

    # Calls the user_profile_setname_v1 function to change name
    user_profile_setname_v1(token1, "Mark", "Johnson")

    # Calls the user_profile_v1 function for testing
    user1 = user_profile_v1(token1, u_id1)['user']

    # Check output if correct
    assert user1['email'] == "haha@gmail.com"
    assert user1['u_id'] == u_id1
    assert user1['name_first'] == "Mark"
    assert user1['name_last'] == "Johnson"


# Case 2 - tests for input error due to name_first
#          expected outcome is input error
# Occurs when name_first is not between 1 and 50 characters inclusively in length
def test_user_profile_setname_v1_inputError_nameFirst_caseOne():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Test conditions leading to an input error outcome due to invalid first name
    with pytest.raises(InputError):
        user_profile_setname_v1(token1, "", "Johnson")


# Case 3 - tests for input error due to name_first
#          expected outcome is input error
# Occurs when name_first is not between 1 and 50 characters inclusively in length
def test_user_profile_setname_v1_inputError_nameFirst_caseTwo():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Made an invalid first_name for testing
    invalid_first_name = 51 * "a"

    # Test conditions leading to an input error outcome due to invalid first name
    with pytest.raises(InputError):
        user_profile_setname_v1(token1, invalid_first_name, "Johnson")


# Case 4 - tests for input error due to name_last
#          expected outcome is input error
# Occurs when name_last is not between 1 and 50 characters inclusively in length
def test_user_profile_setname_v1_inputError_nameLast_caseOne():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Test conditions leading to an input error outcome due to invalid last name
    with pytest.raises(InputError):
        user_profile_setname_v1(token1, "Mark", "")


# Case 5 - tests for input error due to name_last
#          expected outcome is input error
# Occurs when name_last is not between 1 and 50 characters inclusively in length
def test_user_profile_setname_v1_inputError_nameLast_caseTwo():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Made an invalid last_name for testing
    invalid_last_name = 51 * "a"

    # Test conditions leading to an input error outcome due to invalid last name
    with pytest.raises(InputError):
        user_profile_setname_v1(token1, "Mark", invalid_last_name)


# Case 6 - tests for access error outcome
#          expected outcome is access error
# Occurs when token is invalid
def test_user_profile_setname_v1_accessError():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Made an invalid token for testing
    invalid_token = token1 + "rkbgesorgbv#$%"

    # Test conditions leading to an access error outcome due to invalid token
    with pytest.raises(AccessError):
        user_profile_setname_v1(invalid_token, "Mark", "Johnson")


"""
Author: Emir Aditya Zen

This file is for testing user_profile_setemail_v1 function implementation

Background
Update the authorised users email address

HTTP Method: PUT

Parameters: (token, email)
Return Type: {}

InputError:
- email is invalid
- email is already used by another user

AccessError:
- The function is called with an invalid token
"""


#############################################################################
#                                                                           #
#                   Test for user_profile_setemail_v1                       #
#                                                                           #
#############################################################################


# Case 1 - tests for valid function implementation (no errors expected)
#          expected outcome is function changes user email and outputs nothing
# Occurs when token and email is valid
def test_user_profile_setemail_v1_success():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]
    u_id1 = token_id_dict1["auth_user_id"]

    # Calls the user_profile_setemail_v1 function to change email
    user_profile_setemail_v1(token1, "newhaha@gmail.com")

    # Calls the user_profile_v1 function for testing
    user1 = user_profile_v1(token1, u_id1)['user']

    # Check output if correct
    assert user1['email'] == "newhaha@gmail.com"
    assert user1['u_id'] == u_id1
    assert user1['name_first'] == "Peter"
    assert user1['name_last'] == "White"
    assert user1['handle_str'] == "peterwhite"


# Case 2 - tests for input error due to email
#          expected outcome is input error
# Occurs when email inputted has not been used but invalid
def test_user_profile_setemail_v1_inputError_email_caseOne():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Test conditions leading to an input error outcome due to invalid email
    with pytest.raises(InputError):
        user_profile_setemail_v1(token1, "")


# Case 3 - tests for input error due to email
#          expected outcome is input error
# Occurs when email inputted has not been used but invalid
def test_user_profile_setemail_v1_inputError_email_caseTwo():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Test conditions leading to an input error outcome due to invalid email
    with pytest.raises(InputError):
        user_profile_setemail_v1(token1, "blablaadgmaildotcom")


# Case 4 - tests for input error due to repeated email
#          expected outcome is input error
# Occurs when email is valid but is used by another user
def test_user_profile_setemail_v1_inputError_repeatedEmail():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Test conditions leading to an input error outcome due to repeated email
    with pytest.raises(InputError):
        user_profile_setemail_v1(token1, "test@testexample.com")


# Case 5 - tests for access error outcome
#          expected outcome is access error
# Occurs when token is invalid
def test_user_profile_setemail_v1_accessError():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Made an invalid token for testing
    invalid_token = token1 + "rkbgesorgbv#$%"

    # Test conditions leading to an access error outcome due to invalid token
    with pytest.raises(AccessError):
        user_profile_setemail_v1(invalid_token, "newhaha@gmail.com")


"""
Author: Emir Aditya Zen

This file is for testing user_profile_sethandle_v1 function implementation

Background
Update the authorised users handle

HTTP Method: PUT

Parameters: (token, handle_str)
Return Type: {}

InputError:
- handle_str is not between 3 and 20 characters inclusive
- handle_str is already used by another user

AccessError:
- The function is called with an invalid token
"""


#############################################################################
#                                                                           #
#                   Test for user_profile_sethandle_v1                      #
#                                                                           #
#############################################################################


# Case 1 - tests for valid function implementation (no errors expected)
#          expected outcome is function changes user handle and outputs nothing
# Occurs when token and handle_str is valid
def test_user_profile_sethandle_v1_success():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]
    u_id1 = token_id_dict1["auth_user_id"]

    # Calls the user_profile_sethandle_v1 function to change handle
    user_profile_sethandle_v1(token1, "markjohnson")

    # Calls the user_profile_v1 function for testing
    user1 = user_profile_v1(token1, u_id1)['user']

    # Check output if correct
    assert user1['email'] == "haha@gmail.com"
    assert user1['u_id'] == u_id1
    assert user1['name_first'] == "Peter"
    assert user1['name_last'] == "White"
    assert user1['handle_str'] == "markjohnson"


# Case 2 - tests for input error due to handle
#          expected outcome is input error
# Occurs when handle_str is not between 3 and 20 characters inclusive
def test_user_profile_sethandle_v1_inputError_handle_caseOne():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Test conditions leading to an input error outcome due to invalid handle
    with pytest.raises(InputError):
        user_profile_sethandle_v1(token1, "")


# Case 3 - tests for input error due to handle
#          expected outcome is input error
# Occurs when handle_str is not between 3 and 20 characters inclusive
def test_user_profile_sethandle_v1_inputError_handle_caseTwo():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Made an invalid handle for testing
    invalid_handle = 51 * "a"

    # Test conditions leading to an input error outcome due to invalid handle
    with pytest.raises(InputError):
        user_profile_sethandle_v1(token1, invalid_handle)


# Case 4 - tests for input error due to repeated handle
#          expected outcome is input error
# Occurs when handle_str is valid but is used by another user
def test_user_profile_sethandle_v1_inputError_repeatedHandle():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]

    # Test conditions leading to an input error outcome due to repeated handle
    with pytest.raises(InputError):
        user_profile_sethandle_v1(token1, "tomgreen")


# Case 5 - tests for access error outcome
#          expected outcome is access error
# Occurs when token is invalid
def test_user_profile_sethandle_v1_accessError():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Made an invalid token for testing
    invalid_token = token1 + "rkbgesorgbv#$%"

    # Test conditions leading to an access error outcome due to invalid token
    with pytest.raises(AccessError):
        user_profile_sethandle_v1(invalid_token, "markjohnson")


"""
Author: Emir Aditya Zen

This file is for testing users_all_v1 function implementation

Background
Returns a list of all users and their associated details

HTTP Method: GET

Parameters: (token)
Return Type: { users }

AccessError:
- The function is called with an invalid token
"""


#############################################################################
#                                                                           #
#                          Test for users_all_v1                            #
#                                                                           #
#############################################################################


# Case 1 - tests for valid function implementation (no errors expected) single user case
#          expected outcome is function outputs users as a list of dictionaries
# Occurs when token is valid and only 1 user is currently registered
def test_users_all_v1_success():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]
    u_id1 = token_id_dict1["auth_user_id"]

    # Calls the users_all_v1 function for testing
    output = users_all(token1)['users']

    # Check output if correct
    assert output[0]['email'] == "haha@gmail.com"
    assert output[0]['u_id'] == u_id1
    assert output[0]['name_first'] == "Peter"
    assert output[0]['name_last'] == "White"
    assert output[0]['handle_str'] == "peterwhite"


# Case 2 - tests for valid function implementation (no errors expected) multiple user case
#          expected outcome is function outputs users as a list of dictionaries
# Occurs when token is valid and multiple users is currently registered
def test_users_all_v1_successMultiple():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]
    u_id1 = token_id_dict1["auth_user_id"]
    u_id2 = token_id_dict2["auth_user_id"]

    # Calls the users_all_v1 function for testing
    output = users_all(token1)['users']

    # Check output if correct
    assert output[0]['email'] == "haha@gmail.com"
    assert output[0]['u_id'] == u_id1
    assert output[0]['name_first'] == "Peter"
    assert output[0]['name_last'] == "White"
    assert output[0]['handle_str'] == "peterwhite"
    assert output[1]['email'] == "test@testexample.com"
    assert output[1]['u_id'] == u_id2
    assert output[1]['name_first'] == "Tom"
    assert output[1]['name_last'] == "Green"
    assert output[1]['handle_str'] == "tomgreen"


# Case 5 - tests for access error outcome
#          expected outcome is access error
# Occurs when token is invalid
def test_users_all_v1_accessError():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Made an invalid token for testing
    invalid_token = token1 + "rkbgesorgbv#$%"

    # Test conditions leading to an access error outcome due to invalid token
    with pytest.raises(AccessError):
        users_all(invalid_token)


#############################################################################
#                                                                           #
#                       Test for admin_user_permission_change               #
#                                                                           #
#############################################################################


"""
Author: Lan Lin
Background: Given a User by their user ID, set their permissions 
to new permissions described by permission_id
Input Error: 
1. u_id does not refer to a valid user
2. permission_id does not refer to a value permission
Access Error: The authorised user is not an owner
"""


def test_invalid_token():
    clear_v1()
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token = register1['token']
    invalid_token = f"{token}123"
    register2 = auth_register_v1('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    u_id2 = register2['auth_user_id']
    new_permission_id = Permission.global_owner
    with pytest.raises(AccessError):
        admin_userpermission_change(invalid_token, u_id2, new_permission_id)


def test_admin_change_permission_invalid_owner():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v1('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    register3 = auth_register_v1('haha1@gmail.com', '1231231231', 'Pete', 'Whit')
    token2 = register2['token']
    uid3 = register3['auth_user_id']
    with pytest.raises(AccessError):
        admin_userpermission_change(token2, uid3, Permission.global_owner)


def test_admin_change_permission_invalid_user():
    clear_v1()
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v1('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    token1 = register1['token']
    uid2 = register2['auth_user_id']
    invalid_uid = uid2 + 100
    with pytest.raises(InputError):
        admin_userpermission_change(token1, invalid_uid, Permission.global_owner)


def test_admin_change_permission_invalid_permission():
    clear_v1()
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v1('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    token1 = register1['token']
    uid2 = register2['auth_user_id']
    invalid_permission = 3
    with pytest.raises(InputError):
        admin_userpermission_change(token1, uid2, invalid_permission)


def test_admin_change_permission_owner():
    clear_v1()
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v1('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    token1 = register1['token']
    uid2 = register2['auth_user_id']
    token2 = register2['token']
    admin_userpermission_change(token1, uid2, Permission.global_owner)
    channel_id = channels_create_v1(token1, "My Channel", False)['channel_id']
    channel_join_v1(token2, channel_id)


def test_admin_change_permission_member():
    clear_v1()
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v1('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    token1 = register1['token']
    uid1 = register1['auth_user_id']
    uid2 = register2['auth_user_id']
    token2 = register2['token']
    admin_userpermission_change(token1, uid2, Permission.global_owner)
    admin_userpermission_change(token2, uid1, Permission.global_member)
    channel_id = channels_create_v1(token2, "My Channel", False)['channel_id']
    with pytest.raises(AccessError):
        channel_join_v1(token1, channel_id)


#############################################################################
#                                                                           #
#                       Test for admin_user_remove                          #
#                                                                           #
#############################################################################
"""
Author: Lan Lin
Background: Given a User by their user ID, remove the user from the Dreams.
Input Error: 
1. u_id does not refer to a valid user
2. The user is currently the only owner
Access Error: The authorised user is not an owner
"""


def test_admin_user_remove_invalid_token():
    clear_v1()
    u_id_0 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')['auth_user_id']
    with pytest.raises(AccessError):
        admin_user_remove("invalid token", u_id_0)
    with pytest.raises(AccessError):
        admin_user_remove(None, u_id_0)


def test_admin_user_remove_invalid_uid():
    clear_v1()
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = register1['token']
    with pytest.raises(InputError):
        admin_user_remove(token1, None)
    with pytest.raises(InputError):
        admin_user_remove(token1, 'hehe')


def test_admin_user_remove_only_owner():
    clear_v1()
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = register1['token']
    uid1 = register1['auth_user_id']
    with pytest.raises(InputError):
        admin_user_remove(token1, uid1)


def test_admin_user_remove_invalid_owner():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v1('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    token2 = register2['token']
    uid2 = register2['auth_user_id']
    with pytest.raises(AccessError):
        admin_user_remove(token2, uid2)


def test_admin_user_remove_successfully():
    clear_v1()
    regiester1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v1('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    token1 = regiester1['token']
    token2 = register2['token']
    uid2 = register2['auth_user_id']
    user_profile2 = user_profile_v1(token2, uid2)
    assert user_profile2['user']['email'] == 'test@testexample.com'
    admin_user_remove(token1, uid2)
    user_profile2 = user_profile_v1(token2, uid2)
    name_first = user_profile2['user']['name_first']
    name_last = user_profile2['user']['name_last']
    assert f'{name_first} {name_last}' == 'Removed user'


def test_admin_user_remove_successfully2():
    clear_v1()
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v1('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    token1 = register1['token']
    token2 = register2['token']
    uid2 = register2['auth_user_id']

    channel_id_0 = channels_create_v1(token2, "channel1", True)['channel_id']
    dm_id_0 = dm_create_v1(token2, [uid2])['dm_id']

    message_send_v2(token2, channel_id_0, "channel_msg")
    message_senddm_v1(token2, dm_id_0, "dm_msg")

    user_profile2 = user_profile_v1(token2, uid2)
    assert user_profile2['user']['email'] == 'test@testexample.com'

    admin_user_remove(token1, uid2)
    user_profile2 = user_profile_v1(token2, uid2)
    name_first = user_profile2['user']['name_first']
    name_last = user_profile2['user']['name_last']
    assert f'{name_first} {name_last}' == 'Removed user'
    clear_v1()
#############################################################################
#                                                                           #
#                        Test for user_stats_v1                             #
#                                                                           #
#############################################################################


"""
Auther: Lan Lin
"""


def test_user_stats_v1():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    token_1 = auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")["token"]

    auth_login_v1("test_email0@gmail.com", "password")
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")["auth_user_id"]

    def test_zero_involvement_rate():
        assert user_stats_v1(token_0)['user_stats']['involvement_rate'] == 0

    # ----------------------------testing------------------------------------
    test_zero_involvement_rate()
    # ------------------------------------------------------------------------

    dm_0_id = dm_create_v1(token_0, [u_id_1])["dm_id"]
    channel_0_id = channels_create_v1(token_1, "channel_0", True)["channel_id"]

    message_senddm_v1(token_0, dm_0_id, "I am message.")
    message_send_v2(token_1, channel_0_id, "I am message.")
    message_send_v2(token_1, channel_0_id, "I am message.")

    def test_invalid_token_user_stats():
        with pytest.raises(AccessError):
            user_stats_v1("string token")  # token's type is incorrect
        with pytest.raises(AccessError):
            user_stats_v1(1111111111)  # token's range is incorrect
        with pytest.raises(AccessError):
            user_stats_v1(None)

    def test_valid1():
        user0_stats = user_stats_v1(token_0)['user_stats']
        user1_stats = user_stats_v1(token_1)['user_stats']
        assert len(user0_stats['channels_joined']) == 0
        assert len(user0_stats['dms_joined']) == 1
        assert len(user0_stats['messages_sent']) == 1
        assert user0_stats['involvement_rate'] == 2/5
        assert len(user1_stats['channels_joined']) == 1
        assert len(user1_stats['dms_joined']) == 1
        assert len(user1_stats['messages_sent']) == 2
        assert user1_stats['involvement_rate'] == 4/5
    # ----------------------------testing------------------------------------
    test_invalid_token_user_stats()
    test_valid1()
    # -----------------------------------------------------------------------
    message_senddm_v1(token_0, dm_0_id, "I am message.")
    message_senddm_v1(token_0, dm_0_id, "I am message.")
    message_senddm_v1(token_0, dm_0_id, "I am message.")

    def test_valid2():
        user_stats = user_stats_v1(token_0)['user_stats']
        assert len(user_stats['messages_sent']) == 4
        assert user_stats['involvement_rate'] == 5 / 8
    # ----------------------------testing------------------------------------
    test_valid2()
#############################################################################
#                                                                           #
#                        Test for users_stats_v1                             #
#                                                                           #
#############################################################################


"""
Auther: Lan Lin
"""


def test_users_stats_v1():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    token_1 = auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")["token"]
    uid2 = auth_register_v1("test_email2@gmail.com", "password", "First1", "Last1")['auth_user_id']

    auth_login_v1("test_email0@gmail.com", "password")
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")["auth_user_id"]

    dm_0_id = dm_create_v1(token_0, [u_id_1])["dm_id"]
    channel_0_id = channels_create_v1(token_1, "channel_0", True)["channel_id"]
    channels_create_v1(token_1, "channel_1", True)

    message_senddm_v1(token_0, dm_0_id, "I am message.")
    message_id1 = message_send_v2(token_1, channel_0_id, "I am message.")['message_id']
    message_send_v2(token_1, channel_0_id, "I am message.")

    def test_invalid_token_users_stats():
        with pytest.raises(AccessError):
            user_stats_v1("string token")  # token's type is incorrect
        with pytest.raises(AccessError):
            user_stats_v1(1111111111)  # token's range is incorrect
        with pytest.raises(AccessError):
            user_stats_v1(None)

    def test_valid1():
        dreams_stats = users_stats_v1(token_0)['dreams_stats']
        assert len(dreams_stats['channels_exist']) == 2
        assert len(dreams_stats['dms_exist']) == 1
        assert len(dreams_stats['messages_exist']) == 3
        assert dreams_stats['utilization_rate'] == 2 / 3
    # ----------------------------testing------------------------------------
    test_invalid_token_users_stats()
    test_valid1()
    # -----------------------------------------------------------------------
    message_remove_v1(token_1, message_id1)
    admin_user_remove(token_0, uid2)

    def test_valid2():
        dreams_stats = users_stats_v1(token_0)['dreams_stats']
        assert len(dreams_stats['messages_exist']) == 4
        assert dreams_stats['utilization_rate'] == 1
    # ----------------------------testing------------------------------------
    test_valid2()
#############################################################################
#                                                                           #
#                        Test for user_profile_uploadphoto_v1               #
#                                                                           #
#############################################################################


def test_user_profile_uploadphoto_v1():
    clear_v1()
    url = 'https://static.boredpanda.com/blog/wp-content/uploads/2020/05/700-1.jpg'
    register = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")
    token_0 = register['token']
    uid0 = register['auth_user_id']

    def test_invalid_token1():
        with pytest.raises(AccessError):
            user_profile_uploadphoto_v1("string token", url, 0, 0, 50, 50)  # token's type is incorrect
        with pytest.raises(AccessError):
            user_profile_uploadphoto_v1(1111111111, url, 0, 0, 50, 50)  # token's range is incorrect
        with pytest.raises(AccessError):
            user_profile_uploadphoto_v1(None, url, 0, 0, 50, 50)

    def test_invalid_url():
        with pytest.raises(InputError):
            user_profile_uploadphoto_v1(token_0, "http://haha", 0, 0, 50, 50)

    def test_invalid_image_format():
        invalid_format_url = 'https://pngimg.com/uploads/mario/mario_PNG53.png'
        with pytest.raises(InputError):
            user_profile_uploadphoto_v1(token_0, invalid_format_url, 0, 0, 50, 50)

    def test_invalid_x_bound():
        with pytest.raises(InputError):
            user_profile_uploadphoto_v1(token_0, url, 50, 0, 0, 50)

    def test_invalid_y_bound():
        with pytest.raises(InputError):
            user_profile_uploadphoto_v1(token_0, url, 0, 50, 50, 0)

    def test_valid():
        user_profile_start = user_profile_v1(token_0, uid0)['user']
        img_url1 = user_profile_start['profile_img_url']

        user_profile_uploadphoto_v1(token_0, url, 0, 0, 50, 50)

        user_profile = user_profile_v1(token_0, uid0)['user']
        img_url = user_profile['profile_img_url']

        assert img_url1 != img_url
        assert img_url == 'http://127.0.0.1:8080/static/' + str(uid0) + '.jpg'
    # ----------------------------testing------------------------------------
    test_invalid_token1()
    test_invalid_url()
    test_invalid_image_format()
    test_invalid_x_bound()
    test_invalid_y_bound()
    test_valid()
    clear_v1()
