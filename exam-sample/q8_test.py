from q8 import reverse_words

def test_two_multiple():
	assert reverse_words(["Hello World", "I am here"]) == ['World Hello', 'here am I']
