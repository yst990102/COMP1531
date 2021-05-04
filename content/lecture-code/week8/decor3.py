def foo(*args, **kwargs):
    print(args) # A list
    print(kwargs) # A dictionary

if __name__ == '__main__':
    foo('this', 'is', truly='dynamic')