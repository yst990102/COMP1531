import pytest

def sum(x, y):
    return x * y

def test_sum1():
    assert sum(1, 2) == 3, "1 + 2 == 3"
