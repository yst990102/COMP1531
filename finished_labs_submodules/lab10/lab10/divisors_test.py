from divisors import divisors
from hypothesis import given, strategies
import pytest


def test_not_int():
    with pytest.raises(ValueError):
        divisors(0.123)
    with pytest.raises(ValueError):
        divisors("string")
    with pytest.raises(ValueError):
        divisors(None)


def test_negative_int():
    with pytest.raises(ValueError):
        divisors(-1)


def test_zero():
    with pytest.raises(ValueError):
        divisors(0) == 1


def test_12():
    assert divisors(12) == {1, 2, 3, 4, 6, 12}
