from factors import factors, is_prime
from hypothesis import given, strategies
import inspect
import pytest


def test_generator():
    '''
    Ensure it is generator function
    '''
    assert inspect.isgeneratorfunction(factors), "factors does not appear to be a generator"


def test_int_less_than_one():
    with pytest.raises(ValueError):
        list(factors(-1))
    with pytest.raises(ValueError):
        list(factors(0))
    pass


def test_invalid_int():
    with pytest.raises(ValueError):
        list(factors("string"))
    with pytest.raises(ValueError):
        list(factors(None))
    with pytest.raises(ValueError):
        list(factors([1, 2, 3]))
    pass


def test_prime_num():
    assert list(factors(5)) == [1, 5]
    assert list(factors(13)) == [1, 13]
    assert list(factors(97)) == [1, 97]
    pass


def test_non_prime_num():
    assert list(factors(15)) == [3, 5]
    assert list(factors(50)) == [2, 5, 5]
    assert list(factors(1500)) == [2, 2, 3, 5, 5, 5]
    pass
