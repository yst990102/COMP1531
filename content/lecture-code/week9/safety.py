from typing import Optional

def count(needle, haystack):
    '''
    Returns the number of copies of integer needle in the list of integers haystack.
    '''
    copies = 0
    for value in haystack:
        if needle == value:
            copies += 1
    return copies
 
def search(needle, haystack):
    '''
    Returns the needle if it's found in the haystack.
    '''
    for i in range(len(haystack)):
        if haystack[i] == needle:
            return needle
    return None

print(count('h', 'haydhen'))
print(search('z', 'haydhen'))
