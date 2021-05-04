from encapsulate import Student
from datetime import datetime
from pytest import fixture

@fixture
def student():
    return Student('Rob', 'Everest', 1961)

def test_name(student):
    assert student.getName() == 'Rob Everest'

def test_age(student):
    assert student.getAge() == datetime.now().year - 1961
