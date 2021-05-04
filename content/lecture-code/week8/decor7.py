class Message:
	def __init__(self, id, text):
		self.id = id
		self.text = text

messages = [
	Message(1, "Hello"),
	Message(2, "How are you?"),
]

def get_message_by_id(id):
	return [m for m in messages if m.id == id][0]

def message_id_to_obj(function):
	def wrapper(*args, **kwargs):
		argsList = list(args)
		argsList[0] = get_message_by_id(argsList[0])
		args = tuple(argsList)
		return function(*args, **kwargs)
	return wrapper

@message_id_to_obj
def printMessage(message):
	print(message.text)

if __name__ == '__main__':
	printMessage(1)
