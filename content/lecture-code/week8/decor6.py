def run_twice(function):
	def wrapper(*args, **kwargs):
		return function(*args, **kwargs) \
		     + function(*args, **kwargs)
	return wrapper

@run_twice
def get_first_name():
	return "Hayden"

@run_twice
def get_last_name():
	return "Smith"

if __name__ == '__main__':
    print(get_first_name())
    print(get_last_name())