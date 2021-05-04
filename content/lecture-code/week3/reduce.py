from functools import reduce

if __name__ == '__main__':
    marks = [ 65, 72, 81, 40, 56 ]
    total = reduce(lambda a, b: (a + b if a >= 50 else b), marks)
    average = total/len(marks)
    print(average)