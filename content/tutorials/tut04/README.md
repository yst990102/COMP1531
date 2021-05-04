# Tutorial 4

## A. Code Review

Your tutor will split you up into your project groups, and provide you with a document to share your thoughts on:

* [review_1.py](review_1.py)
* [review_2.py](review_2.py)

Compare these two pieces of code from a pythonic, style, and readability point of view and choose which one you prefer. When you choose one, you must justify your reasoning in the shared document your tutor gives you.

> Discuss with your class their ideas. No right or wrong answer, just discussion.

## B. Requirements

Your tutor may break you up into groups to complete this activity.

* Q. What are attributes of good requirements?
* Q. How could we clean this up into well described requirements? "I want a burger with lots of pickles and mayo but I need to make sure that the mayo doesn't make the burger bun really wet. Oh, and it needs to be warm, like, made less than 5 minutes ago warm but not so hot that I burn myself. I'm also not a big fan of plastic containers so if it could be in a paper bag that would be good. Actually, make that a brown paper bag, I like the colour of that"

```text
I would recommend breaking students up into their project groups to do this activity.

A burger shall be provided to the user
  * The burger shall contain lots of pickles
  * The burger shall contain lots of mayo
  * The mayo shall not make the bun wet
  * The burger shall be warm
  * The burger shall be wrapped in a brown paper bag
```

## C. Functional and Non-functional

* What is the difference between functional and non functional requirements? (See lecture slides)
* Are the following requirements functional or non functional?
  1. Every unsuccessful attempt by a user to access an item of data shall be recorded on an audit trail. 
  2. Privacy of information, the export of restricted technologies, intellectual property rights, etc. should be audited. 
  3. The software system should be integrated with banking API

> 1. Non-functional
> 2. Non-functional
> 3. Functional

## D. Verification & Validation

Given the Zune bug example from the lecture (in [day_to_year.py](day_to_year.py)) and a test that **doesn't** find the bug (in [day_to_year_test.py](day_to_year_test.py)), fix the implementation of `day_to_year()` such that it no longer has the bug.

To check whether you have in fact removed the bug and that your tests are adequate, use [Coverage.Py](https://coverage.readthedocs.io) to measure and inspect your code coverage. You may need to add more to the test to have satisfactory coverage. Make sure you're doing **branch** coverage checking!

Run your [day_to_year.py](day_to_year.py) through pylint. Consider what issues it highlights and discuss, as a class, the alternatives for resolving them.

* Fixing the code so the issue no longer exists.
* Adding a pragma to the line the issue occurs, so pylint stops reporting it.
* Suppressing all instances of such errors via a config file.

You may wish to consult the [Google python style guide](https://google.github.io/styleguide/pyguide.html)

*Ensure pylint is run on your code.*

> See [day_to_year.py](solutions/day_to_year.py) and [day_to_year_test.py](solutions/day_to_year_test.py).

## E. More Python Practice

Write a program [prettydate.py](prettydate.py) that converts 24 hour time into 12 hour time.
- You may assume that all inputs will be a valid 24 hour time.
- You program should read each line of input from standard input until EOF and output the result to standard output.

Sample input:
```python
1234
0525
0000
0001
1904
```

Sample output:
```python
12:34 PM
05:25 AM
00:00 AM
00:01 AM
07:04 PM
```

*Ensure pylint is run on your code.*

Make your code as pythonic as possible.

> See [prettydate.py](solutions/prettydate.py).
