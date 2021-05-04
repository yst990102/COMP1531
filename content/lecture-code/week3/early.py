class SqrtException(Exception):
    pass

def sqrt(num):
    if num < 0:
        raise SqrtException("Number cannot be < 0")
    return num ** 0.5

try:
    print(sqrt(int(input())))
except SqrtException as e:
    print(e)