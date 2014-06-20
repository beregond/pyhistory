import argparse

from . import __version__ as ver
from . import cli_commands

parser = argparse.ArgumentParser(
    description="Manage Python project history file.")
parser.add_argument(
    '--version', action='version', version="PyHistory ver {}".format(ver))
parser.add_argument('--history-dir', default='history')

subparsers = parser.add_subparsers(help="sub-command help")

parser_add = subparsers.add_parser('add', help="add new message")
parser_add.add_argument('message')
parser_add.set_defaults(func=cli_commands.add)

parser_list = subparsers.add_parser('list', help="list actual history")
parser_list.set_defaults(func=cli_commands.list_history)

parser_update = subparsers.add_parser(
    'update', help='update history file')
parser_update.add_argument('version')
parser_update.add_argument(
    '--history-file', default='HISTORY.rst')
parser_update.add_argument('--date', help="date of release (by default today)")
parser_update.set_defaults(func=cli_commands.update)

parser_clear = subparsers.add_parser(
    'clear', help="remove entries from history directory")
parser_clear.set_defaults(func=cli_commands.clear)


def main():
    args = parser.parse_args()
    args.func(args)
