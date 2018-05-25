from unittest import TestCase


class Decipher:

    def __init__(self):
        pass

    ENGLISH_WORLDS = ['This', 'is', 'a', 'sample', 'first', 'second']

    @staticmethod
    def caesar_cipher(message, secret_shift, is_decipher=False):
        """ Implements Caesar cipher algorithm: all letters are shifted by secret_shift mod 26
        :param message: string
        :param secret_shift: int
        :param is_decipher: bool, if true, decipher the message
        :return: string
        """

        mult = -1 if is_decipher else 1
        result = [chr((ord(l) + mult * (secret_shift % 26))) for l in message]
        return ''.join(result)

    @staticmethod
    def viginere_cipher(message, secret_word, is_decipher=False):
        """ Implements Vigenere cipher algorithm:
        1. augment secret_word by itself until it becomes equal in length to the message
        2. for each symbol in message, start Ceaser cipher using the position of corresponding letter of secret word
        :param message: string
        :param secret_word: string
        :param is_decipher: bool, decipher if True
        :return: string
        """

        result = []
        for i, symbol in enumerate(message):
            result.append(Decipher.caesar_cipher(message=symbol, secret_shift=ord(secret_word[i % len(secret_word)]), is_decipher=is_decipher))
        return ''.join(result)

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


def main():
    import argparse
    from os import path
    import re
    import logging
    import getpass

    logger = logging.getLogger('cipher')
    logger.setLevel(logging.INFO)

    def abs_file_path(value):
        abs_path = path.abspath(path.expanduser(value))
        if not path.isdir(abs_path):
            raise argparse.ArgumentTypeError(value + ' is not found')
        return abs_path

    parser = argparse.ArgumentParser(prog='cipher')
    parser.add_argument('dir_path', type=abs_file_path, nargs='?', help='path to dir with info file')
    args = parser.parse_args()
    secret = getpass.getpass()

    ints = re.findall('\(.{1,2}(\d{1,3})\)', secret)
    if len(ints) != 1:
        raise ValueError('Secret is not of you know what type!')

    file_path = path.join(args.dir_path, 'info' + ints[0])
    encripted_file_path = path.expanduser('~/Google Drive/info{}'.format(ints))

    with open(file_path) as f:
        text = f.read()

    if file_path == encripted_file_path:
        text += 'ciphered with secret: ' + secret + ' from ' + file_path
        with open(encripted_file_path, 'w') as f:
            f.write(Decipher.viginere_cipher(message=text, secret_word=secret))
        logger.info(encripted_file_path + ' created')
    else:
        decoded = Decipher.viginere_cipher(message=text, secret_word=args.secret, is_decipher=True)
        logger.info(decoded + '\ntaken from ' + file_path)


class TestDecipher(TestCase):
    def setUp(self):
        super(TestDecipher, self).setUp()
        self.plain_text = 'Some plain text\n with new line'

    def t1est_random_decipher(self):
        encrypted = Decipher.random_cipher(message='This is a sample')
        self.assertEqual(['This', 'is', 'a', 'sample'], Decipher.random_decipher(message=encrypted))

    def test_caesar_cipher(self):
        self.assertEqual('*', Decipher.caesar_cipher(message=' ', secret_shift=10))

        self.assertEqual('A', Decipher.caesar_cipher(message='A', secret_shift=0))

        self.assertEqual('z', Decipher.caesar_cipher(message='a', secret_shift=25))
        self.assertEqual('z', Decipher.caesar_cipher(message='a', secret_shift=51))

        self.assertEqual('a', Decipher.caesar_cipher(message='a', secret_shift=26))
        self.assertEqual('b', Decipher.caesar_cipher(message='a', secret_shift=27))
        self.assertEqual('c', Decipher.caesar_cipher(message='a', secret_shift=28))

        for i in range(30):
            ciphered = Decipher.caesar_cipher(message=self.plain_text, secret_shift=i)
            decipered = Decipher.caesar_cipher(message=ciphered, secret_shift=i, is_decipher=True)
            self.assertEqual(self.plain_text, decipered)

    def test_viginere_cipher(self):
        ciphered = Decipher.viginere_cipher(message=self.plain_text, secret_word='LEMON')
        deciphered = Decipher.viginere_cipher(message=ciphered, secret_word='LEMON', is_decipher=True)
        self.assertEqual(self.plain_text, deciphered)


if __name__ == '__main__':
    main()
