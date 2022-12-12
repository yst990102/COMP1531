# COMP1531 Final Exam (Sample)

*Please note: This is a sample paper to indicate general structure of your final exam. The number of questions, and the weightings of those questions, may potentially vary on the final exam. The sample exam by nature has less questions in it than the final exam. If you want to practice the questions in this sample exam, you should aim to complete the questions provided within 1.5 hours as a rough guide.*

For this exam you are provided with this public repostory (`exam-spec-example`) that all students are provided that includes the questions being asked. You will then also have your own [personal exam repository](https://cgi.cse.unsw.edu.au/~cs1531/redirect/?path=COMP1531/21T1/students/_/exam-sample) where you actually answer and submit these questions to.

If you are seeking information not provided in this file, check the [COMP1531 Exam Brief page](https://webcms3.cse.unsw.edu.au/COMP1531/21T1/resources/56701). If your question is still unanswered, follow the "Communicating with teaching staff" instructions at said link.

## Change Log

* Coming Soon

## Part 1. Cloning your repository

Please clone your [personal exam repository](https://cgi.cse.unsw.edu.au/~cs1531/redirect/?path=COMP1531/21T1/students/_/exam-sample).

## Part 2. Questions - Short Answer (20%)

### Question 1 (3%)

In your personal exam repository, answer this question in `q1.txt`

Describe and justify three attributes of good requirements.

### Question 2 (2%)

In your personal exam repository, answer this question in `q2.txt`

Compare and contrast the differences between authentication and authorisation, providing an example for each.

### Question 3 (3%)

In your personal exam repository, answer this question in `q3.txt`

Break the following elicited requirements into a list of atomic dot points. Remove or consolidate any unnecessary or distracting information

*How could we clean this up into well described requirements? "I want a burger with lots of pickles and mayo but I need to make sure that the mayo doesn't make the burger bun really wet. Oh, and it needs t obe warm, like, made less than 5 minutes ago warm but not so hot that I burn myself. I'm also not a big fan of plastic containers so if it could be in a paper bag that would be good. Actually, make that a brown paper bag, I like the colour of that"*

### Question 4 (2%)

In your personal exam repository, answer this question in `q4.txt`

Compare and contrast the difference between `cohesion` and `coupling` when it comes to analysing two modules of a piece of a software.

### Question 5 (3%)

**etc**. This is simply here to give you a sense of the number of questions you might be asked in the exam, although we are not providing an example.

### Question 6 (3%)

**etc**. This is simply here to give you a sense of the number of questions you might be asked in the exam, although we are not providing an example.

### Question 7 (4%)

**etc**. This is simply here to give you a sense of the number of questions you might be asked in the exam, although we are not providing an example.

## Part 3. Questions - Programming Questions (80%)

### Question 8 (8%)

In your personal exam repository, answer this question in `q8.py`

Complete the function `reverse_words()`, where given a list of strings, the function return a new list where the order of the words is reversed.

Write tests for this function using pytest, and include them in `q8_test.py`.

You will receive 50% of your marks from the correctness of your implementation, 25% from the ability of your tests to identify correct and incorrect implementations, and 25% of your marks from your branch coverage.

You can determine your branch coverage by running `coverage run -m pytest q8_test.py` 

### Question 9 (12%)

In your personal exam repository, answer this question in `q9.py`

Complete the function `timetable(dates, times)` where given a list of dates and list of times, generates and returns a list of datetimes. All possible combinations of date and time are contained within the result. The result is sorted in chronological order.

Write tests for this function using pytest, and include them in `q9_test.py`.

You will receive 50% of your marks from the correctness of your implementation, 25% from the ability of your tests to identify correct and incorrect implementations, and 25% of your marks from your branch coverage.

You can determine your branch coverage by running `coverage run -m pytest q9_test.py` 

### Question 10 (12%)

In your personal exam repository, answer this question in `q10.py`

Complete the function `factors(num)` that factorises a number into its prime factors. The primes should be listed in ascending order.

Write tests for this function using pytest, and include them in `q10_test.py`.

You will receive 50% of your marks from the correctness of your implementation, 25% from the ability of your tests to identify correct and incorrect implementations, and 25% of your marks from your branch coverage.

You can determine your branch coverage by running `coverage run -m pytest q10_test.py` 

### Question 11 (10%)

In your personal exam repository, answer this question in `q11.py`

Complete the function `roman(numerals)`. Given a string, this function returns their value as an integer. You may assume the Roman numerals are in the "standard" form, i.e. any digits involving 4 and 9 will always appear in the subtractive form.

Write tests for this function using pytest, and include them in `q11_test.py`.

You will receive 50% of your marks from the correctness of your implementation, 25% from the ability of your tests to identify correct and incorrect implementations, and 25% of your marks from your branch coverage.

You can determine your branch coverage by running `coverage run -m pytest q11_test.py` 

### Question 12 (15%)

**etc**. This is simply here to give you a sense of the number of questions you might be asked in the exam, although we are not providing an example.

### Question 13 (13%)

**etc**. This is simply here to give you a sense of the number of questions you might be asked in the exam, although we are not providing an example.

### Question 14 (10%)

**etc**. This is simply here to give you a sense of the number of questions you might be asked in the exam, although we are not providing an example.

## Submission

At the end of your specified exam time, we will automatically collect the code on your `master` branch's HEAD (i.e. latest commit). 

Please note: If you develop locally ensure you check that your code works on the CSE servers. Failure to do so could result in a fail mark in the exam.

## Originality of Work

The work you submit must be your own work. Submission of work partially or completely derived from any other person or jointly written with any other person is not permitted.

The penalties for such an offence may include negative marks, automatic failure of the course and possibly other academic discipline. Assignment submissions will be examined both automatically and manually for such submissions.

Relevant scholarship authorities will be informed if students holding scholarships are involved in an incident of plagiarism or other misconduct.

Do not provide or show your assignment work to any other person — apart from the teaching staff of COMP1531.

If you knowingly provide or show your assignment work to another person for any reason, and work derived from it is submitted, you may be penalized, even if the work was submitted without your knowledge or consent.  This may apply even if your work is submitted by a third party unknown to you.

Note you will not be penalized if your work has the potential to be taken without your consent or
knowledge.