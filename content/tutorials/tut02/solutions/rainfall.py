import pytest
'''
Compute the average of only the positive elements in the list.
'''
def rainfall(integers):
    ''' Single-loop solution '''
    total = 0
    count = 0
    for i in integers:
        if  i > 0:
            total += i
            count += 1
    if (count > 0):
        return total/count
    else:
        return None

def rainfall_alternative(integers):
    ''' List-comprehension solution '''
    positive = [i for i in integers if i > 0]
    if (len(positive) > 0):
        return sum(positive)/len(positive)
    else:
        return None

@pytest.fixture
def test_data_set():
    return [1, 2, 3]

def test_simple(test_data_set):
    assert rainfall(test_data_set) == 2

def test_simple_alternative(test_data_set):
    assert rainfall_alternative(test_data_set) == 2

def test_negative():
    assert rainfall([1, -5, 3, 4, 4]) == 3

def test_zero():
    assert rainfall([1, 0, 2, 3]) == 2

def test_empty():
    assert rainfall([-1, -2, -3]) == None
