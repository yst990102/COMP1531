from reduce import reduce

def test_none_list():
    assert reduce(lambda x, y: x + y, []) == None

def test_one_element():
    assert reduce(lambda x, y: x + y, [1]) == 1

def test_01():
    assert reduce(lambda x, y: x + y, [1,2,3,4,5]) == 15

def test_02():
    assert reduce(lambda x, y: x + y, 'abcdefg') == 'abcdefg'

def test_03():
    assert reduce(lambda x, y: x * y, [1,2,3,4,5]) == 120