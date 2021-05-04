# This is written out in the order the programmer would write it


def register(username, password, repeatPassword):
    if not usernameUsed(username):
        if validPassword(password):
            if matches(password, repeatPassword):
                return createNewUser(username, password)
    return None


def usernameUsed(username):
    return True  # Lookup database for existing user


def validPassword(password):
    return len(password) >= 10


def matches(password, repeatPassword):
    return password == repeatPassword  # Example of over-abstraction


def createNewUser(username, password):
    return 1  # Create new user in the database
