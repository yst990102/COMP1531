def reverse_words(string_list):
    '''
    Given a list of strings, return a new list where the order of the words is
    reversed
    '''
    new_list = string_list
    for i in new_list:
        # print(' '.join(i.split()[::-1]))
        new_list[new_list.index(i)] = ' '.join(i.split()[::-1])

    return new_list


if __name__ == "__main__":
    print(reverse_words(["Hello World", "I am here"]))
    # it should print ['World Hello', 'here am I']
