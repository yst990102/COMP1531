def inverse(d):
    '''
    Given a dictionary d, invert its structure such that values in d map to lists of keys in d.
    For example:
    >>> inverse({1: 'A', 2: 'B', 3: 'A'})
    {'A': [1, 3], 'B': [2]}

    Params:
      d (dict): A dictionary where all the values are hashable (i.e. can be used as keys in the
      result).

    Returns:
      (dict): A dictionary with the structure described above.
    '''
    d_list = list(d.items())

    dict_return = {}
    for i in d_list:
        first = i[0]
        second = i[1]
        if second not in dict_return.keys():
            dict_return[second] = [first]
        else:
            dict_return[second].append(first)

    return dict_return


if __name__ == "__main__":
    print(inverse({}))
    print(inverse({"": "1"}))
    print(inverse({1: 'A', 2: 'B', 3: 'A'}))
    print(inverse({1: 'A', 2: 'B', 3: 'A', 4: 'B', 6: 'A'}))
