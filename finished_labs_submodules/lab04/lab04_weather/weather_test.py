from weather import weather
import pytest


def test_normal():
    assert (weather("08-08-2010", "Albury") == (10.8, 10.0))


def test_NA():
    with pytest.raises(ValueError):
        weather("11-09-2009", "Albury")


def test_invalid_location():
    with pytest.raises(ZeroDivisionError):
        weather("11-09-2009", "NoWhere")
