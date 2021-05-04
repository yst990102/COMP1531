import random


# def table():
if __name__ == "__main__":
    mul_1 = random.randint(2, 12)
    mul_2 = random.randint(2, 12)
    correct_answer = mul_1 * mul_2

    result = False
    while result == False:
        answer = int(input("What is %d x %d? " % (mul_1, mul_2)))
        if correct_answer == answer:
            result = True
            print("Correct!")
            break
        else:
            print("Incorrect - try again.")
