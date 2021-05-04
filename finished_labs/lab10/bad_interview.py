def bad_interview():
    '''
    A generator that yields all numbers from 1 onward, but with some exceptions:
    * For numbers divisible by 3 it instead yields "Fizz"
    * For numbers divisible by 5 it instead yields "Buzz"
    * For numbers divisible by both 3 and 5 it instead yields "FizzBuzz"
    '''
    count = 0
    while True:
        count += 1
        if count % 3 == 0 and count % 5 != 0:
            yield "Fizz"
        elif count % 3 != 0 and count % 5 == 0:
            yield "Buzz"
        elif count % 3 == 0 and count % 5 == 0:
            yield "FizzBuzz"
        else:
            yield count
