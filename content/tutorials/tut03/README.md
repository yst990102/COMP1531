# Tutorial 3

## A. Code Review

Your tutor will select one of your classmate's code from lab02 to present and discuss as a class.

Is the code:
* Compliant with the COMP1531/Google style guide?
* Pythonic in nature?

## B. Agile

Each group in the tutorial should share a summary of their teams plans and progress in relation to:
 * When (or if) they are running standups and whether they are synchronous or asynchronous
 * How often they meet, how they meet, and what the goals/outcomes of any meetings so far have been
 * Have they or will they try pair programming
 * Any challenges they've faced already after being in a group for a week

Other group members (in other teams) are encouraged to ask questions and learn from what other groups are doing/saying.

## C. Dictionaries

Write a python program `vowel.py` that takes in a series of words on a single line in from STDIN, passes that input string into a function called `find_vowels`, which then return the frequency of how often each vowel appears. This object is then outputted (however you think works best). Assume all input is lowercase or uppercase letters, or spaces.

If there are any uppercase letters passed in as part of the input, a `ValueError` should be thrown and caught in the main part of the code. The user should then be given a clear error.

```python
import sys

def find_vowels(inp):
    vowels = {}
    if not inp.islower():
        raise ValueError
    for character in 'aeiou':
        vowels[character] = 0
    words = inp.split(' ')
    for word in words:
        for character in word:
            if character in 'aeiou':
                vowels[character] += 1
    return vowels

if __name__ == '__main__':
    words = sys.stdin.readline()
    try:
        vowels = find_vowels(words)
        for character in 'aeiou':
            print(f"{character}: {vowels[character]}")
    except ValueError:
        print("Please only enter lowercase letters")
```

## D. Importing

Here is a file *foo.py*
```python
def bar(txt):
    return txt

name = 'Ralph'
def editName(string):
    name = string
def getName():
    return name
```

In the same directory we have a file *imp.py*. There are multiple ways we can import and use a function in another file. Discuss each.
```python
import foo
print(foo.bar('hi')) # 1

import foo as fooFile
print(fooFile.bar('hi')) # 2

from foo import bar
print(bar('hi')) # 3

from foo import *
print(bar('hi')) # 4
```

> * #1 This is fine, and is useful when using many functions from an import
> * #2 This is like (#1), except useful when the name of the import is quite generic and could be confused with something else
> * #3 This is often useful when you only need to import very particular functions from a file
> * #4 This is not recommended, this imports a whole number of functions that could conflict with other names in the namespace

Why does the following function not behave as intended?
```python
import foo

print(foo.getName())
foo.editName('Hayden')
print(foo.getName())
```

> Because to edit global variables inside of functions we need to add a global keyword
```python
def editName(string):
    global name
    name = string
```
