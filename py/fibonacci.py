import unittest
import decorators

@decorators.print_time
def fib(n):
    """ T(n) = T(n-2) + T(n-1) , T(0) = 0,  T(1) = 1 """
    if n <= 0:
        return 0
    if 1 <= n <= 2:
        return 1
    tn2 = 0
    tn1 = 1
    tn = tn1 + tn2
    for i in xrange(2, n+1):
        tn = tn1 + tn2
        tn2 = tn1
        tn1 = tn
    return tn


def fib_req(n):
    """ T(n) = T(n-2) + T(n-1) , T(0) = 0,  T(1) = 1 """
    if n <= 0:
        return 0
    if 1 <= n <= 2:
        return 1
    return fib_req(n-2) + fib_req(n-1)


def fibonacci2(a, b, n):
    """ T(n) = T(n-2)^2 + T(n-1) """
    pass


class TestFibonacci(unittest.TestCase):
    def setUp(self):
        super(TestFibonacci, self).setUp()
        self.values = [0, 1, 1, 2, 3, 5, 8, 13, 21]

    def test_fib(self):
        for n in xrange(len(self.values)):
            self.assertEqual(self.values[n], fib(n))

    def test_fib_req(self):
        for n in xrange(len(self.values)):
            self.assertEqual(self.values[n], fib_req(n))
