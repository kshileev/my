
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def traverse(self, l_values=None):
        if l_values:
            l_values.append(self.value)
        else:
            l_values = [self.value]
        if self.left:
            self.left.traverse(l_values)
        if self.right:
            self.right.traverse(l_values)
        return l_values

    @staticmethod
    def _reconstruct(l_values, start, end):
        root = Node(l_values[start])
        left_start = start + 1
        right_start = left_start
        while right_start < end and l_values[right_start] < root.value:
            right_start += 1

        if left_start < right_start:
            root.left = Node._reconstruct(l_values, left_start, right_start)
        if right_start < end:
            root.right = Node._reconstruct(l_values, right_start, end)
        return root

    @staticmethod
    def reconstruct(l_values):
        return Node._reconstruct(l_values, 0, len(l_values))

if __name__ == '__main__':
    tree = Node.reconstruct([10, 5, 3, 7, 15, 12, 17, 19])
    values = tree.traverse()
    print values