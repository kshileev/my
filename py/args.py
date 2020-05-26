#!/usr/bin/env python3
import argparse
from unittest import TestCase


def ip(value):
    import ipaddress

    try:
        return ipaddress.ip_address(value)
    except ValueError as ex:
        raise argparse.ArgumentTypeError(ex)


def abs_dir_path(value):
    from os import path

    abs_path = path.abspath(path.expanduser(value))
    if not path.isdir(abs_path):
        raise argparse.ArgumentTypeError(value + ' is not found')
    return abs_path


class CustomAction(argparse.Action):
    def __call__(self, parser, args, path, option_string=None):
        print (parser, args, path, option_string)


def parser_file():
    p = argparse.ArgumentParser(prog='./args.py', description='test parser to learn how to create arguments')
    p.add_argument('file', type=argparse.FileType('r'), help='path to some file')  # single positional
    p.add_argument('dir_path', type=abs_dir_path, nargs='?', default='~', help='path to dir')  # optional single positional (? means 0 or 1), custom type, dest not allowed
    p.add_argument('--debug', action='store_true', help='is debug?')
    p.add_argument('--ip', type=ip, help='ip address')
    p.add_argument('--pod', type=str, choices=['a', 'b', 'c'], nargs='+', required=False, help='list of strings')
    return p


def parser_yes_no():
    ok = ['Y', 'YES', 'Yes', 'True', 'true']

    def yes(value):
        return value in ok

    p = argparse.ArgumentParser(prog='./args.py', description='test parser for yes-no string as bool')
    p.add_argument('--is_tls', type=yes, default=False, help=f'set to true if one of {ok}')
    return p


def parser_int():
    p = argparse.ArgumentParser(prog='./args.py', description='test parser for int')
    p.add_argument('--n1', type=int, default=1, help=f'n1 int value')
    p.add_argument('--n2', type=int, default=1, help=f'n2 int value')
    return p


class TestParser(TestCase):
    def setUp(self):
        self.file = None

    def tearDown(self):
        if self.file:
            self.file.close()

    def test_nargs(self):
        def monitoring(value):
            try:
                n, v = value.split('_')
            except (IndexError, ValueError):
                raise ValueError('value ' + str(value) + ' is not name_value')

        parser = argparse.ArgumentParser()
        parser.add_argument('--monitoring', nargs='+', type=monitoring, help='a number of name_value tags')
        args = parser.parse_args(['--monitoring', 'a2'])


    def test_simple(self):
        args = parser_file().parse_args(['/etc/hosts', '/etc'])
        self.file = args.file
        self.assertEqual('/etc/hosts', args.file.name)
        self.assertEqual('/etc', args.dir_path)
        self.assertFalse(args.debug)

    def test_simple_debug(self):
        args = parser_file().parse_args(['/etc/hosts', '/etc', '--debug'])
        self.assertTrue(args.debug)

    def test_parser_yes_no(self):
        p = parser_yes_no()
        args = p.parse_args(['--is_tls', 'Y'])
        self.assertTrue(args.is_tls)

        args = p.parse_args(['--is_tls', 'N'])
        self.assertFalse(args.is_tls)

    def test_parser_int(self):
        p = parser_int()
        args = p.parse_args([])
        self.assertEqual(args.n1, 1)
        self.assertEqual(args.n2, 1)

        args = p.parse_args(['--n1', '1', '--n2', '2'])
        self.assertEqual(args.n1, 1)
        self.assertEqual(args.n2, 2)

        args = p.parse_args(['--n1', '-1', '--n2', '-2'])
        self.assertEqual(args.n1, -1)
        self.assertEqual(args.n2, -2)


if __name__ == '__main__':
    out = input(f'choose from {[x for x in locals() if x .startswith("parser")]}>>> ', )
    args = getattr(out)
    print(args)
