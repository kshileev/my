class Foo(object):

    def __init__(self):
        self._actual_ports = []

    @property
    def actual_ports(self):
        if not self._actual_ports:
            self._actual_ports = [1, 2, 3]
        return self._actual_ports

if __name__ == '__main__':
    f = Foo()
    print('{}'.format(f.actual_ports))

