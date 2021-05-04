from functools import reduce

if __name__ == '__main__':
    marks = [ 39, 43.2, 48.6, 24, 33.6 ] # Marks out of 60
    normalised_marks = map(lambda m: 100*m/60, marks)
    passing_marks = list(filter(
        lambda m: m >= 50, normalised_marks))
    total = reduce(lambda a, b: a + b, passing_marks)
    average = total/len(passing_marks)
    print(average)

def greater_than_0(n):
    return n > 0

filter(lambda n: n > 0, [-1,2,4,-8])