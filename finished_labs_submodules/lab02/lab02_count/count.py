def count_char(input):
    """
    Counts the number of occurrences of each character in a string. The result should be a dictionary where the key is the character and the dictionary is its count.

    For example,
    >>> count_char("HelloOo!")
    {'H': 1, 'e': 1, 'l': 2, 'o': 2, 'O': 1, '!': 1}
    """

    dict = {}
    for i in input:
        if i not in dict.keys():
            dict[i] = 1
        else:
            dict[i] += 1
    return dict
