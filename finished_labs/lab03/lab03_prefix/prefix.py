def prefix_search(dictionary, key_prefix):
    '''
    Given a dictionary (with strings for keys) and a string, returns a new dictionary containing only the keys (and their corresponding values) for which the string is a prefix.
    If the string is not a prefix for any key, a KeyError is raised.
    You can assume that you will not be given any empty strings in dictionary or as key_prefix

    For example,
    >>> prefix_search({"ac": 1, "ba": 2, "ab": 3}, "a")
    {'ac': 1, 'ab': 3}
    '''
    result_dict = {}
    for i in dictionary.keys():
        inside = True
        for j in range(0, len(key_prefix)):
            if key_prefix[j] != i[j]:
                inside = False
                break
        if inside == True:
            result_dict[i] = dictionary[i]
    return result_dict
