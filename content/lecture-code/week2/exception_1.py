import sys

def sqrt(x):
    if x < 0:
        sys.stderr.write("Error Input < 0\n")
        sys.exit(1)
    return x**0.5

if __name__ == '__main__':
    print("Please enter a number: ",)
    inputNum = int(sys.stdin.readline())
    print(sqrt(inputNum))
