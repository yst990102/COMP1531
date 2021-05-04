def balanced(n):
    '''
    Given a positive number n, compute the set of all strings of length n, in any order, that only
    contain balanced brackets. For example:
    >>> balanced(6)
    {'((()))', '(()())', '(())()', '()(())', '()()()'}

    Note that, by definition, the only string of length 0 containing balanced brackets is the empty
    string.

    Params:
      n (int): The length of string we want

    Returns:
      (set of str): Each string in this set contains balanced brackets. In the event n is odd, this
      set is empty.

    Raises:
      ValueError: If n is negative
    '''
    if type(n) != int:
        raise ValueError("n is not int.")
    elif n < 0:
        raise ValueError("n is negative.")
    elif n == 0:
        return {}

    def permutations(string):

        # Idea 02 : with recursion
        if len(string) <= 1:
            return set([string])
        string_list = []
        for i in range(len(string)):
            for j in permutations(string[0:i] + string[i + 1:]):
                string_list.append(string[i] + j)
        return set(string_list)

    def remove_item(string):
        open__bracket_num = 0
        close_bracket_num = 0
        for i in string:
            if i == "(":
                open__bracket_num += 1
            else:
                close_bracket_num += 1
            if close_bracket_num > open__bracket_num:
                return False
        if close_bracket_num == open__bracket_num:
            return True
        else:
            return False

    string_bracket = ""
    for i in range(int(n/2)):
        string_bracket = string_bracket.join("()")

    permutations_set = permutations(string_bracket)
    for i in permutations_set.copy():
        if remove_item(i) == False:
            permutations_set.remove(i)

    return permutations_set


if __name__ == "__main__":
    print((balanced(6)) == {'((()))', '(()())', '(())()', '()(())', '()()()'})
