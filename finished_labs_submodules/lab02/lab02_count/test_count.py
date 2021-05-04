from count import count_char


def test_empty():
    assert count_char("") == {}


def test_simple():
    assert count_char("abc") == {"a": 1, "b": 1, "c": 1}


def test_double():
    assert count_char("aa") == {"a": 2}


def test_multiple_input():
    assert count_char("abcdefg") == {"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1}


def test_cases_and_numbers():
    assert count_char("Student5192519") == {"S": 1, "t": 2, "u": 1, "d": 1, "e": 1, "n": 1,"5": 2, "1": 2, "9": 2, "2": 1}
