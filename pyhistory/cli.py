import argparse

from . import __version__ as ver
from . import pyhistory

# General parser.
parser = argparse.ArgumentParser(
    description="Manage Python project history file.")
parser.add_argument(
    '--version', action='version', version="Pyhistory ver {}".format(ver))
parser.add_argument('--history-dir', default='history')
parser.add_argument('--history-file', default='HISTORY.rst')

subparsers = parser.add_subparsers(help="sub-command help")

# Add.
parser_add = subparsers.add_parser('add', help="add new message")
parser_add.add_argument('message')
parser_add.set_defaults(func=pyhistory.add)

# List.
parser_list = subparsers.add_parser('list', help="list actual history")
parser_list.set_defaults(func=pyhistory.list_history)

# Update and squash.
update_parsers = [
    subparsers.add_parser('update', help='update history file'),
    subparsers.add_parser('squash', help='alias to "update"'),
]

for uparser in update_parsers:
    uparser.add_argument('version')
    uparser.add_argument('--date', help="date of release (by default today)")
    uparser.add_argument(
        '--at-line', help="at which line put history in history file")
    uparser.set_defaults(func=pyhistory.update)

# Clear.
parser_clear = subparsers.add_parser(
    'clear', help="remove all entries from history directory")
parser_clear.set_defaults(func=pyhistory.clear)

# Delete.
parser_delete = subparsers.add_parser(
    'delete', help="remove specified entries from history directory")
parser_delete.add_argument(
    'entry', help='Entries to delete', nargs='*')
parser_delete.set_defaults(func=pyhistory.delete)


def main():
    args = parser.parse_args()
    args.func(args)
