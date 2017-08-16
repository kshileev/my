

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

    def abs_file_path(value):
        abs_path = path.abspath(path.expanduser(value))
        if not path.isdir(abs_path):
            raise argparse.ArgumentTypeError(value + ' is not found')
        return abs_path

    parser = argparse.ArgumentParser(prog='cipher')
    parser.add_argument('-s', required=True, type=str, dest='secret', help='secret word')
    parser.add_argument('dir_path', type=abs_file_path, nargs='?', default='~/Google Drive', help='path to dir with info file')
    args = parser.parse_args()

    ints = re.findall('\(.{1,2}(\d{1,3})\)', args.secret)
    if len(ints) != 1:
        raise ValueError(args.secret + ' is not of you know what type!')

    abs_file_path = path.join(args.dir_path, 'info' + ints[0])
    with open(abs_file_path) as f:
        text = f.read()

    if text.startswith('INFO:'):
        text += 'ciphered with secret: ' + args.secret + ' from ' + abs_file_path
        with open(abs_file_path, 'w') as f:
            f.write(Decipher.viginere_cipher(message=text, secret_word=args.secret))
        print abs_file_path, 'with secret', args.secret, 'created'
    else:
        print Decipher.viginere_cipher(message=text, secret_word=args.secret, is_decipher=True)
        print 'taken from', abs_file_path


if __name__ == '__main__':
    main()