from unittest import TestCase


def parser_example(args):
    import argparse

    parser = argparse.ArgumentParser(prog='example')
    parser.add_argument('--foo', required=False, help='foo help')
    parser.add_argument('--all', action='store_true', help='all help')
    parser.add_argument('--str', type=str, choices=['a', 'b', 'c'], nargs='+', required=True, help='<REQUIRED> a list of strings')
    values = parser.parse_args(args)
    return values.foo, values.all, values.str


class TestParser(TestCase):
    def setUp(self):
        super(TestParser, self).setUp()

    def test_parser(self):
        self.assertEqual((None, False, ['a', 'b', 'c']), parser_example(args=['--str', 'a', 'b', 'c']))
