import pytest
from src.other import clear_v1
from src.echo import echo
from src.error import InputError


def test_echo():
    assert echo("1") == "1", "1 == 1"
    assert echo("abc") == "abc", "abc == abc"
    assert echo("trump") == "trump", "trump == trump"

    clear_v1()


def test_echo_except():
    with pytest.raises(InputError):
        assert echo("echo")

    clear_v1()
