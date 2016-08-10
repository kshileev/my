#!/usr/bin/python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--foo', required=False, help='foo help')
parser.add_argument('--all', action='store_true', help='all help')
args = parser.parse_args()
