from inverse import inverse
from hypothesis import given, strategies


def test_empty():
    assert inverse({}) == {}


def test_one_element():
    assert inverse({"": "1"}) == {"1": [""]}


def test_normal01():
    assert inverse({1: 'A', 2: 'B', 3: 'A'}) == {'A': [1, 3], 'B': [2]}


def test_normal02():
    assert inverse({1: 'A', 2: 'B', 3: 'A', 4: 'B', 6: 'A', 7: 'C', 8: 'D'}) == {'A': [1, 3, 6], 'B': [2, 4], 'C': [7], 'D': [8]}
