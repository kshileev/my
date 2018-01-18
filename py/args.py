from unittest import TestCase


def main(args):
    import argparse

    def abs_dir_path(value):
        from os import path

        abs_path = path.abspath(path.expanduser(value))
        if not path.isdir(abs_path):
            raise argparse.ArgumentTypeError(value + ' is not found')
        return abs_path

    def ip(value):
        import ipaddress

        return ipaddress.ip_address(unicode(value))

    parser = argparse.ArgumentParser(prog='example')
    parser.add_argument('--foo', required=False, help='foo help')
    parser.add_argument('--all', action='store_true', help='all help')
    parser.add_argument('--ip', required=True, type=ip, help='ip address')
    parser.add_argument('--str', type=str, choices=['a', 'b', 'c'], nargs='+', required=True, help='<REQUIRED> a list of strings')
    parser.add_argument('file_path', type=abs_dir_path, nargs='?', default='~', help='path to dir')  # positional with one or no args with custom type, dest not allowed

    values = parser.parse_args(args)
    return values.foo, values.all, values.str


class TestParser(TestCase):
    def setUp(self):
        super(TestParser, self).setUp()

    def test_parser(self):
        self.assertEqual((None, False, ['a', 'b', 'c']), main(args='--str a b c'.split()))
