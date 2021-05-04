import math


def factors(num):
    '''
    Returns a list containing the prime factors of 'num'. The primes should be
    listed in ascending order.

    For example:
    >>> factors(16)
    [2, 2, 2, 2]
    >>> factors(21)
    [3, 7]
    '''
    i = 2
    maximum = num
    return_list = []
    while i <= maximum:
        if num % i == 0:
            return_list.append(i)
            num /= i
        else:
            i += 1
    return return_list
