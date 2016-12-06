import unittest


def reverse(a):
    """
    :param a: 1d array [1, 2, 3, ...]
    :return: 1d array which is reverse of a: [..., 3, 2, 1]
    """
    return a[::-1]


def reverse1(a):
    """
    :param a: 1d array [1, 2, 3, ...]
    :return: 1d array which is reverse of a: [..., 3, 2, 1]
    """

    r = []
    for i in range(len(a)-1, -1, -1):
        r.append(a[i])  # O(n)
    return r


def hour_glass(a):
    """ -9 <= A[i],[j] <= 9; i,j = 0..5
    a = [[1, 1, 1, 0, 0, 0],
         [0, 1, 0, 0, 0, 0],
         [1, 1, 1, 0, 0, 0],
         [0, 0, 2, 4, 4, 0],
         [0, 0, 0, 2, 0, 0],
         [0, 0, 1, 2, 4, 0]
        ]
        goes to 1 1 1 and all other possible
                  1
                1 1 1
        then sum up all elements
    :return: max sum
    """
    def sum_glass_from_left_up_cornet(x, y):
        s = 0
        s += a[x][y]; s += a[x][y + 1]; s += a[x][y + 2]
        s += a[x+1][y + 1]
        s += a[x+2][y]; s += a[x + 2][y + 1]; s += a[x + 2][y + 2]
        return s

    max_sum = -70  # min possible sum is 7 * -9
    for i in range(0, 4):
        for j in range(0, 4):
            new_sum = sum_glass_from_left_up_cornet(i, j)
            if new_sum > max_sum:
                max_sum = new_sum
    return max_sum


class TestArrayAlgorithms(unittest.TestCase):
    def setUp(self):
        super(TestArrayAlgorithms, self).setUp()

    def test_reverse(self):
        self.assertEqual([4, 3, 2, 1], reverse([1, 2, 3, 4]))

    def test_reverse1(self):
        self.assertEqual([4, 3, 2, 1], reverse1([1, 2, 3, 4]))

    def test_hour_glass(self):
        a = [[1, 1, 1, 0, 0, 0],
             [0, 1, 0, 0, 0, 0],
             [1, 1, 1, 0, 0, 0],
             [0, 0, 2, 4, 4, 0],
             [0, 0, 0, 2, 0, 0],
             [0, 0, 1, 2, 4, 0]
             ]
        self.assertEqual(19, hour_glass(a))
