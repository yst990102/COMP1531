def make_uppercase(function):
	def wrapper(*args, **kwargs):
		return function(*args, **kwargs).upper()
	return wrapper

@make_uppercase
def get_first_name():
	return "Hayden"

@make_uppercase
def get_last_name():
	return "Smith"

if __name__ == '__main__':
    print(get_first_name())
    print(get_last_name())