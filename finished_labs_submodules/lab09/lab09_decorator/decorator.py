import sys

MESSAGE_LIST = []


def authorise(function):
    """
    You need a function here authorise which contains another function called wrapper.
    This function authenticates the token against CrocodileLikesStrawberries and if valid calls the function given as input,
    authorise then needs to return wrapper.
    """
    def wrapper(*args, **kwargs):
        if auth_token != "CrocodileLikesStrawberries":
            sys.exit(1)
        return function(*args, **kwargs)
    return wrapper


@authorise
def get_messages():
    return MESSAGE_LIST


@authorise
def add_messages(msg):
    global MESSAGE_LIST
    MESSAGE_LIST.append(msg)


if __name__ == '__main__':
    auth_token = ""
    if len(sys.argv) == 2:
        auth_token = sys.argv[1]

    add_messages("Hello")
    add_messages("How")
    add_messages("Are")
    add_messages("You?")
    print(get_messages())
