import unittest


class TreeNode:
    def __init__(self, uid):
        self.uid = uid
        self.parent = None
        self.children = []

    def __repr__(self):
        return str(self.uid)

    def add_children(self, children):
        self.children = children
        for child in children:
            child.parent = self

    def dfs(self, uid, order):
        order.append(self.uid)
        if self.uid == uid:
            return self
        for child in self.children:
            node = child.dfs(uid, order)
            if node:
                return node
        return None

    def bfs(self, uid, order):
        if self.uid == uid:
            order.append(self.uid)
            return self
        for child in self.children:
            order.append(child.uid)
            if child.uid == uid:
                return child
        for child in self.children:
            node = child.bfs(uid, order)
            if node:
                return node
        return None

    def list_of_parents(self):
        """Traverse the tree to the root and build a list of nodes seen"""
        if not self.parent:
            return [self] + self.parent.list_of_parents()
        else:
            return None

    @staticmethod
    def least_common_parent(node1, node2):
        if node1 == node2:
            return node1
        l1 = node1.list_of_parents()  # log(N)
        l2 = node2.list_of_parents()

        min_len = min(len(l1), len(l2))

        i = 0
        for i in range(min_len):
            while not l1[-i] == l2[-i]:
                continue
        return l1[i+1]


class TestTree(unittest.TestCase):
    def setUp(self):
        """       0
              /       \
             1        2
            /\        /\
           3 4      5  6
             /\   /   /  \
            7 8  9   10  11
                     \
                     12
        """
        super(TestTree, self).setUp()
        self.nodes = map(lambda i: TreeNode(i), range(13))

        self.nodes[0].add_children([self.nodes[1], self.nodes[2]])
        self.nodes[1].add_children([self.nodes[3], self.nodes[4]])
        self.nodes[2].add_children([self.nodes[5], self.nodes[6]])
        self.nodes[4].add_children([self.nodes[7], self.nodes[8]])
        self.nodes[5].add_children([self.nodes[9]])
        self.nodes[6].add_children([self.nodes[10], self.nodes[11]])
        self.nodes[10].add_children([self.nodes[12]])

    def test_dfs(self):
        order = []
        self.assertEqual(None, self.nodes[0].dfs(13, order))
        self.assertEqual([0, 1, 3, 4, 7, 8, 2, 5, 9, 6, 10, 12, 11], order)

    def test_bfs(self):
        order = []
        self.assertEqual(None, self.nodes[0].bfs('f', order))
        self.assertEqual(range(13), order)
