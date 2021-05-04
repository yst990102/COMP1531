from roman import roman


def test01():
    assert (roman("II")) == 2


def test02():
    assert (roman("IV")) == 4


def test03():
    assert (roman("IX")) == 9


def test04():
    assert (roman("XIX")) == 19


def test05():
    assert (roman("XX")) == 20


def test06():
    assert (roman("MDCCLXXVI")) == 1776


def test07():
    assert (roman("MMXIX")) == 2019