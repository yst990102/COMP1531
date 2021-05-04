from time import sleep
import pytest
import poplib
from email.parser import Parser
from src.other import clear_v1
from src.auth import auth_login_v1, auth_register_v1, auth_logout, auth_passwordreset_request_v1, auth_passwordreset_reset_v1
from src.error import InputError, AccessError
from src.channel import channel_details_v1, channel_invite_v1
from src.channels import channels_create_v1

"""
Author: Lan Lin

Test for auth_register_v1 function implementation

Tests content:
1. The email is invalid
2. The email address is already been used by another user
3. Password length is less than 6 characters
4. The length of name_first is not between 1 and 50
5. The length of name_last is not between 1 and 50
6. Successfully register several users
7. Successfully register large amount users
8. Test if the handle generated is valid
"""
#############################################################################
#                                                                           #
#                       Test for auth_register_v1                           #
#                                                                           #
#############################################################################


# test email does not match the regular expression
def test_auth_register_invalid_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('123.com', '12345ufd', 'Lan', 'Lin')
    with pytest.raises(InputError):
        auth_register_v1('abc@@@.com', '0823hdskhji', 'Langley', 'Lin')


# test email address is already being used by another user
def test_auth_register_duplicate_email():
    clear_v1()
    auth_register_v1('haha1@gmail.com', 'shkdlch', 'Peter', 'White')
    with pytest.raises(InputError):
        auth_register_v1('haha1@gmail.com', '0w9epodu', 'Tom', 'White')


# test for password entered is less than 6 characters long
def test_auth_register_pwd_length():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('haha@gmail.com', '123', 'Tom', 'White')
    with pytest.raises(InputError):
        auth_register_v1('haha2@gmail.com', 'ab#', 'Peter', 'White')


# name_first is not between 1 and 50 characters inclusively in length
def test_auth_register_firstName_length():
    clear_v1()
    name = 'a' * 51
    with pytest.raises(InputError):
        auth_register_v1('haha@gmail.com', '123iwuiused', '', 'White')
    with pytest.raises(InputError):
        auth_register_v1('haha2@gmail.com', 'iwsdrjcio', name, 'White')


# name_last is not between 1 and 50 characters inclusively in length
def test_auth_register_lastName_length():
    clear_v1()
    name = 'a' * 51
    with pytest.raises(InputError):
        auth_register_v1('haha@gmail.com', '123kjsldfiew', 'Peter', '')
    with pytest.raises(InputError):
        auth_register_v1('haha2@gmail.com', 'iwsdcio3', 'Tom', name)


# test several users can successfully register
def test_auth_register_valid_small():
    clear_v1()
    # register two users with valid inputs
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v1('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')

    # test a dictionary is return
    assert isinstance(register1, dict)
    assert isinstance(register2, dict)

    # test the returned auth_user_id is not None
    assert len(register1) != 0
    assert len(register2) != 0

    # test the auth_user_id for different users are different
    auth_user_id1 = register1['auth_user_id']
    auth_user_id2 = register2['auth_user_id']
    token1 = register1['token']
    token2 = register2['token']
    assert auth_user_id1 != auth_user_id2
    assert token1 != token2


# test large number of users can register successfully
def test_auth_register_valid_large():
    clear_v1()
    id_list = []
    for index in range(50):
        person = auth_register_v1('example'+str(index)+'@testexample.com', 'abcuief98dh', 'Tom', 'Green')
        # check the auth_user_id generated is correct
        assert person['auth_user_id'] == index
        id_list.append(person['auth_user_id'])

    # check all auth_user_ids are unique
    # check the number of registered users are correct
    assert len(set(id_list)) == len(id_list) == 50


# test if a valid handle is generated
def test_auth_register_handle_valid():
    clear_v1()
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'zxcvbnmasdfg', 'hjklqwe')
    register2 = auth_register_v1('test@testexample.com', 'wp01^#123', 'zxcvbnmasdfg', 'hjklqwert')
    register3 = auth_register_v1('haha2@gmail.com', '123jcqewp2', 'zxcvbnmasdfg', 'hjklqwert')
    register4 = auth_register_v1('haha3@gmail.com', '123jcqewp2', 'zxcvbnmasdfg', 'hjklqwertiowjec')

    token1 = register1['token']
    user_id2 = register2['auth_user_id']
    user_id3 = register3['auth_user_id']
    user_id4 = register4['auth_user_id']

    channel_id = channels_create_v1(token1, 'Zoom', True)['channel_id']
    channel_invite_v1(token1, channel_id, user_id2)
    channel_invite_v1(token1, channel_id, user_id3)
    channel_invite_v1(token1, channel_id, user_id4)
    channel_members = channel_details_v1(token1, channel_id)['all_members']
    member1 = channel_members[0]
    member2 = channel_members[1]
    member3 = channel_members[2]
    member4 = channel_members[3]

    """
    - test if the handle is already taken, append the concatenated names with 
    the smallest number (starting at 0) that 
    forms a new handle that isn't already taken.
    - test if the concatenation is longer than 20 characters, it is cutoff at 20 characters.
    """

    assert member1['handle_str'] == 'zxcvbnmasdfghjklqwe'
    assert member2['handle_str'] == 'zxcvbnmasdfghjklqwer'
    assert member3['handle_str'] == 'zxcvbnmasdfghjklqwer0'
    assert member4['handle_str'] == 'zxcvbnmasdfghjklqwer1'


"""
Author : Lan Lin

Test for auth_login_v1 function implementation

Tests content:
1. The email is invalid
2. The email address does not belong to any user
3. Password is wrong
4. The users can successfully register
"""
#############################################################################
#                                                                           #
#                       Test for auth_login_v1                              #
#                                                                           #
#############################################################################


# test for email entered is not a valid email
def test_auth_login_invalid_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1('123.@com', '12345ufd')
    with pytest.raises(InputError):
        auth_login_v1('a.,#0@test.com', '0823hdskhji')
    with pytest.raises(InputError):
        auth_login_v1(None, 'password')


# test for email entered does not belong to a user
def test_auth_login_not_registered_email():
    clear_v1()
    # register a user
    auth_register_v1('haha@gmail.com', '123123123', 'Tom', 'Green')
    # login the user with not registered email
    # will give error
    with pytest.raises(InputError):
        auth_login_v1('haha2@gmail.com', '123123123')


# test for password is not correct
def test_auth_login_wrong_password():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'Green')
    with pytest.raises(InputError):
        auth_login_v1('haha@gmail.com', 'jfqowei0-23opj')


# test for users can login successfully
def test_auth_login_valid():
    clear_v1()
    # register two users with valid inputs
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v1('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')

    # login the two registered users
    login1 = auth_login_v1('haha@gmail.com', '123123123')
    login2 = auth_login_v1('test@testexample.com', 'wp01^#$dp1o23')

    # test the auth_user_id returned by login is the same with register
    # test the auth_user_id generated is correct
    assert register1['auth_user_id'] == login1['auth_user_id']
    assert register2['auth_user_id'] == login2['auth_user_id']
    # test that tokens are different
    assert login1['token'] != register1['token']
    assert login2['token'] != register2['token']


# test for the same user with different sessions
def test_auth_login_different_sessions():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')

    login1 = auth_login_v1('haha@gmail.com', '123123123')
    login2 = auth_login_v1('haha@gmail.com', '123123123')
    login3 = auth_login_v1('haha@gmail.com', '123123123')
    auth_user_id1 = login1['auth_user_id']
    auth_user_id2 = login2['auth_user_id']
    auth_user_id3 = login3['auth_user_id']
    token1 = login1['token']
    token2 = login2['token']
    token3 = login3['token']
    assert auth_user_id1 == auth_user_id2 == auth_user_id3
    assert token1 != token2 != token3
#############################################################################
#                                                                           #
#                       Test for auth_logout                                #
#                                                                           #
#############################################################################


def test_auth_logout_invalid_token():
    clear_v1()
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token = register1['token']
    invalid_token = f"{token}123"
    assert auth_logout(invalid_token) == {'is_success': False}
    assert auth_logout(None) == {'is_success': False}


def test_auth_logout_successfully_emall():
    clear_v1()
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = register1['token']
    # user1 = get_user_by_token(token1)
    login2 = auth_login_v1('haha@gmail.com', '123123123')
    # assert len(user1.current_sessions) == 2
    token2 = login2['token']
    assert auth_logout(token1) == {'is_success': True}
    # assert len(user1.current_sessions) == 1
    assert auth_logout(token2) == {'is_success': True}
    # assert len(user1.current_sessions) == 0


def test_auth_logout_successfully_large():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token_list = []
    for _i in range(20):
        login = auth_login_v1(f'haha@gmail.com', '123123123')
        token_list.append(login['token'])
    for token in token_list:
        result = auth_logout(token)
        assert result == {'is_success': True}
#############################################################################
#                                                                           #
#   Test for auth_passwordreset_request_v1 and auth_passwordreset_reset_v1  #
#                                                                           #
#############################################################################


def test_auth_passwordreset_successful1():
    clear_v1()
    id_check = auth_register_v1('styuannj@163.com', '123123123', 'Peter', 'White')['auth_user_id']
    reset_code_1 = auth_passwordreset_request_v1('styuannj@163.com')['reset_code']

    sleep(2)
    msg = get_email_content("styuannj@163.com", "UXRVCTIAEQZVVGAG", "pop.163.com")

    error_wait = 0
    reset_code_2 = parser_reset_code(msg)
    while reset_code_1 != reset_code_2 and error_wait <= 5:
        sleep(1)
        msg = get_email_content("styuannj@163.com", "UXRVCTIAEQZVVGAG", "pop.163.com")
        reset_code_2 = parser_reset_code(msg)
        error_wait += 1
    assert reset_code_1 == reset_code_2

    auth_passwordreset_reset_v1(reset_code_2, 'TheNewPassword')
    assert auth_login_v1('styuannj@163.com', 'TheNewPassword')['auth_user_id'] == id_check

    clear_v1()


def test_auth_passwordreset_successful2():
    clear_v1()
    id_check = auth_register_v1('cblinker17@gmail.com', '123123123', 'Peter', 'White')['auth_user_id']
    reset_code = auth_passwordreset_request_v1('cblinker17@gmail.com')['reset_code']
    auth_passwordreset_reset_v1(reset_code, 'TheNewPassword')
    assert auth_login_v1('cblinker17@gmail.com', 'TheNewPassword')['auth_user_id'] == id_check


def test_auth_passwordrequest_invalid_email():
    clear_v1()
    auth_register_v1('cblinker17@gmail.com', '123123123', 'Peter', 'White')
    with pytest.raises(InputError):
        auth_passwordreset_request_v1('cblinker@gmail.com')

    clear_v1()


def test_auth_passwordreset_reset_invalid_password():
    clear_v1()
    auth_register_v1('cblinker17@gmail.com', '123123123', 'Peter', 'White')
    reset_code = auth_passwordreset_request_v1('cblinker17@gmail.com')['reset_code']
    invalid_password = '123'
    with pytest.raises(InputError):
        auth_passwordreset_reset_v1(reset_code, invalid_password)

    clear_v1()


def test_auth_passwordreset_reset_invalid_reset_code():
    clear_v1()
    auth_register_v1('cblinker17@gmail.com', '123123123', 'Peter', 'White')
    reset_code = auth_passwordreset_request_v1('cblinker17@gmail.com')['reset_code']
    invalid_reset_code = reset_code + '123'
    with pytest.raises(InputError):
        auth_passwordreset_reset_v1(invalid_reset_code, 'TheNewPassword')
    clear_v1()
#############################################################################
#                                                                           #
#                              Helper function                              #
#                                                                           #
#############################################################################


def parser_reset_code(msg):
    content = msg.get_payload()
    reset_code = list(content.split())[-1:][0]
    return reset_code


def get_email_content(email_address, password, pop3_server):
    # start connecting to server
    server = poplib.POP3(pop3_server)

    server.set_debuglevel(1)

    # identification
    server.user(email_address)
    server.pass_(password)
    _rsp, msg_list, _rsp_siz = server.list()

    # get the least recent email
    total_mail_numbers = len(msg_list)
    _rsp, _msglines, _msgsiz = server.retr(total_mail_numbers)
    msg_content = b'\r\n'.join(_msglines).decode('gbk')

    msg = Parser().parsestr(text=msg_content)
    # close the server
    server.close()

    return msg
