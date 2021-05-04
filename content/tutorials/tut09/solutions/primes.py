# Define a recursive function
def factors(number_to_factorise):
    if number_to_factorise == 1:
        return []
    else:
        factor_to_try = 2
        while True:
            if number_to_factorise % factor_to_try == 0:
                residual = number_to_factorise / factor_to_try
                return [factor_to_try] + factors(residual)                
            else:
                factor_to_try += 1

# Ask the user for a number
number = input('Enter a number: ')

# Convert it to an integer
number = int(number)

# Use the function to show the factorisation
print(f"{number} = {' x '.join(str(n) for n in factors(number))}")