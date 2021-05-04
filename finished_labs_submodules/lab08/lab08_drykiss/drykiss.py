import math


def drykiss(my_list):
    # my_min = 999999
    # for i in range(0, 5):
    #     if my_list[i] < my_min:
    #         my_min = my_list[i]
    my_min = min(my_list)           # replace previous code, min() is an inner function, so we don't need to loop anymore

    product = 1
    for i in range(0, 4):
        product = product * my_list[i]
    result = product

    product = 1
    for i in range(1, 5):
        product = product * my_list[i]
    result = (my_min, result, product)
    return result


if __name__ == '__main__':
    a = input("Enter a: ")
    a = int(a)
    b = input("Enter b: ")
    b = int(b)
    c = input("Enter c: ")
    c = int(c)
    d = input("Enter d: ")
    d = int(d)
    e = input("Enter e: ")
    e = int(e)
    my_list = [a, b, c, d, e]
    result = drykiss(my_list)
    print("Minimum: " + str(result[0]))
    print("Product of first 4 numbers: ")
    print(f"  {result[1]}")
    print("Product of last 4 numbers")
    print(f"  {result[2]}")
