
def neighbours(iterable):
    '''
    A generator, that, given an iterable, yields the "neighbourhood" of each
    element. The neighbourhood is a tuple containing the element itself as well
    as the one that comes before and the one that comes after. For example,
    >>> list(neighbours([1,2,3,4]))
    [(1,2), (1,2,3), (2,3,4), (3,4)]

    Note that the first and last elements are pairs, while the rest are triples.

    Params:
      iterable (iterable): The iterable being processed. In the event it's empty,
      this generator should not yield anything. In the event it only contains
      one element, only that element should be yielded in a one-tuple.

    Yields:
      (tuple) : The neighbourhood of the current element.
    '''
    # Hint: Don't forget that iterables can produce values infinitely. You can't
    # rely on being able to retrieve all the elements at once.

    iterable_list = list(iterable)
    if len(iterable_list) == 0:
        return
    elif len(iterable_list) == 1:
        yield (iterable_list[0],)
    else:
        yield (iterable_list[0], iterable_list[1])

        for i in range(1, len(iterable_list)-1):
            yield (iterable_list[i-1], iterable_list[i], iterable_list[i+1])
        yield (iterable_list[len(iterable_list) - 2], iterable_list[len(iterable_list) - 1])
