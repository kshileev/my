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


simple = argparse.ArgumentParser(prog='./args.py', description='test parser to learn how to create arguments')
simple.add_argument('file', type=argparse.FileType('r'), help='path to some file')  # single positional
simple.add_argument('--debug', action='store_true', help='is debug?')
simple.add_argument('--ip', type=ip, help='ip address')
simple.add_argument('dir_path', type=abs_dir_path, nargs='?', default='~', help='path to dir')  # optional single positional (? means 0 or 1), custom type, dest not allowed
simple.add_argument('--pod', type=str, choices=['a', 'b', 'c'], nargs='+', required=False, help='list of strings')


class TestParser(TestCase):
    def test_simple(self):
        args = simple.parse_args(['/etc/hosts', '/etc'])
        self.assertEqual('/etc/hosts', args.file.name)
        self.assertEqual('/etc', args.dir_path)
        args.file.close()


if __name__ == '__main__':
    args = simple.parse_args()
    print(args)
