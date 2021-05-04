import primes
from primes import factors


def test_repeat_factors():
    assert(factors(16) == [2, 2, 2, 2])


def test_prime():
    assert(factors(2) == [2])
    assert(factors(3) == [3])
    assert(factors(5) == [5])
    assert(factors(7) == [7])
    assert(factors(11) == [11])

def test_normal():
    assert(factors(30) == [2,3,5])
    assert(factors(110) == [2,5,11])
