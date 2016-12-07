from unittest import TestCase


def f1(x):
    if x == 0:
        return 0

    return f1(int(x / 10)) + x % 10


class TestRecursion(TestCase):
    def setUp(self):
        super(TestRecursion, self).setUp()

    def test_f1(self):
        self.assertAlmostEqual(2, f1(2000))
