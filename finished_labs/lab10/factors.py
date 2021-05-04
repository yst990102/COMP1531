'''
NOTE: This exercise assumes you have completed divisors.py
'''

from divisors import divisors

# You may find this helpful


def is_prime(n):
    return n != 1 and divisors(n) == {1, n}


def factors(n):
    '''
    A generator that generates the prime factors of n. For example
    >>> list(factors(12))
    [2,2,3]

    Params:
      n (int): The operand

    Yields:
      (int): All the prime factors of n in ascending order.

    Raises:
      ValueError: When n is <= 1.
    '''
    if type(n) != int:
        raise ValueError("n is not int.")
    elif n <= 1:
        raise ValueError("n is <= 1.")

    if is_prime(n):
        yield 1
        yield n
    else:
        dividend = n
        for i in range(2, n):
            if is_prime(i):
                while dividend % i == 0:
                    dividend /= i
                    yield i
