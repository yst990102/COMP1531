def check_password(password):
    """
    Takes in a password, and returns a string based on the strength of that password.

    The returned value should be:
    * "Strong password", if at least 12 characters, contains at least one number, at least one uppercase letter, at least one lowercase letter.
    * "Moderate password", if at least 8 characters, contains at least one number.
    * "Poor password", for anything else
    * "Horrible password", if the user enters "password", "iloveyou", or "123456"
    """

    num = 0
    upper_char = 0
    lower_char = 0

    for i in password:
        if i.islower() == True:
            lower_char += 1

        if i.isupper() == True:
            upper_char += 1

        if i.isdigit() == True:
            num += 1

    # print("len == %d, upper_char == %d, lower_char == %d, num == %d\n", len(password), upper_char, lower_char, num)

    if len(password) >= 12 and num >= 1 and upper_char >= 1 and lower_char >= 1:
        return "Strong password"
    elif len(password) >= 8 and num >= 1:
        return "Moderate password"
    elif password in ["password", "iloveyou", "123456"]:
        return "Horrible password"
    else:
        return "Poor password"


if __name__ == "__main__":
    print(check_password("ihearttrimesters"))
    # What does this do?
