import pytest
from src.error import InputError, AccessError
from src.dm import dm_create_v1, dm_details_v1, dm_invite_v1, dm_leave_v1, dm_list_v1, dm_messages_v1, dm_remove_v1
from src.auth import auth_register_v1, auth_login_v1
from src.other import clear_v1
from src.message import message_senddm_v1

#############################################################################
#                                                                           #
#                        Test for dm_details_v1                             #
#                                                                           #
#############################################################################
"""
dm_details_v1():

Users that are part of this direct message can view basic information about the DM.

Parameters:(token, dm_id)
Return Type:{ name, members }

TEST CASES:
	InputError when any of:
        DM ID is not a valid DM
    AccessError when
        Authorised user is not a member of this DM with dm_id

"""


def test_dm_details_v1():
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    token1 = auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")['token']
    token2 = auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")['token']

    auth_login_v1("haha@gmail.com", "123123123")
    auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    auth_login_v1("user1@test.com", "user1password")

    # user1 create the dm, invite user0 into dm
    dm_create_v1(token1, [0])

    def test_invalid_token():
        # token type error
        with pytest.raises(AccessError):
            dm_details_v1("invalid token", 0)
        with pytest.raises(AccessError):
            dm_details_v1(None, 0)

    def test_invalid_dm():
        # dm_id type invalid
        with pytest.raises(InputError):
            dm_details_v1(token1, "invalid_dm_id")

        # dm_id is out of range
        with pytest.raises(InputError):
            dm_details_v1(token1, 999)

    def test_Inaccessible_member():
        # test: user2 should not be in dm, cause this is dm between user1 and user0
        with pytest.raises(AccessError):
            dm_details_v1(token2, 0)

    def test_invalid_user():
        with pytest.raises(AccessError):
            dm_details_v1("invalid user", 0)

    def test_normal_case():
        dm_details_v1(token1, 0)

    # --------------------------testing---------------------------
    test_invalid_token()
    test_invalid_dm()
    test_Inaccessible_member()
    test_invalid_user()
    test_normal_case()
    pass


#############################################################################
#                                                                           #
#                         Test for dm_list_v1                               #
#                                                                           #
#############################################################################
"""
dm_list_v1():

Returns the list of DMs that the user is a member of.

Parameters:(token)
Return Type:{ dms }

TEST CASES:
	N/A

"""


def test_dm_list_v1():
    clear_v1()
    token0 = auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")['token']
    token1 = auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")['token']
    auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")

    auth_login_v1("haha@gmail.com", "123123123")
    auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    auth_login_v1("user1@test.com", "user1password")

    dm_create_v1(token0, [1])
    dm_create_v1(token0, [2])
    dm_create_v1(token1, [2])

    def test_invalid_token():
        with pytest.raises(AccessError):
            dm_list_v1("invalid token")
        with pytest.raises(AccessError):
            dm_list_v1(None)

    def test_normal_case():
        dm_create_v1(token0, [1])
        dm_create_v1(token0, [2])
        dm_create_v1(token1, [2])

        user0_involved = dm_list_v1(token0)

        assert user0_involved['dms'][0]['name'] == "peterwhite, tomgreen"
        assert user0_involved['dms'][0]['dm_id'] == 0

        assert user0_involved['dms'][1]['name'] == "peterwhite, rogerluo"
        assert user0_involved['dms'][1]['dm_id'] == 1

    # --------------------------testing---------------------------
    test_invalid_token()
    test_normal_case()

    pass


#############################################################################
#                                                                           #
#                        Test for dm_create_v1                              #
#                                                                           #
#############################################################################
"""
dm_create_v1():

[u_id] is the user(s) that this DM is directed to, and will not include the creator. The creator is the owner of the DM. name should be automatically generated based on the user(s) that is in this dm. The name should be an alphabetically-sorted, comma-separated list of user handles, e.g. 'handle1, handle2, handle3'.

Parameters:(token, [u_id])
Return Type:{ dm_id, dm_name }

TEST CASES:
	InputError when any of:
        u_id does not refer to a valid user

"""


def test_dm_create_v1():
    clear_v1()
    token0 = auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")['token']
    token1 = auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")['token']
    auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")

    auth_login_v1("haha@gmail.com", "123123123")
    auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    auth_login_v1("user1@test.com", "user1password")

    def test_invalid_token():
        with pytest.raises(AccessError):
            dm_create_v1("invalid token", [1])
        with pytest.raises(AccessError):
            dm_create_v1(None, [1])

    def test_invalid_u_id_list():
        with pytest.raises(InputError):
            dm_create_v1(token1, "i am not a list.")
        with pytest.raises(InputError):
            dm_create_v1(token1, [4, 5, 6])

    def test_none_inviter():
        with pytest.raises(AccessError):
            dm_create_v1(None, [1])

    def test_normal_case():
        dm1 = dm_create_v1(token0, [1])
        assert dm1['dm_id'] == 0
        assert dm1['dm_name'] == "peterwhite, tomgreen"

    # --------------------------testing---------------------------
    test_invalid_token()
    test_normal_case()
    test_invalid_u_id_list()
    test_none_inviter()
    pass


#############################################################################
#                                                                           #
#                        Test for dm_remove_v1                              #
#                                                                           #
#############################################################################
"""
dm_remove_v1():

Remove an existing DM. This can only be done by the original creator of the DM.

Parameters:(token, dm_id)
Return Type:{}

TEST CASES:
	InputError when:
        dm_id does not refer to a valid DM 
    AccessError when:
        the user is not the original DM creator

"""


def test_dm_remove_v1():
    clear_v1()
    token0 = auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")['token']
    token1 = auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")['token']
    auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")

    auth_login_v1("haha@gmail.com", "123123123")
    auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    auth_login_v1("user1@test.com", "user1password")

    dm_create_v1(token0, [1])
    dm_create_v1(token0, [2])
    dm_create_v1(token1, [2])

    def test_invalid_token():
        with pytest.raises(AccessError):
            dm_remove_v1("invalid token", 0)
        with pytest.raises(AccessError):
            dm_remove_v1(None, 0)

    def test_invalid_dm_id():
        # dm_id type invalid
        with pytest.raises(InputError):
            dm_remove_v1(token0, "invalid_dm_id")

        # dm_id is out of range
        with pytest.raises(InputError):
            dm_remove_v1(token0, 999)

    def test_remove_dm_twice():
        dm_remove_v1(token0, 1)
        with pytest.raises(InputError):
            dm_remove_v1(token0, 1)

    def test_not_creator():
        with pytest.raises(AccessError):
            dm_remove_v1("invalid token", 2)
        with pytest.raises(AccessError):
            dm_remove_v1(token0, 2)

    def test_normal_case():
        dm_remove_v1(token0, 0)

    # --------------------------testing---------------------------
    test_invalid_token()
    test_invalid_dm_id()
    test_remove_dm_twice()
    test_not_creator()
    test_normal_case()
    pass


#############################################################################
#                                                                           #
#                        Test for dm_invite_v1                              #
#                                                                           #
#############################################################################
"""
dm_invite_v1():

Inviting a user to an existing dm.

Parameters:(token, dm_id, u_id)
Return Type:{}

TEST CASES:
	InputError when any of:
        dm_id does not refer to an existing dm.
        u_id does not refer to a valid user.
    AccessError when:
        the authorised user is not already a member of the DM
"""


def test_dm_invite_v1():
    clear_v1()
    token0 = auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")['token']
    token1 = auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")['token']
    token2 = auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")['token']

    auth_login_v1("haha@gmail.com", "123123123")
    auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    auth_id2 = auth_login_v1("user1@test.com", "user1password")["auth_user_id"]

    dm_create_v1(token0, [1])
    dm_create_v1(token0, [2])
    dm_create_v1(token1, [2])

    def test_invalid_token():
        with pytest.raises(AccessError):
            dm_invite_v1("invalid token", 0, 2)
        with pytest.raises(AccessError):
            dm_invite_v1(None, 0, 2)

    def test_invalid_dm_id():
        # dm_id type invalid
        with pytest.raises(InputError):
            dm_invite_v1(token0, "invalid_dm_id", 2)

        # dm_id is out of range
        with pytest.raises(InputError):
            dm_invite_v1(token0, 999, 2)

    def test_pre_exist_dm():
        # dm_id is int, but it used to exit
        dm_remove_v1(token0, 1)
        with pytest.raises(InputError):
            dm_invite_v1(token0, 1, 2)

    def test_invalid_u_id():
        with pytest.raises(InputError):
            dm_invite_v1(token0, 0, "invalid_u_id")

    def test_already_user():
        with pytest.raises(AccessError):
            dm_invite_v1(token0, 0, 1)

    def test_inviter_not_authorised():
        with pytest.raises(AccessError):
            dm_invite_v1("invalid token", 0, 0)
        with pytest.raises(AccessError):
            dm_invite_v1(token2, 0, 0)

    def test_normal_case():
        dm_invite_v1(token0, 0, auth_id2)

    # --------------------------testing---------------------------
    test_invalid_token()
    test_invalid_dm_id()
    test_pre_exist_dm()
    test_invalid_u_id()
    test_already_user()
    test_inviter_not_authorised()
    test_normal_case()
    pass


#############################################################################
#                                                                           #
#                         Test for dm_leave_v1                              #
#                                                                           #
#############################################################################
"""
dm_leave_v1():

Given a DM ID, the user is removed as a member of this DM.

Parameters:(token, dm_id)
Return Type:{}

TEST CASES:
	InputError when any of:
        dm_id is not a valid DM
    AccessError when
        Authorised user is not a member of DM with dm_id

"""


def test_dm_leave_v1():
    clear_v1()
    token0 = auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")['token']
    token1 = auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")['token']
    auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")

    auth_login_v1("haha@gmail.com", "123123123")
    auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    auth_login_v1("user1@test.com", "user1password")

    dm_create_v1(token0, [1])
    dm_create_v1(token0, [2])
    dm_create_v1(token1, [2])

    def test_invalid_token():
        with pytest.raises(AccessError):
            dm_leave_v1("invalid token", 0)
        with pytest.raises(AccessError):
            dm_leave_v1(None, 0)

    def test_invalid_dm_id():
        # dm_id type invalid
        with pytest.raises(InputError):
            dm_leave_v1(token0, "invalid_dm_id")

        # dm_id is out of range
        with pytest.raises(InputError):
            dm_leave_v1(token0, 999)

    def test_leave_nonexist_dm():
        dm_remove_v1(token0, 1)
        with pytest.raises(InputError):
            dm_leave_v1(token0, 1)

    def test_user_not_in():
        with pytest.raises(AccessError):
            dm_leave_v1(token0, 2)

    def test_invalid_leaver():
        with pytest.raises(AccessError):
            dm_leave_v1(None, 2)

    def test_normal_case():
        dm_leave_v1(token0, 0)

    # --------------------------testing---------------------------
    test_invalid_token()
    test_invalid_dm_id()
    test_leave_nonexist_dm()
    test_user_not_in()
    test_invalid_leaver()
    test_normal_case()
    pass


#############################################################################
#                                                                           #
#                       Test for dm_messages_v1                             #
#                                                                           #
#############################################################################
"""
dm_messages_v1():

Given a DM with ID dm_id that the authorised user is part of, return up to 50 messages between index "start" and "start + 50". Message with index 0 is the most recent message in the channel. This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the channel, returns -1 in "end" to indicate there are no more messages to load after this return.

Parameters:(token, dm_id, start)
Return Type:{ messages, start, end }

TEST CASES:
	InputError when any of:
        DM ID is not a valid DM
        start is greater than the total number of messages in the channel
    AccessError when any of:
        Authorised user is not a member of DM with dm_id

"""


def test_dm_messages_v1():
    clear_v1()
    token0 = auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")['token']
    token1 = auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")['token']
    auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")

    auth_login_v1("haha@gmail.com", "123123123")
    auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    auth_login_v1("user1@test.com", "user1password")

    dm_create_v1(token0, [1])
    dm_create_v1(token0, [2])
    dm_create_v1(token1, [2])

    def test_invalid_token():
        with pytest.raises(AccessError):
            dm_messages_v1("invalid token", 1, 0)

    def test_invalid_dm_id():
        # dm_id type invalid
        with pytest.raises(InputError):
            dm_messages_v1(token0, "invalid_dm_id", 0)

        # dm_id is out of range
        with pytest.raises(InputError):
            dm_messages_v1(token0, 999, 0)

    def test_oversized_start():
        with pytest.raises(InputError):
            dm_messages_v1(token0, 1, 999)

    def test_user_not_in():
        with pytest.raises(AccessError):
            dm_messages_v1(token1, 1, 0)

    def test_normal_case_less_50_msg():
        dm_messages_v1(token0, 0, 0)

    def test_normal_case_more_50_msg():
        for _i in range(0, 300):
            message_senddm_v1(token0, 0, "This is a message.")
        dm_messages_v1(token0, 0, 60)

    # --------------------------testing---------------------------
    test_invalid_token()
    test_invalid_dm_id()
    test_oversized_start()
    test_user_not_in()
    test_normal_case_less_50_msg()
    test_normal_case_more_50_msg()
    pass
    clear_v1()