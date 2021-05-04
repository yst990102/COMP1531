def isValid(isbn):
    # Get the sum of the first 9 digits multiplied by their position
    first_nine = isbn[:9]
    sum_of_first_nine = 0
    for index, value in enumerate(first_nine):
        sum_of_first_nine += int(value) * (index + 1)

    # Get the remainder when this is divided by 11
    remainder = sum_of_first_nine % 11

    # Calculate the validity
    if (remainder == 10):
        return isbn[9] == 'X'
    else:    
        return int(isbn[9]) == remainder

if __name__ == "__main__":
    # Get the ISBN
    isbn = input('What is the ISBN? ')
    # Show the result
    valid = 'valid' if isValid(isbn) else 'invalid'
    print(f'{isbn} is {valid}.')