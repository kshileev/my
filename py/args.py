#/usr/bin/env python3
from unittest import TestCase


def create_parser():
    import argparse

    def abs_dir_path(value):
        from os import path

        abs_path = path.abspath(path.expanduser(value))
        if not path.isdir(abs_path):
            raise argparse.ArgumentTypeError(value + ' is not found')
        return abs_path

    def ip(value):
        import ipaddress

        return ipaddress.ip_address(value)

    parser = argparse.ArgumentParser()
    subparsers =parser.add_subparsers(title='commands')
    parserMp = subparsers.add_parser(name='mp', help='run tests on the pod')
    parserMp.add_argument('--ip', required=True, type=ip, help='ip or name')
    parserMp.add_argument('--prefix', required=True, type=str, help='prefix to match tests')
    parserMp.add_argument('--debug', action='store_true', help='debug')

    parserCmd = subparsers.add_parser(name='cmd', help='manual operations on the pod')
    parserCmd.add_argument('--pod', type=str, choices=['a', 'b', 'c'], nargs='+', required=True, help='<REQUIRED> a list of strings')

    parserInfo = subparsers.add_parser(name='info', help='collect current pod status')
    parserInfo.add_argument('file_path', type=abs_dir_path, nargs='?', default='~', help='path to dir')  # positional with one or no args with custom type, dest not allowed

    return parser


class TestParser(TestCase):
    def setUp(self):
        super(TestParser, self).setUp()
        self.parser = create_parser()

    def test_help(self):
        self.assertEqual('aaa', self.parser.parse_args([]))

    def test_cmd1_with_ip(self):
        self.assertEqual('',self.parser.parse_args('mp --ip 10.11.12.13'.split()))


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    print(args)
