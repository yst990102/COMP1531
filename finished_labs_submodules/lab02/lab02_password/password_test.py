"""
Tests for check_password()
"""
from password import check_password


def test_for_strong_password():
    assert check_password("Asdfghjkl987321") == "Strong password"


def test_for_moderate_password():
    assert check_password("styuan0102") == "Moderate password"


def test_for_horrible_password():
    assert check_password("password") == "Horrible password"
    assert check_password("iloveyou") == "Horrible password"
    assert check_password("123456") == "Horrible password"


def test_for_poor_password():
    assert check_password("yst0102") == "Poor password"
    assert check_password("ZXCVBBNMASDFGH") == "Poor password"
    assert check_password("sadfasdfasdf") == "Poor password"


def test_for_empty_input():
    assert check_password("") == "Poor password"