import json
import pytest
import requests
from server import port


# url = f"http://localhost:{port}/"

url = f"http://cs1531lab09deploy.alwaysdata.net/"


def test_multiply_by_two():
    testcase_01 = requests.get(url + "multiply_by_two?" + "number=2")
    assert json.loads(testcase_01.text) == 4

    testcase_02 = requests.get(url + "multiply_by_two?" + "number=10")
    assert json.loads(testcase_02.text) == 20


def test_print_message():
    testcase_01 = requests.get(url + "print_message?" + "message=COMP1531 is legit my favourite course ever")
    assert testcase_01.text == 'COMP1531 is legit my favourite course ever'


def test_sum_list_of_numbers():
    testcase_01 = requests.get(url + "sum_list_of_numbers?" + "numbers=[1, 2, 3, 4]")
    assert json.loads(testcase_01.text) == 10

    testcase_02 = requests.get(url + "sum_list_of_numbers?" + "numbers=[]")
    assert json.loads(testcase_02.text) == 0


def test_sum_iterable_of_numbers():
    testcase_01 = requests.get(url + "sum_iterable_of_numbers?" + "numbers=[1, 2, 3, 4]")
    assert json.loads(testcase_01.text) == 10

    testcase_02 = requests.get(url + "sum_iterable_of_numbers?" + "numbers={1, 2, 3, 4, 5}")
    assert json.loads(testcase_02.text) == 15

    testcase_03 = requests.get(url + "sum_iterable_of_numbers?" + "numbers=(1, 10, 100, 1000)")
    assert json.loads(testcase_03.text) == 1111


def test_is_in():
    testcase_01 = requests.get(url + "is_in?" + "needle=1" + "&" + "haystack=[1,2,3,4,5]")
    assert testcase_01.text == "True"

    testcase_02 = requests.get(url + "is_in?" + "needle='1'" + "&" + "haystack=[1,2,3,4,5]")
    assert testcase_02.text == "False"

    testcase_03 = requests.get(url + "is_in?" + "needle='a'" + "&" + "haystack=['a', 'b', 'c']")
    assert testcase_03.text == "True"


def test_index_of_number():
    testcase_01 = requests.get(url + "index_of_number?" + "item=1" + "&" + "numbers=[1,2,3,4,5]")
    assert testcase_01.text == "0"

    testcase_02 = requests.get(url + "index_of_number?" + "item=6" + "&" + "numbers=[1,2,3,4,5]")
    assert testcase_02.text == "None"
