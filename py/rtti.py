import inspect


def my_func():
    print inspect.currentframe().f_code.co_name
    print inspect.stack()[0][3]


class MyClass(object):
    def get_method_name(self):
        print inspect.currentframe().f_code.co_name
        print inspect.stack()[0][3]


if __name__ == '__main__':
    my_func()
    m = MyClass()
    m.get_method_name()
