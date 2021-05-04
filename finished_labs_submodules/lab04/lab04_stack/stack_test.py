from stack import Stack
import pytest


def test_push():
    s = Stack()
    s.stack_push(1)
    assert(s.stack == [1])


def test_pop():
    s = Stack()
    s.stack_push(1)
    s.stack_pop()
    assert(s.stack == [])


def test_pop_when_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.stack_pop()
