import pickle
from datetime import datetime, timezone
"""
Define different classes: User, Channel, Message
Define data structure: data
Written by: Lan Lin
"""


class Permission:
    global_owner = 1
    global_member = 2


class Status:
    offline = 0
    online = 1
    busy_working = 2
    leave_away = 3


class User:
    def __init__(self, u_id, email, hashed_password, name_first, name_last, handle_str, auth_user_id, permission_id, status):
        self.u_id = u_id
        self.email = email
        self.hashed_password = hashed_password
        self.name_first = name_first
        self.name_last = name_last
        self.handle_str = handle_str
        self.auth_user_id = auth_user_id
        self.permission_id = permission_id
        self.part_of_channel = []
        self.part_of_dm = []
        self.dm_owns = []
        self.channel_owns = []  # a list of all channels that the user is the owner of the channel
        self.current_sessions = []  # a list of current sessions of the user
        self.notifications = []
        self.messages = []
        self.channels_joined = []
        self.dms_joined = []
        self.messages_sent = []
        self.image_url = 'https://static.boredpanda.com/blog/wp-content/uploads/2020/05/700-1.jpg'
        self.image_path = ''
        self.reset_code = ''
        # bonus points
        self.asciimoji = {"<acid>": "⊂(◉‿◉)つ", "<afraid>": "(ㆆ _ ㆆ)", "<angry>": "•`_´•", "<catlenny>": "( ͡° ᴥ ͡°)"}
        self.common_words = ["I will be back soon.", "On my way, baby.", "How is it recently?"]

        self.status = status
        self.login_time = -1
        self.online_time = current_time() - self.login_time

    def return_type_user_v2(self):
        return {
            'u_id': self.u_id,
            'email': self.email,
            'name_first': self.name_first,
            'name_last': self.name_last,
            'handle_str': self.handle_str,
            'profile_img_url': self.image_url
        }


class Channel:
    def __init__(self, name, channel_id, is_public):
        self.start = -1
        self.end = -1
        self.name = name
        self.channel_id = channel_id
        self.is_public = is_public
        if not isinstance(self.is_public, bool):  # is_public must be type of bool
            raise TypeError("is_public must be bool")
        self.all_members = []  # a list of all members of the channel, including members and owners
        self.owner_members = []  # a list of all owners of the channel
        self.messages = []
        self.standup = {'is_active': False, 'time_finish': None}
        self.packaged_messages = []

    def is_standup_active(self):
        return self.standup['is_active']

    def return_time_finish(self):
        return self.standup['time_finish']

    def activate_standup(self):
        self.standup['is_active'] = True

    def deactivate_standup(self):
        self.standup['is_active'] = False

    def set_time_finish(self, in_time_finish):
        self.standup['time_finish'] = in_time_finish

    def clear_time_finish(self):
        self.standup['time_finish'] = None

    def clear_packaged_messages(self):
        self.packaged_messages = []

    def return_type_channel(self):
        """dictionary contains types { channel_id, name }"""
        return {
            'channel_id': self.channel_id,
            'name': self.name
        }


class Message:
    def __init__(self, message_id, u_id, message, time_created, channel_id, dm_id):
        self.message_id = message_id
        self.u_id = u_id
        self.message = message
        self.time_created = time_created
        self.channel_id = channel_id
        self.dm_id = dm_id
        self.is_pinned = False
        self.reacted_users = []

    def return_type_message_v2(self):
        return {
            'message_id': self.message_id,
            'u_id': self.u_id,
            'message': self.message,
            'time_created': self.time_created,
            'reacts': [{'react_id': 1, 'u_ids': [u.u_id for u in self.reacted_users], 'is_this_user_reacted': False}],
            'is_pinned': self.is_pinned
        }


class DM:
    def __init__(self, dm_name, dm_id):
        self.start = -1
        self.end = -1
        self.dm_name = dm_name
        self.dm_id = dm_id
        self.dm_members = []
        self.dm_owners = []
        self.dm_messages = []

    def return_type_dm(self):
        return {
            'dm_id': self.dm_id,
            'name': self.dm_name
        }


class Notification:
    def __init__(self, channel_id, dm_id, notification_message):
        self.channel_id = channel_id
        self.dm_id = dm_id
        self.notification_message = notification_message

    def return_type_notification(self):
        return {
            'channel_id': self.channel_id,
            'dm_id': self.dm_id,
            'notification_message': self.notification_message
        }


DATA = {
    # a list of class User
    'class_users': [],
    # a list of class Channel
    'class_channels': [],
    # a list of class DM
    'class_dms': [],
    # a list of class Message
    'class_messages': [],
    'channels_exist': [],
    'dms_exist': [],
    'messages_exist': [],
    # to record the number of sessions
    'session_num': 0,
    # to record the number of messages
    'message_num': 0,
    # number of channel and dm
    'channel_num': 0,
    'dm_num': 0,
    'secret': 'THIS_IS_SECRET',
}


def load_data():
    global DATA
    try:
        with open("db.p", "rb") as FILE:
            dt = pickle.load(FILE)
            return dt
    except FileNotFoundError:
        with open("db.p", "wb") as FILE:
            pickle.dump(DATA, FILE)
            return DATA


def dump_data(dt):
    with open("db.p", "wb") as FILE:
        pickle.dump(dt, FILE)


def current_time():
    return int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())


data = load_data()
