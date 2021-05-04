import sys
from json import dumps
from flask import Flask, request, send_from_directory, send_file
from flask_cors import CORS
from src import config
from src.data_file import data, dump_data
from src.auth import auth_register_v1, auth_login_v1, auth_logout, auth_passwordreset_request_v1, \
    auth_passwordreset_reset_v1
from src.user import user_profile_v1, user_profile_setname_v1, user_profile_setemail_v1, user_profile_sethandle_v1, \
    users_all, admin_user_remove, admin_userpermission_change, user_profile_uploadphoto_v1, user_stats_v1, \
    users_stats_v1
from src.other import clear_v1, search_v1, notification_get_v1
from src.channel import channel_invite_v1, channel_details_v1, channel_messages_v1, channel_join_v1, channel_leave_v1, \
    channel_addowner_v1, channel_removeowner_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.message import message_send_v2, message_senddm_v1, message_edit_v2, message_remove_v1, message_share_v1, \
    message_sendlater_v1, message_sendlaterdm_v1, message_react_v1, message_unreact_v1, message_pin_v1, message_unpin_v1
from src.dm import dm_create_v1, dm_invite_v1, dm_remove_v1, dm_leave_v1, dm_details_v1, dm_list_v1, dm_messages_v1
from src.standup import standup_start_v1, standup_active_v1, standup_send_v1
from src.error import InputError, AccessError


def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__)
# app = Flask(__name__, static_url_path='/static/')
CORS(APP)
# CORS(app)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)


# APP.config['TRAP_HTTP_EXCEPTIONS'] = True
# APP.register_error_handler(Exception, defaultHandler)
# APP.config['MAIL_SERVER'] = 'smtp.gmail.com'
# APP.config['MAIL_PORT'] = 465
# APP.config['MAIL_USERNAME'] = 'cblinker17@gmail.com'
# APP.config['MAIL_PASSWORD'] = 'cs1531f11cblinker'
# APP.config['MAIL_USE_TLS'] = False
# APP.config['MAIL_USE_SSL'] = True
# mail = Mail(APP)


# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })


#############################################################################
#                                                                           #
#                           Server for auth.py by Lan Lin                   #
#                                                                           #
#############################################################################


@APP.route("/auth/register/v2", methods=['POST'])
def auth_register_v2():
    info = request.get_json()
    email = info['email']
    password = info['password']
    name_first = info['name_first']
    name_last = info['name_last']
    result = auth_register_v1(email, password, name_first, name_last)
    dump_data(data)
    return dumps(result)


@APP.route("/auth/login/v2", methods=['POST'])
def auth_login_v2():
    info = request.get_json()
    result = auth_login_v1(info['email'], info['password'])
    dump_data(data)
    return dumps(result)


@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout_v1():
    info = request.get_json()
    result = auth_logout(info['token'])
    dump_data(data)
    return dumps(result)


@APP.route("/auth/passwordreset/request/v1", methods=['POST'])
def auth_passwordreset_request_v1_http():
    info = request.get_json()
    auth_passwordreset_request_v1(info['email'])
    # msg = Message('Reset Code', sender='yourID@gmail.com', recipients=[info['email']])
    # msg.body = f"The code to rest password is {result['reset_code']}"
    # mail.send(msg)

    dump_data(data)
    return dumps({})


@APP.route("/auth/passwordreset/reset/v1", methods=['POST'])
def auth_passwordreset_reset_v1_http():
    info = request.get_json()
    result = auth_passwordreset_reset_v1(info['reset_code'], info['new_password'])
    dump_data(data)
    return dumps(result)


#############################################################################
#                                                                           #
#                           Server for user.py by Lan Lin                   #
#                                                                           #
#############################################################################


@APP.route("/user/profile/v2", methods=['GET'])
def user_profile_v2():
    token = request.args.get('token')
    try:
        u_id = int(request.args.get('u_id'))
    except ValueError as error:
        raise InputError(description='u_id is not int') from error
    result = user_profile_v1(token, u_id)
    dump_data(data)
    return dumps(result)


@APP.route("/users/all/v1", methods=['GET'])
def users_all_v1():
    token = request.args.get('token')
    result = users_all(token)
    dump_data(data)
    return dumps(result)


@APP.route("/user/profile/setname/v2", methods=['PUT'])
def user_profile_setname_v2():
    info = request.get_json()
    result = user_profile_setname_v1(info['token'], info['name_first'], info['name_last'])
    dump_data(data)
    return dumps(result)


@APP.route("/user/profile/setemail/v2", methods=['PUT'])
def user_profile_setemail_v2():
    info = request.get_json()
    result = user_profile_setemail_v1(info['token'], info['email'])
    dump_data(data)
    return dumps(result)


@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def user_profile_sethandle():
    info = request.get_json()
    result = user_profile_sethandle_v1(info['token'], info['handle_str'])
    dump_data(data)
    return dumps(result)


@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def admin_user_remove_v1():
    info = request.get_json()
    result = admin_user_remove(info['token'], info['u_id'])
    dump_data(data)
    return dumps(result)


@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def admin_userpermission_change_v1():
    info = request.get_json()
    result = admin_userpermission_change(info['token'], info['u_id'], info['permission_id'])
    dump_data(data)
    return dumps(result)


@APP.route("/user/profile/uploadphoto/v1", methods=['POST'])
def user_profile_uploadphoto():
    info = request.get_json()
    result = user_profile_uploadphoto_v1(info['token'], info['img_url'], info['x_start'], info['y_start'],
                                         info['x_end'], info['y_end'])
    dump_data(data)
    return dumps(result)


@APP.route("/src/static/<path:path>", methods=['GET'])
def send_photo(path):
    return send_file(f"src/static/{path}")


@APP.route("/user/stats/v1", methods=['GET'])
def user_stats():
    token = request.args.get('token')
    result = user_stats_v1(token)
    dump_data(data)
    return dumps(result)


@APP.route("/users/stats/v1", methods=['GET'])
def users_stats():
    token = request.args.get('token')
    result = users_stats_v1(token)
    dump_data(data)
    return dumps(result)


#############################################################################
#                                                                           #
#                           Server for other.py by Lan Lin                  #
#                                                                           #
#############################################################################


@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    result = clear_v1()
    dump_data(data)
    return dumps(result)


@APP.route("/search/v2", methods=['GET'])
def search():
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    result = search_v1(token, query_str)
    dump_data(data)
    return dumps(result)


@APP.route("/notifications/get/v1", methods=['GET'])
def notifications():
    token = request.args.get('token')
    result = notification_get_v1(token)
    dump_data(data)
    return dumps(result)


#############################################################################
#                                                                           #
#                           Server for channel.py by Lan Lin                #
#                                                                           #
#############################################################################


@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    info = request.get_json()
    result = channel_invite_v1(info['token'], info['channel_id'], info['u_id'])
    dump_data(data)
    return dumps(result)


@APP.route("/channel/details/v2", methods=['GET'])
def channel_details():
    token = request.args.get('token')
    try:
        channel_id = int(request.args.get('channel_id'))
    except ValueError as error:
        raise InputError(description="channel_id is not int") from error
    result = channel_details_v1(token, channel_id)
    dump_data(data)
    return dumps(result)


@APP.route("/channel/join/v2", methods=['POST'])
def channel_join():
    info = request.get_json()
    result = channel_join_v1(info['token'], info['channel_id'])
    dump_data(data)
    return dumps(result)


@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner():
    info = request.get_json()
    result = channel_addowner_v1(info['token'], info['channel_id'], info['u_id'])
    dump_data(data)
    return dumps(result)


@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_remove_owner():
    info = request.get_json()
    result = channel_removeowner_v1(info['token'], info['channel_id'], info['u_id'])
    dump_data(data)
    return dumps(result)


@APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
    info = request.get_json()
    result = channel_leave_v1(info['token'], info['channel_id'])
    dump_data(data)
    return dumps(result)


@APP.route("/channel/messages/v2", methods=['GET'])
def channel_message():
    token = request.args.get("token")
    try:
        channel_id = int(request.args.get("channel_id"))
    except ValueError as error:
        raise InputError(description="channel_id is not int") from error
    try:
        start = int(request.args.get("start"))
    except ValueError as error:
        raise InputError(description="start is not int") from error
    result = channel_messages_v1(token, channel_id, start)
    dump_data(data)
    return dumps(result)


#############################################################################
#                                                                           #
#                           Server for channels.py by Lan Lin               #
#                                                                           #
#############################################################################


@APP.route("/channels/create/v2", methods=['POST'])
def channels_create():
    info = request.get_json()
    result = channels_create_v1(info['token'], info['name'], info['is_public'])
    dump_data(data)
    return dumps(result)


@APP.route("/channels/list/v2", methods=['GET'])
def channel_list():
    token = request.args.get('token')
    result = channels_list_v1(token)
    dump_data(data)
    return dumps(result)


@APP.route("/channels/listall/v2", methods=['GET'])
def channel_listall():
    token = request.args.get('token')
    result = channels_listall_v1(token)
    dump_data(data)
    return dumps(result)


#############################################################################
#                                                                           #
#                           Server for message.py by Lan Lin                #
#                                                                           #
#############################################################################


@APP.route("/message/send/v2", methods=['POST'])
def message_send():
    info = request.get_json()
    result = message_send_v2(info['token'], info['channel_id'], info['message'])
    dump_data(data)
    return dumps(result)


@APP.route("/message/senddm/v1", methods=['POST'])
def message_senddm():
    info = request.get_json()
    result = message_senddm_v1(info['token'], info['dm_id'], info['message'])
    dump_data(data)
    return dumps(result)


@APP.route("/message/edit/v2", methods=['PUT'])
def message_edit():
    info = request.get_json()
    result = message_edit_v2(info['token'], info['message_id'], info['message'])
    dump_data(data)
    return dumps(result)


@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove():
    info = request.get_json()
    result = message_remove_v1(info['token'], info['message_id'])
    dump_data(data)
    return dumps(result)


@APP.route("/message/share/v1", methods=['POST'])
def message_share():
    info = request.get_json()
    result = message_share_v1(info['token'], info['og_message_id'], info['message'], info['channel_id'], info['dm_id'])
    dump_data(data)
    return dumps(result)


@APP.route("/message/sendlater/v1", methods=['POST'])
def message_sendlater():
    info = request.get_json()
    result = message_sendlater_v1(info['token'], info['channel_id'], info['message'], info['time_sent'])
    dump_data(data)
    return dumps(result)


@APP.route("/message/sendlaterdm/v1", methods=['POST'])
def message_sendlaterdm():
    info = request.get_json()
    result = message_sendlaterdm_v1(info['token'], info['dm_id'], info['message'], info['time_sent'])
    dump_data(data)
    return dumps(result)


@APP.route("/message/react/v1", methods=['POST'])
def message_react():
    info = request.get_json()
    result = message_react_v1(info['token'], info['message_id'], info['react_id'])
    dump_data(data)
    return dumps(result)


@APP.route("/message/unreact/v1", methods=['POST'])
def message_unreact():
    info = request.get_json()
    result = message_unreact_v1(info['token'], info['message_id'], info['react_id'])
    dump_data(data)
    return dumps(result)


@APP.route("/message/pin/v1", methods=['POST'])
def message_pin():
    info = request.get_json()
    result = message_pin_v1(info['token'], info['message_id'])
    dump_data(data)
    return dumps(result)


@APP.route("/message/unpin/v1", methods=['POST'])
def message_unpin():
    info = request.get_json()
    result = message_unpin_v1(info['token'], info['message_id'])
    dump_data(data)
    return dumps(result)


#############################################################################
#                                                                           #
#                           Server for dm.py by Zheng Luo                   #
#                                                                           #
#############################################################################


@APP.route("/dm/create/v1", methods=['POST'])
def http_dm_create_v1():
    info = request.get_json()
    token = info['token']
    u_ids = info['u_ids']
    result = dm_create_v1(token, u_ids)
    dump_data(data)
    return dumps(result)


@APP.route("/dm/invite/v1", methods=['POST'])
def http_dm_invite_v1():
    info = request.get_json()
    token = info['token']
    dm_id = info['dm_id']
    u_id = info['u_id']
    result = dm_invite_v1(token, dm_id, u_id)
    dump_data(data)
    return dumps(result)


@APP.route("/dm/remove/v1", methods=['DELETE'])
def http_dm_remove_v1():
    info = request.get_json()
    token = info['token']
    dm_id = info['dm_id']
    result = dm_remove_v1(token, dm_id)
    dump_data(data)
    return dumps(result)


@APP.route("/dm/leave/v1", methods=['POST'])
def http_dm_leave_v1():
    info = request.get_json()
    token = info['token']
    dm_id = info['dm_id']
    result = dm_leave_v1(token, dm_id)
    dump_data(data)
    return dumps(result)


@APP.route("/dm/details/v1", methods=['GET'])
def http_dm_detail_v1():
    token = request.args.get('token')
    try:
        dm_id = int(request.args.get('dm_id'))
    except ValueError as error:
        raise InputError(description="dm_id is not an int") from error
    result = dm_details_v1(token, dm_id)
    dump_data(data)
    return dumps(result)


@APP.route("/dm/list/v1", methods=['GET'])
def http_dm_list_v1():
    token = request.args.get('token')
    result = dm_list_v1(token)
    dump_data(data)
    return dumps(result)


@APP.route("/dm/messages/v1", methods=['GET'])
def http_dm_messages_v1():
    token = request.args.get('token')
    try:
        dm_id = int(request.args.get('dm_id'))
    except ValueError as error:
        raise InputError(description="dm_id is not int") from error
    try:
        start = int(request.args.get('start'))
    except ValueError as error:
        raise InputError(description="start is not int") from error
    result = dm_messages_v1(token, dm_id, start)
    dump_data(data)
    return dumps(result)


#############################################################################
#                                                                           #
#                           Server for standup.py by Lan Lin                #
#                                                                           #
#############################################################################


@APP.route("/standup/start/v1", methods=['POST'])
def standup_start():
    info = request.get_json()
    result = standup_start_v1(info['token'], info['channel_id'], info['length'])
    dump_data(data)
    return dumps(result)


@APP.route("/standup/active/v1", methods=['GET'])
def standup_active():
    token = request.args.get('token')
    if request.args.get('channel_id') is None:
        raise InputError(description='channel_id is not int')
    try:
        channel_id = int(request.args.get('channel_id'))
    except ValueError as error:
        raise InputError(description='channel_id is not int') from error
    result = standup_active_v1(token, channel_id)
    dump_data(data)
    return dumps(result)


@APP.route("/standup/send/v1", methods=['POST'])
def standup_send():
    info = request.get_json()
    result = standup_send_v1(info['token'], info['channel_id'], info['message'])
    dump_data(data)
    return dumps(result)


if __name__ == "__main__":
    APP.run(port=config.port)  # Do not edit this port
    # app.run()
