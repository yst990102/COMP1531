def permutations(string):
    '''
    For the given string, compute the set of all permutations of the characters of that string. For example:
    >>> permutations('ABC')
    {'ABC', 'ACB', 'BAC', 'BCA', 'CAB', 'CBA'}

    Params:
      string (str): The string to permute

    Returns:
      (set of str): Each string in this set should be a permutation of the input string.
    '''

    # Idea 01 : by using itertools.permutations
    # result_set = set()
    # for i in itertools.permutations(string, len(string)):
    #     result_set.add("".join(i))
    # return result_set

    # Idea 02 : with recursion
    if len(string) <= 1:
        return set([string])
    string_list=[]
    for i in range(len(string)):
        for j in permutations(string[0:i] + string[i + 1:]):
            string_list.append(string[i] + j)
    return set(string_list)


if __name__ == "__main__":
    print(permutations(''))
