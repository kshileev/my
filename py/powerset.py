import unittest


def p2(s):
    if not len(s):
        return [[]]
    new_elm = s[0]
    res = p2(s[1:])
    res += [x + [new_elm] for x in res]
    return res


def p1(s):
    lst = [[], s]

    for i, elem in enumerate(s):
        lst.append([elem])
        for j in lst[i+1:]:
            lst += [elem, j]
    return lst


class TestPowerset(unittest.TestCase):
    def setUp(self):
        super(TestPowerset, self).setUp()

    def test_empty(self):
        self.assertEqual([[]], p2([]))

    def test_single(self):
        self.assertEqual([[], [1]], p2([1]))

    def test_normal(self):
        self.assertSetEqual([[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]], p2([1, 2, 3]))
