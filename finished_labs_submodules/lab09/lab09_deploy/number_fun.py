import typing


def multiply_by_two(number: int) -> int:
    '''
    Multiplies a given number by two.
    '''
    return number * 2
    pass


def print_message(message: str) -> None:
    '''
    Prints a given message.
    '''
    print(message)
    pass


def sum_list_of_numbers(numbers: typing.List[int]) -> int:
    '''
    Returns the sum of a list of numbers
    '''
    sum_of_numbers = 0
    for i in numbers:
        sum_of_numbers += i
    return sum_of_numbers
    pass


def sum_iterable_of_numbers(numbers: typing.List[int]) -> int:
    '''
    Calculates the sum of an iterable of numbers

    numbers: any iterable

    Return value: integer
    '''
    return sum(numbers)
    pass


def is_in(needle: typing.Union[str, int], haystack: typing.Union[str, int]) -> bool:
    '''
    Checks if the given item is in a list

    Parameters:
    - needle: a string or an integer
    - haystack: a list of strings or integers

    Return value: bool - if the needle is in the haystack
    '''
    if needle in haystack:
        return True
    else:
        return False


def index_of_number(item: int, numbers: typing.List[int]) -> typing.Union[None, int]:
    '''
    Returns the index of the given item in a list of numbers

    Parameters:
    - item: an integer
    - numbers: a list of numbers

    Return value: the index of the item, or None if the items is not in numbers
    '''
    try:
        return numbers.index(item)
    except ValueError:
        return None
    pass
