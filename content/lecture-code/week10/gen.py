"""def simple_generator():
    print("Hello")
    yield 1
    print("Nice to meet you")
    yield 2
    print("I am a generator")

for s in simple_generator():
    print(s)"""

"""def get_nums(count):
    return [8] * count

for num in get_nums(1000000):
    print(num, end='')"""

def squares(max_base):
    i = 0
    while i < max_base:
        i += 1
        yield i*i

for s in squares(10000):
    print(s)

for i in range(10000):
    print(i)