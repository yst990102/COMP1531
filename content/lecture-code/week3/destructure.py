import math

def convert(x, y):
    return (math.sqrt(x**2 + y**2), math.degrees(math.atan(y/x)))

if __name__ == '__main__':
    print("Enter x coord: ", end='')
    x = int(input())
    print("Enter y coord: ", end='')
    y = int(input())

    mag, dir = convert(x, y)
    print(mag, dir)

    mag2, _ = convert(x, y)
    print(mag2)
