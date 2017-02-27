import unittest
# https://www.hackerrank.com/challenges/encryption


def encrypt(text):
    import math

    text = text.replace(' ', '')
    sqrt_l = math.sqrt(len(text))
    floor, ceil = int(math.floor(sqrt_l)), int(math.ceil(sqrt_l))
    n_columns = ceil

    m = [text[r:r + n_columns] for r in range(0, len(text), n_columns)]
    m[-1] += '*' * (n_columns - len(m[-1]))

    by_columns = list()
    for c in range(n_columns):
        column = ''.join([r[c] for r in m])
        by_columns.append(column.replace('*', ''))

    return ' '.join(by_columns)


class TestEncryption(unittest.TestCase):
    def setUp(self):
        super(TestEncryption, self).setUp()

    def test_0(self):
        self.assertEqual(encrypt('if man was meant to stay on the ground god would have given us roots'), 'imtgdvs fearwer mayoogo anouuio ntnnlvt wttddes aohghn sseoau')

    def test_1(self):
        self.assertEqual(encrypt('have a nice day'), 'hae and via ecy')

    def test_2(self):
        self.assertEqual(encrypt('feed the dog'), 'fto ehg ee dd')

    def test_3(self):
        self.assertEqual(encrypt('chill out'), 'clu hlt io')
