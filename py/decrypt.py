from unittest import TestCase


class Decipher:

    ENGLISH_WORLDS = ['This', 'is', 'a', 'sample', 'first', 'second']

    @staticmethod
    def caesar_cipher(message, encryption_key):
        """ Implements Caesar cipher algorithm: all letters a substituted by letter which is shifted by encrypted_key mod 23. Symbols like space and - are not shifted
        :param message: input plain test message
        :param encryption_key: int
        :return: encrypted message
        """
        n_letters = 26
        a = []
        for l in message:
            base = ord('a') if l.islower() else ord('A')
            a.append(chr(base + (ord(l) + encryption_key - base) % n_letters) if l.isalpha() else l)
        return ''.join(a)

    @staticmethod
    def random_cipher(message):
        """ Remove all spaces then shift all letters in message into a random positions
            :param message: initial message
            :returns: scrambled message
        """
        import random

        message = message.replace(' ', '')
        scrambled_message = list(message)
        n = len(message)
        for i in range(n):
            k = random.randint(i + 1, n)
            scrambled_message[i] = scrambled_message[k]
        return scrambled_message

    @staticmethod
    def words_in_message(message):
        found_words = [word for word in Decipher.ENGLISH_WORLDS if word in message]  # O(len(words))
        return sum(map(lambda word: len(word), found_words)), found_words

    @staticmethod
    def random_decipher(message):
        """
            :param message: scrambled english text where spaces are removed and all letters are moved to random positions e.g. This is a sample -> histsiaampels
            :returns: a list of all valid English words e.g. [This, is,sample, a, additional]
    # n_letters = len(message)
    # how_many_samples = 10
    # while True:
    # 	#list_of_lists_of_words = map(lambda x: words_in_string(x), [random_move(string) for y in xrange(some_number)])
    #
    # 	for s, words in list_of_lists_of_words:
    # 		if s == len(message):
    #           return ''.join(list_of_words)

        """
        return message


class TestDecipher(TestCase):
    def setUp(self):
        super(TestDecipher, self).setUp()

    def t1est_random_decipher(self):
        encrypted = Decipher.random_cipher(message='This is a sample')
        self.assertEqual(['This', 'is', 'a', 'sample'], Decipher.random_decipher(message=encrypted))

    def test_caesar_cipher(self):
        self.assertEqual('A', Decipher.caesar_cipher(message='A', encryption_key=0))

        self.assertEqual('z', Decipher.caesar_cipher(message='a', encryption_key=25))
        self.assertEqual('z', Decipher.caesar_cipher(message='a', encryption_key=51))

        self.assertEqual('a', Decipher.caesar_cipher(message='a', encryption_key=26))
        self.assertEqual('b', Decipher.caesar_cipher(message='a', encryption_key=27))
        self.assertEqual('c', Decipher.caesar_cipher(message='a', encryption_key=28))
        self.assertEqual('okffng-Qwvb', Decipher.caesar_cipher(message='middle-Outz', encryption_key=2))
