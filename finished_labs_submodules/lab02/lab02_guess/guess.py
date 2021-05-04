print("Pick a number between 1 and 100 (inclusive)")

lower_range = 1
upper_range = 100
while True:
    my_guess = (lower_range + upper_range) / 2
    print("My guess is: %d" % my_guess)
    result = input("Is my guess too low (L), too high (H), or correct (C)?\n")

    if result == 'L':
        lower_range = my_guess
    elif result == 'H':
        upper_range = my_guess
    elif result == 'C':
        print("Got it!")
        break
    else:
        print("what the fuck you have entered?")