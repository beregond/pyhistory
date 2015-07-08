import argparse

from . import __version__ as ver
from . import pyhistory, file_config

# Default values.
default_values = file_config.get_defaults_from_config_file_if_exists()
to_override_if_none = {
    'history_dir': 'history',
    'history_file': 'HISTORY.rst',
    'line_length': pyhistory.DEFAULT_LINE_LENGTH,
}

for key, value in to_override_if_none.items():
    default_values[key] = default_values[key] or value

# General parser.
parser = argparse.ArgumentParser(
    description="Manage Python project history file.")
parser.add_argument(
    '--version', action='version', version="Pyhistory ver {}".format(ver))
parser.add_argument('--history-dir', default=default_values['history_dir'])
parser.add_argument('--history-file', default=default_values['history_file'])

subparsers = parser.add_subparsers(help="sub-command help")

# Add.
parser_add = subparsers.add_parser('add', help="add new message")
parser_add.add_argument('message')
parser_add.set_defaults(func=pyhistory.add)

# List.
parser_list = subparsers.add_parser('list', help="list actual history")
parser_list.set_defaults(func=pyhistory.list_history)
parser_list.add_argument(
    '--line-length', default=default_values['line_length'])

# Update and squash.
update_parsers = [
    subparsers.add_parser('update', help='update history file'),
    subparsers.add_parser('squash', help='alias to "update"'),
]

for uparser in update_parsers:
    uparser.add_argument('version')
    uparser.add_argument('--date', help="date of release (by default today)")
    uparser.add_argument(
        '--at-line',
        help="at which line put history in history file",
        default=default_values['at_line']
    )
    uparser.set_defaults(func=pyhistory.update)
    uparser.add_argument(
        '--line-length', default=default_values['line_length'])

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
parser_delete.add_argument(
    '--line-length', default=default_values['line_length'])


def main():
    args = parser.parse_args()
    args.func(args)
