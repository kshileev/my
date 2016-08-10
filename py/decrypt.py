import unittest
"""This is a sample -> histsiaampels
[This, is,sample, a, additional]
"""

WORLDS = ['This', 'is', 'a', 'sample', 'first', 'second']

def scramble(message):
	"""shift all letters in message into a random position
	:param message: initial message
	"""
	import random

	scrambled_message = list(message)
	message_len = len(message)
	for i, letter in enumerate(message):
		k = random.randint(0, len(message))
		message[k] = letter
	return scrambled_message

def words_in_message(message, words)
	found_words = [word for word in words if word in message] # O(len(words))
	return  sum(map(lambda word: len(word), found_words)), found_words

def unscramble(message, words):
	"""Get a list of english word
	:param message: scrambled english text where spaces are removed and all letters are moved to different position
	:param words: list of all English words

	"""
	n_letters = len(message)
	how_many_samples = 10
	while True:
		list_of_lists_of_words = map(lambda x: words_in_string(x), [random_move(string) for y in xrange(some_number)])

		for s, words in list_of_lists_of_words:
			if s = len(string):
		return ‘ ’.join(list_of_words)

class TestDecrypt(unittest.TestCase):
	def setUp(self):
		super(TestDecrypt, self).setUp()

	def test_normal(self):
		worlds = ['This', 'is', 'a', 'sample']
		self.assertEqual(self.values[n], fib(n))
