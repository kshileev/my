import unittest


def fib(n):
    """ T(n) = T(n-2) + T(n-1) , T(0) = 0,  T(1) = 1
    :param n: order of fibonachi series
    """
    if n <= 0:
        return 0
    if 1 <= n <= 2:
        return 1
    tn2 = 0
    tn1 = 1
    tn = 1
    for i in range(2, n+1):
        tn = tn1 + tn2
        tn2 = tn1
        tn1 = tn
    return tn


def fib_recursive(n):
    """ T(n) = T(n-2) + T(n-1) , T(0) = 0,  T(1) = 1
    :param n: order of series
    """
    if n <= 0:
        return 0
    if 1 <= n <= 2:
        return 1
    return fib_recursive(n-2) + fib_recursive(n-1)


def fib2(n):
    """ T(n) = T(n-2)^2 + T(n-1)
    :param n:
    """
    if n <= 0:
        return 0
    if 1 <= n <= 2:
        return 1
    tn2 = 0
    tn1 = 1
    tn = 1
    for i in range(2, n+1):
        tn = tn1 + tn2 * tn2
        tn2 = tn1
        tn1 = tn
    return tn


class TestFibonacci(unittest.TestCase):
    def setUp(self):
        super(TestFibonacci, self).setUp()
        self.values = [0, 1, 1, 2, 3, 5, 8, 13, 21]
        self.values2 = [0, 1, 1, 2, 3, 7, 16, 65, 321]

    def test_fib(self):
        for n in range(len(self.values)):
            self.assertEqual(self.values[n], fib(n))

    def test_fib_recursive(self):
        for n in range(len(self.values)):
            self.assertEqual(self.values[n], fib_recursive(n))

    def test_fib2(self):
        for n in range(len(self.values)):
            self.assertEqual(self.values2[n], fib2(n))
