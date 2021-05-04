from balanced import balanced
from hypothesis import given, strategies
import pytest


def test_invalid_n():
    with pytest.raises(ValueError):
        balanced("string")
    with pytest.raises(ValueError):
        balanced(0.123)
    with pytest.raises(ValueError):
        balanced(None)
    with pytest.raises(ValueError):
        balanced(-1)


def test_zero():
    assert balanced(0) == {}


def test_normal01():
    assert balanced(6) == {'((()))', '(()())', '(())()', '()(())', '()()()'}
