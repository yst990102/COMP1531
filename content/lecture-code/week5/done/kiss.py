"""Write a python function to generate a random number with up to 50
characters that consist of lowercase and uppercase characters"""

from random import choice
import string

def randoNumbo():
	'''
		
	'''
	return ''.join([choice(string.ascii_letters) for i in range(50)])

print(randoNumbo())
