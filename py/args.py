import argparse
from log import logger

parser = argparse.ArgumentParser()
parser.add_argument('--foo', required=False, help='foo help')
parser.add_argument('--all', action='store_true', help='all help')
parser.add_argument('--str', type=str, nargs='+', required=True, help='<REQUIRED> a list of strings')
args = parser.parse_args()
logger.info(args)
