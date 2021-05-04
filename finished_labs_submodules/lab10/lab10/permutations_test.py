import itertools
from permutations import permutations
from hypothesis import given, strategies, assume


def test_empty():
    string = ""

    expected = set()
    for i in itertools.permutations(string, len(string)):
        expected.add("".join(i))

    assert permutations(string) == expected


def test_one_char():
    string = "a"

    expected = set()
    for i in itertools.permutations(string, len(string)):
        expected.add("".join(i))

    assert permutations(string) == expected


def test_normal01():
    string = "abc"

    expected = set()
    for i in itertools.permutations(string, len(string)):
        expected.add("".join(i))

    assert permutations(string) == expected


def test_normal02():
    string = "ABCDEFG"

    expected = set()
    for i in itertools.permutations(string, len(string)):
        expected.add("".join(i))

    assert permutations(string) == expected
