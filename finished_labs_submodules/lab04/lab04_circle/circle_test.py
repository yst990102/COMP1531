from circle import Circle
import pytest


def test_small():
    c = Circle(3)
    assert(round(c.circumference(), 1) == 18.8)
    assert(round(c.area(), 1) == 28.3)


def test_negative():
    with pytest.raises(ValueError):
        Circle(-1)

def test_zero():
    with pytest.raises(ValueError):
        Circle(0)