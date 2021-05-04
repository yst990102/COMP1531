import pytest
from auth import auth_register
from channels import channels_create
from message import message_send
from error import InputError

@pytest.fixture
def get_new_user():
    data = auth_register('hayden.smith@unsw.edu.au', '123!@#asd', 'Hayden', 'Smith')
    return (data['u_id'], data['token'])

def test_message_send(get_new_user):
    u_id, token = get_new_user
    data = channels_create(token, 'my channel', False)
    with pytest.raises(InputError) as e:
        message_send(token, data['channel_id'], 'Hello there' * 1001)

def test_channels_create(get_new_user):
    u_id, token = get_new_user
    data = channels_create(token, 'my channel', False)