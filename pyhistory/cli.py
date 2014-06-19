import argparse

from . import __version__ as ver
from . import cli_commands

parser = argparse.ArgumentParser(description="Manage project history file.")
parser.add_argument(
    '--version', action='version', version='PyHistory ver {}'.format(ver))
parser.add_argument('--history-dir', dest='history_dir', default='history')

subparsers = parser.add_subparsers(help='sub-command help')

parser_add = subparsers.add_parser('add')
parser_add.add_argument('message')
parser_add.set_defaults(func=cli_commands.add)


def main():
    args = parser.parse_args()
    args.func(args)
