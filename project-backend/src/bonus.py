# Here is bonus functions
from re import S
from src.data_file import current_time, data, Status
from src.other import InputError, AccessError
from src.auth import get_user_by_token, get_user_by_uid
from src.message import get_message_by_message_id
import pickle
from typing import Any, List, Dict, Tuple


def asciimoji_import_package(token: str, package: str, pkg_type: str) -> Any:
    # input checking
    if type(token) != str or type(package) != str or type(pkg_type) != str:
        raise InputError(description="asciimoji_import_package : Parameters' type has error.")

    user = get_user_by_token(token)
    if user is None:
        raise InputError(description="asciimoji_import_package : user not found.")

    if pkg_type == "pak":
        try:
            with open(package + ".pak", "rb") as FILE:
                asciimoji_load = pickle.load(FILE)
        except FileNotFoundError as error:
            raise InputError(description=f"asciimoji_import_package : {package}.pak not found.") from error
    elif pkg_type == "txt":
        try:
            with open(package + ".txt", "r") as FILE:
                asciimoji_load = FILE.read()
        except FileNotFoundError as error:
            raise InputError(description=f"asciimoji_import_package : {package}.txt not found.") from error

    user.asciimoji.update(eval(asciimoji_load))
    FILE.close()


def asciimoji_export_package(token: str, package: str, pkg_type: str) -> Any:
    # input checking
    if type(token) != str or type(package) != str or type(pkg_type) != str:
        raise InputError(description="asciimoji_export_package : Parameters' type has error.")

    user = get_user_by_token(token)
    if user is None:
        raise InputError(description="asciimoji_export_package : user not found.")

    asciimoji_saved = str(user.asciimoji)

    if pkg_type == "pak":
        with open(package + ".pak", "wb") as FILE:
            pickle.dump(asciimoji_saved, FILE)
    elif pkg_type == "txt":
        with open(package + ".txt", "w") as FILE:
            FILE.write(asciimoji_saved)

    FILE.close()


def txt_to_pak(file_name: str) -> None:
    # input checking
    if type(file_name) != str:
        raise InputError(description=f"txt_to_pak : {file_name} need to be string.")

    try:
        with open(file_name + ".txt", "r") as FILE_1:
            content = eval(FILE_1.read())
    except FileNotFoundError as error:
        raise InputError(description=f"txt_to_pak : {file_name}.txt not found.") from error
    with open(file_name + ".pak", "wb") as FILE_2:
        pickle.dump(content, FILE_2)
    FILE_1.close()
    FILE_2.close()


def pak_to_txt(file_name: str) -> None:
    # input checking
    if type(file_name) != str:
        raise InputError(description=f"pak_to_txt : {file_name} need to be string.")

    try:
        with open(file_name + ".pak", "rb") as FILE_1:
            content = eval(pickle.load(FILE_1))
    except FileNotFoundError as error:
        raise InputError(description=f"pak_to_txt : {file_name}.txt not found.") from error
    with open(file_name + ".txt", "w") as FILE_2:
        FILE_2.write(str(content))
    FILE_1.close()
    FILE_2.close()


def message_to_common_words(token: str, message_id: int) -> None:
    # input checking
    if type(token) != str or type(message_id) != int:
        raise InputError(description="message_to_common_words : Parameters' type has error.")

    user = get_user_by_token(token)
    if user is None:
        raise InputError(description="message_to_common_words : user not found.")

    message = get_message_by_message_id(message_id)
    if message is None:
        raise AccessError(description="message_to_common_words : target message not found.")

    user.common_words.append(message.message)


def get_user_status_by_u_id(u_id: int) -> int:
    user = get_user_by_uid(u_id)
    if user is None:
        raise InputError(description="get_user_status_by_u_id : u_id is invalid.")
    else:
        return user.status


def user_status_switch_personlly(u_id: int, status: int) -> Any:
    if type(status) != int:
        raise InputError(description="user_status_switch_personlly : invalid status.")
    user = get_user_by_uid(u_id)
    if user is None:
        raise InputError(description="user_status_switch_personlly : user not found.")
    user.status = status


def status_auto_switch(u_id: int) -> Any:
    user = get_user_by_uid(u_id)
    if user is None:
        raise InputError(description="get_user_by_uid : u_id not found.")

    # login_time = user.login_time
    time_now = current_time()

    # lastest_message = 0
    lastest_message_time = 0
    for message in user.messages:
        if message.time_created > lastest_message_time:
            lastest_message_time = message.time_created
            # lastest_message = message

    if time_now - lastest_message_time >= 15 * 60 and get_user_status_by_u_id(u_id) == Status.online and user.online_time >= 15 * 60:
        # 15min from the most recent message, online more than 15min
        user.status = Status.busy_working
    elif time_now - lastest_message_time >= 45 * 60 and user.online_time >= 60 * 60:
        # 45min from the most recent message, online more than 60min
        user.status = Status.leave_away
