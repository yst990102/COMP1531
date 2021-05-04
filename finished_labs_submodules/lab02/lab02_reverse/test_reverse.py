"""
Tests for reverse_words()
"""
from reverse import reverse_words


def test_example():
    assert reverse_words(["Hello World", "I am here"]) == ["World Hello", "here am I"]


# my tests
def test01():
    assert reverse_words(["hello everyone", "i am steven yuan"]) == ["everyone hello", "yuan steven am i"]


def test02():
    assert reverse_words(["Today is 2021-02-26.", "I am a student from 1531."]) == ["2021-02-26. is Today", "1531. from student a am I"]


def test03():
    assert reverse_words(["who are you?", "i am shi tong yuan"]) == ["you? are who", "yuan tong shi am i"]


def test04():
    assert reverse_words(["/n/r/t", "%c %d %s %u"]) == ["/n/r/t", "%u %s %d %c"]


def test05():
    assert reverse_words(["English == 中文", "hello == 你好"]) == ["中文 == English", "你好 == hello"]