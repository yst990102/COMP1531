# Here is the tests for Bonus functions
from src.data_file import Status
from src.error import InputError
from src.bonus import asciimoji_import_package, asciimoji_export_package, get_user_status_by_u_id, message_to_common_words, pak_to_txt, txt_to_pak, user_status_switch_personlly
from src.message import message_send_v2, message_senddm_v1
from src.other import clear_v1
from src.auth import auth_logout, auth_register_v1, auth_login_v1, get_user_by_token
from src.channels import channels_create_v1
from src.channel import channel_addowner_v1, channel_messages_v1
from src.dm import dm_create_v1, dm_messages_v1
import os
import pickle
import pytest


def test_send_asciimoji_to_channel():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]

    auth_login_v1("test_email0@gmail.com", "password")

    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]

    message_send_v2(token_0, channel_0_id, "<acid> i am acid, lol.")

    channel_msgs = channel_messages_v1(token_0, channel_0_id, 0)
    assert len(channel_msgs['messages']) == 1
    assert channel_msgs['messages'][0]['message'] == "⊂(◉‿◉)つ i am acid, lol."
    clear_v1()


def test_send_asciimoji_to_dm():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")

    auth_login_v1("test_email0@gmail.com", "password")
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")["auth_user_id"]

    dm_0_id = dm_create_v1(token_0, [u_id_1])["dm_id"]

    message_senddm_v1(token_0, dm_0_id, "<acid> i am acid, lol.")

    dm_msgs = dm_messages_v1(token_0, dm_0_id, 0)
    assert len(dm_msgs['messages']) == 1
    assert dm_msgs['messages'][0]['message'] == "⊂(◉‿◉)つ i am acid, lol."
    clear_v1()


def test_asciimoji_import_txt():
    clear_v1()

    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]

    user_0 = get_user_by_token(token_0)
    user_name = user_0.name_first + user_0.name_last

    package_name = user_name
    extra_asciimoji = open(package_name + ".txt", "w")
    extra_asciimoji.write(str({"<creep>": "ԅ(≖‿≖ԅ)", "crim3s": "( ✜︵✜ )", "cute": "(｡◕‿‿◕｡)"}))
    extra_asciimoji.close()

    asciimoji_import_package(token_0, package_name, "txt")

    assert user_0.asciimoji == {"<acid>": "⊂(◉‿◉)つ", "<afraid>": "(ㆆ _ ㆆ)", "<angry>": "•`_´•", "<catlenny>": "( ͡° ᴥ ͡°)", "<creep>": "ԅ(≖‿≖ԅ)", "crim3s": "( ✜︵✜ )", "cute": "(｡◕‿‿◕｡)"}
    os.system(f"rm -rf {package_name}.txt")
    clear_v1()


def test_asciimoji_export_txt():
    clear_v1()
    token_1 = auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")["token"]

    user_1 = get_user_by_token(token_1)
    package_name = user_1.name_first + user_1.name_last

    asciimoji_export_package(token_1, package_name, "txt")

    check_export = open(package_name + ".txt", "r")

    assert check_export.read() == str({"<acid>": "⊂(◉‿◉)つ", "<afraid>": "(ㆆ _ ㆆ)", "<angry>": "•`_´•", "<catlenny>": "( ͡° ᴥ ͡°)"})
    os.system(f"rm -rf {package_name}.txt")
    clear_v1()


def test_asciimoji_import_pak():
    clear_v1()
    token_1 = auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")["token"]
    user_1 = get_user_by_token(token_1)

    asciimoji_saved = str({"<creep>": "ԅ(≖‿≖ԅ)", "crim3s": "( ✜︵✜ )", "cute": "(｡◕‿‿◕｡)"})
    package = "asciimoji"
    with open(package + ".pak", "wb") as FILE:
        pickle.dump(asciimoji_saved, FILE)
    FILE.close()

    asciimoji_import_package(token_1, package, "pak")

    assert user_1.asciimoji == {"<acid>": "⊂(◉‿◉)つ", "<afraid>": "(ㆆ _ ㆆ)", "<angry>": "•`_´•", "<catlenny>": "( ͡° ᴥ ͡°)", "<creep>": "ԅ(≖‿≖ԅ)", "crim3s": "( ✜︵✜ )", "cute": "(｡◕‿‿◕｡)"}
    os.system(f"rm -rf {package}.pak")
    clear_v1()


def test_asciimoji_export_pak():
    clear_v1()
    token_1 = auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")["token"]

    package = "asciimoji"
    asciimoji_export_package(token_1, package, "pak")

    with open(package + ".pak", "rb") as FILE:
        asciimoji_load = pickle.load(FILE)
    assert eval(asciimoji_load) == {"<acid>": "⊂(◉‿◉)つ", "<afraid>": "(ㆆ _ ㆆ)", "<angry>": "•`_´•", "<catlenny>": "( ͡° ᴥ ͡°)"}

    os.system(f"rm -rf {package}.pak")
    clear_v1()


def test_message_to_common_words():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    user_0 = get_user_by_token(token_0)

    channel_0_id = channels_create_v1(token_0, "channel_0", True)['channel_id']
    channel_msgs = channel_messages_v1(token_0, channel_0_id, 0)["messages"]
    assert len(channel_msgs) == 0

    message_id = message_send_v2(token_0, channel_0_id, "message to channel.")["message_id"]
    channel_msgs = channel_messages_v1(token_0, channel_0_id, 0)["messages"]
    assert len(channel_msgs) == 1

    message_to_common_words(token_0, message_id)
    assert user_0.common_words == ["I will be back soon.", "On my way, baby.", "How is it recently?", "message to channel."]

    clear_v1()


def test_txt_to_pak():
    clear_v1()

    def normal_test():
        with open("123.txt", 'w') as FILE:
            FILE.write("123456")
        FILE.close()

        txt_to_pak("123")

        with open("123.pak", 'rb') as FILE:
            content2 = pickle.load(FILE)

        assert str(content2) == "123456"
        os.system("rm -rf 123.txt 123.pak")

    def no_file_test():
        with pytest.raises(InputError):
            txt_to_pak("no_such_file")

    def invalid_file_name():
        with pytest.raises(InputError):
            pak_to_txt(123)
        with pytest.raises(InputError):
            pak_to_txt(None)

    # ------------------testing---------------------
    normal_test()
    no_file_test()
    invalid_file_name()
    clear_v1()


def test_pak_to_txt():
    clear_v1()

    def normal_test():
        with open("123.pak", "wb") as FILE:
            content = "123"
            pickle.dump(content, FILE)
        FILE.close()

        pak_to_txt("123")
        with open("123.txt", 'r') as FILE:
            content1 = FILE.read()

        assert content1 == "123"
        os.system("rm -rf 123.txt 123.pak")

    def no_file_test():
        with pytest.raises(InputError):
            pak_to_txt("no_such_file")

    def invalid_file_name():
        with pytest.raises(InputError):
            pak_to_txt(123)
        with pytest.raises(InputError):
            pak_to_txt(None)
    # ------------------testing---------------------
    normal_test()
    no_file_test()
    invalid_file_name()
    clear_v1()


def test_get_user_status_by_token():
    clear_v1()

    def test_normal_case():
        register = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")
        token_0 = register['token']
        u_id_0 = register['auth_user_id']

        user_status = get_user_status_by_u_id(u_id_0)
        assert user_status == Status.online

        login = auth_login_v1("test_email0@gmail.com", "password")
        token_1 = login['token']
        u_id_1 = login['auth_user_id']

        user_status = get_user_status_by_u_id(u_id_1)
        assert user_status == Status.online

        auth_logout(token_0)
        user_status = get_user_status_by_u_id(u_id_0)
        assert user_status == Status.online

        auth_logout(token_1)
        user_status = get_user_status_by_u_id(u_id_0)
        assert user_status == Status.offline

    def invalid_u_id():
        with pytest.raises(InputError):
            get_user_status_by_u_id("string token")
        with pytest.raises(InputError):
            get_user_status_by_u_id(123456)
        with pytest.raises(InputError):
            get_user_status_by_u_id(None)
    # -------------------testing------------------------
    test_normal_case()
    invalid_u_id()
    clear_v1()


def test_user_status_switch_personlly():
    clear_v1()
    auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")
    u_id_0 = auth_login_v1("test_email0@gmail.com", "password")['auth_user_id']

    def test_normal_case():
        user_status = get_user_status_by_u_id(u_id_0)
        assert user_status == Status.online

        user_status_switch_personlly(u_id_0, Status.leave_away)

        user_status = get_user_status_by_u_id(u_id_0)
        assert user_status == Status.leave_away

    def invalid_u_id():
        with pytest.raises(InputError):
            user_status_switch_personlly("u_id_0", Status.leave_away)

    def invalid_status():
        with pytest.raises(InputError):
            user_status_switch_personlly(u_id_0, None)
    # -------------------testing------------------------
    test_normal_case()
    invalid_u_id()
    invalid_status()
    clear_v1()
