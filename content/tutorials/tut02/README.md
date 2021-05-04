# Tutorial 2

## A. Code Review

Review this piece of code.
* What does it do?
* What style could be improved here?
* Is this code [pythonic](https://www.computerhope.com/jargon/p/pythonic.htm)? Fix it.

```python
x=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = []

for idx in range(len(x)):
  if x[idx] % 2 == 0:
    result.append(x[idx] * 2)
  else:
    result.append(x[idx])

print(result)
```

> Issues:
> * Spacing not consistent
> * Indentation not 4 spaces (refer to style guide on webcms3)
> * Could use for-range loop in this case
> * `range(len(x))` is redundant, could just use range normally

> Could make things even shorter:
```python
[(element * 2 if element % 2 == 0 else element) for element in x]
```

## B. Thinking about testing

The following `set_name` function is used to set a name according to the follow requirements on input:
 * First Name must be at least 3 characters, and no more than 30.
 * Last Name must be at least 3 characters, and no more than 50.
 * First Name can only contain letters (uppercase or lowercase), and dashes.
 * Last Name can only contain letters (uppercase or lowercase), spaces, and dashes.
 * Middle Name can be None, but if it's not none, it can be between 1 and 50 characters.
 * Middle Name cannot be longer than the first name, and it cannot be longer than the last name.

Your tutor will break you up into your project groups for this activity. Once completed you can come back together to discuss what you have.

The function returns `True` if the inputs are valid, and `False` if the inputs are invalid.

```python
def set_name(firstName, middleName, lastName):
	pass
```

Write a list of inputs and associated return values. This is good practice for trying to conceptualise edge case.

> len(First name) < 3 characters => False
> len(First name) > 30 characters => False
> len(Last name) < 3 characters => False
> len(Last name) > 50 characters => False
> Series of tests for first names containing ASCII that aren't `-` or `[a-zA-Z]` => False
> Series of tests for last names containing ASCII that aren't `-` or `[a-zA-Z]` => False
> Middle name != None and Middle name = '' => False
> len(Middle name) > len(First name) || len(Middle name) > len(Last name) => False
> If all states are valid => True

## C. Testing in python

Consider this problem:

 > Given a list of integers, compute the average of only the *positive* elements.

Your tutor will clone `tutorials.git` and go into the `tut02` folder.

There is a stub for a function that solves this problem in [rainfall.py](rainfall.py). Before implementing it, write some pytest compatible tests for the function.

* What needs to be tested for?
* What are the edge cases and how should they be handled?

Once the tests are written, commit them to git.

## D. Python programming

On a separate branch (`rainfall_solution`), implement the function such that it passes all the tests.

* How confident are you that your solution is correct?
* Is your solution very different from how you might do it in C?

Go back to the `master` branch and try to implement the function a different way. If your previous solution did not use the `sum()` function, rewrite it so it does. If your previous solution *did* use the `sum()` function, rewrite it so it doesn't (also avoiding an intermediate list).

After testing it to ensure correctness, commit this alternate solution to `master`.

> See [rainfall.py](solutions/rainfall.py).

## E. Git merges

Try to merge `rainfall_solution` back into `master`. This will create a merge conflict.

With the class, discuss which solution is better and how you might resolve the merge conflict to ensure it is the one used.

## F. Fixtures

If merge conflict was not resolved by `Accept Both Changes` undo the until before the merge conflict and this time keep both solution and put them in 2 different functions (can name the other one `rainfall_alternative`).

```python
def rainfall(integers):
    ''' Single-loop solution '''
    total = 0
    count = 0
    for i in integers:
        if  i > 0:
            total += i
            count += 1
    if (count > 0):
        return total/count
    else:
        return None

def rainfall_alternative(integers):
    ''' List-comprehension solution '''
    positive = [i for i in integers if i > 0]
    if (len(positive) > 0):
        return sum(positive)/len(positive)
    else:
        return None
```

Copy the first test and replace the function call to `rainfall` with `rainfall_alternative` (don't forget to change the name of the test function too).

```python
def test_simple_alternative():
    assert rainfall_alternative([1, 2, 3]) == 2
```

Make sure the test still passes, now instead of passing the same test data to `rainfall` and `rainfall_alternative`, put it in a `fixture` and pass that to both of the test functions.

```python
import pytest

@pytest.fixture
def test_data_set():
    return [1, 2, 3]

def test_simple(test_data_set):
    assert rainfall(test_data_set) == 2

def test_simple_alternative(test_data_set):
    assert rainfall_alternative(test_data_set) == 2
```

> See [rainfall.py](solutions/rainfall.py).
