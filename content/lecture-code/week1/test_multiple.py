import pytest

def sum(x, y):
    return x + y

def test_small():
    assert sum(1, 2) == 3, "1, 2 == "
    assert sum(3, 5) == 8, "3, 5 == "
    assert sum(4, 9) == 13, "4, 9 == "

def test_small_negative():
    assert sum(-1, -2) == -3, "-1, -2 == "
    assert sum(-3, -5) == -8, "-3, -5 == "
    assert sum(-4, -9) == -13, "-4, -9 == "

def test_large():
    assert sum(84*52, 99*76) == 84*52 + 99*76, "84*52, 99*76 == "
    assert sum(23*98, 68*63) == 23*98 + 68*63, "23*98, 68*63 == "
   