class TreeNode:
    def __init__(self, uid, parent, children):
        self.uid = uid
        self.parent = parent
        self.children = children

    def to_list(self):

        if values:
            values.append(self.uid)
        else:
            l_values = [self.value]
        for child in self.children:
            child.traverse(l_values)
        return l_values

    def list_of_parents(self):
        """Traverse the tree to the root and build a list of nodes seen"""
        if not self.parent:
            return [self] + self.parent.list_of_parents()
        else:
            return None

    @staticmethod
    def least_common_parents(node1, node2):
        if node1 == node2:
            return node1
        l1 = node1.list_of_parents()  #log(N)
        l2 = node2.list_of_parents()

        min_len = min(len(l1), len(l2))

        i = 0
        for i in range(min_len):
            while not l1[-i] == l2[-i]:
                continue
        return l1[i+1]

    @staticmethod
    def build_binary_from_list(lst, start=None, end=None):
        start = start or 0
        end = end or len(values)

        root = TreeNode(values[start])
        left_start = start + 1
        right_start = left_start
        while right_start < end and values[right_start] < root.value:
            right_start += 1

        if left_start < right_start:
            root.left = TreeNode.build_binary_from_list(values, left_start, right_start)
        if right_start < end:
            root.right = TreeNode.build_binary_from_list(values, right_start, end)
        return root


class Tree:
    (ROOT, DEPTH, BREADTH) = range(3)

    def __init__(self):
        self.__nodes = {}

    def print(self, identifier, depth=ROOT):
        children = self[identifier].children
        if depth == _ROOT:
            print('{0}'.format(identifier))
        else:
            print("\t"*depth, "{0}".format(identifier))

        depth += 1
        for child in children:
            self.print(child, depth)  # recursive call

    def __getitem__(self, item):
        return self.__nodes[item]

    def __setitem__(self, key, value):
        self.__nodes[key] = value

if __name__ == '__main__':
    """    a
          / \
         b   c
             / \
            d   f
             \
              e
    """
    tree = TreeNode.build_binary_from_list(['a', 'b', 'c', 'd', 15, 12, 17, 19])
    values = tree.traverse()
    print(values)