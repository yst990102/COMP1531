from list_exercises import *


def test_reverse():
    l = ["how", "are", "you"]
    reverse_list(l)
    assert l == ["you", "are", "how"]
    # my tests
    list1 = ["123", 123, ["i", "am", "fine"]]
    reverse_list(list1)
    assert list1 == [["i", "am", "fine"], 123, "123"]

    list2 = [("python", "321yst"), {"a": 1, "b": 2}, 3.1415, "Pi"]
    reverse_list(list2)
    assert list2 == ["Pi", 3.1415, {"a": 1, "b": 2}, ("python", "321yst")]

    list3 = ["who", "are", "you"]
    reverse_list(list3)
    assert list3 == ["you", "are", "who"]

    list4 = ["990102", "are", "you", "?"]
    reverse_list(list4)
    assert list4 == ["?", "you", "are", "990102"]


def test_min_positive():
    assert minimum([1, 2, 3, 10]) == 1
    # my tests
    assert minimum([4, 6, 7, 2, 9]) == 2
    assert minimum([99, 12, 66, 3]) == 3
    assert minimum([46, 62, 7, 2, 9]) == 2
    assert minimum([99, 1, 66, 3]) == 1


def test_sum_positive():
    assert sum_list([7, 7, 7]) == 21
    # my tests
    assert sum_list([1, 2, 3, 4, 5]) == 15
    assert sum_list([12, 19, 1, 3]) == 35
    assert sum_list([11, 2, 3, 4, 5]) == 25
    assert sum_list([2, 19, 1, 33]) == 55
