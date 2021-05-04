def divisors(n):
    '''
    Given some number n, return a set of all the numbers that divide it. For example:
    >>> divisors(12)
    {1, 2, 3, 4, 6, 12}

    Params:
      n (int): The operand

    Returns:
      (set of int): All the divisors of n

    Raises:
      ValueError: If n is not a positive integer
    '''
    if type(n) != int or n <= 0:
        raise ValueError("n is not a positive integer")

    return_set = set()
    for i in range(1, n):
        if n % i == 0:
            return_set.add(i)
    return_set.add(n)
    return return_set


if __name__ == "__main__":
    print(divisors(5))
