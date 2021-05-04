import sys

def sqrt(x):
    if x < 0:
        raise Exception(f"Input {x} is less than 0. Cannot sqrt a number < 0")
    return x**0.5

if __name__ == '__main__':
    if len(sys.argv) == 2:
        try:
            print(sqrt(int(sys.argv[1])))
        except Exception as e:
            print(f"Got an error: {e}")
