import sys

def sqrt(x):
    if x < 0:
        raise Exception(f"Error, sqrt input {x} < 0")
    return x**0.5

if __name__ == '__main__':
    print("Please enter a number: ",)
    while True:
        try:
            inputNum = int(sys.stdin.readline())
            print(sqrt(inputNum))
            break
        except Exception as e:
            print(f"Error when inputting! {e}. Please try again:")
