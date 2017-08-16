from unittest import TestCase
from cipher import Decipher

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
