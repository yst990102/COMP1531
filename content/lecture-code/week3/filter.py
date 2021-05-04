from functools import reduce

if __name__ == '__main__':
    marks = [ 65, 72, 81, 40, 56 ]
    passing_marks = list(filter(lambda m: m >= 50, marks))
    # Calculate
    total = reduce(lambda a, b: a + b, passing_marks)
    average = total/len(passing_marks)
    print(average)