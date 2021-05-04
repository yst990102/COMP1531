from fibonacci import generate


def test_none():
    assert generate(0) == []


def test_01():
    assert generate(1) == [0]


def test_02():
    assert generate(2) == [0, 1]


def test_03():
    assert generate(3) == [0, 1, 1]


def test_04():
    assert generate(4) == [0, 1, 1, 2]


def test_05():
    assert generate(5) == [0, 1, 1, 2, 3]
