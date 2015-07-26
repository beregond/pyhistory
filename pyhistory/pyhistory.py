from __future__ import print_function

import os.path
import shutil
import time
from itertools import count, chain
from datetime import date
from hashlib import md5

from .utilities import find_file_across_path, split_into_lines

LINE_PREFIX = '* '
DEFAULT_LINE_LENGTH = 79


def add(message, history_dir):
    history_dir = str(history_dir)
    _check_history_dir(history_dir)
    hashed = '{}-{}'.format(
        int(time.time() * 1000),
        md5(message.encode('utf-8')).hexdigest()[:7])

    filepath = os.path.join(history_dir, hashed)
    if os.path.exists(filepath):
        raise RuntimeError("Collision, you lucky bastard!")

    with open(filepath, 'w') as entry_file:
        entry_file.write(message + '\n')


def list_history(history_dir, line_length):
    lines = _list_history_lines(str(history_dir))
    lines = [
        _format_line(LINE_PREFIX, line, line_length)
        for line
        in lines
    ]
    print('\n' + ''.join(lines))


def _get_line_length(args):
    try:
        return int(args.line_length)
    except ValueError:
        return DEFAULT_LINE_LENGTH


def _format_line(prefix, content, line_length):
    prefix_length = len(prefix)
    content = split_into_lines(content, line_length - prefix_length)
    secondary_prefix = ' ' * prefix_length
    lines = chain(
        [_prefix_line(prefix, content[0])],
        [_prefix_line(secondary_prefix, line) for line in content[1:]]
    )
    return '\n'.join(lines)


def _prefix_line(prefix, content):
    return '{}{}'.format(prefix, content)


def update(history_dir, history_file, version, at_line, date_, line_length):

    with open(str(history_file)) as hfile:
        lines = hfile.readlines()

    break_line = _calculate_break_line(lines, at_line)
    result = lines[:break_line]

    release_date = date_ or date.today().strftime('%Y-%m-%d')
    header = '{} ({})'.format(version, release_date)
    result.append(header + '\n')
    result.append('+' * len(header) + '\n\n')

    new_lines = [
        _format_line(LINE_PREFIX, line, line_length)
        for line
        in _list_history_lines(str(history_dir))
    ]
    result += new_lines
    result.append('\n')

    result += lines[break_line:]

    result = ''.join(result)

    with open(str(history_file), 'w') as hfile:
        hfile.write(result)

    _delete_history_dir(str(history_dir))


def _calculate_break_line(lines, at_line):
    if at_line:
        return max(0, int(at_line) - 1)

    start = 0
    for line in lines:
        if not line.startswith('..') and line != '\n':
            break
        start += 1

    return start + 3


def clear(history_dir):
    _delete_history_dir(str(history_dir))


def _list_history_files(history_dir):
    result = []
    for root, _, files in os.walk(history_dir):
        files.sort()
        result += [os.path.join(root, f) for f in files]

    return result


def _list_history_lines(history_dir):
    files = _list_history_files(history_dir)
    lines = []
    for file_ in files:
        with open(file_) as file_handler:
            lines.append(file_handler.read())

    return lines


def _check_history_dir(history_dir):
    try:
        os.stat(history_dir)
    except OSError:
        os.mkdir(history_dir)


def _delete_history_dir(history_dir):
    try:
        shutil.rmtree(history_dir)
    except OSError:
        pass


def _select_history_dir(args):
    filepath = os.path.join(os.getcwd(), args.history_file)
    return os.path.join(select_dir_with_file(filepath), args.history_dir)


def select_dir_with_file(filepath):
    dirname = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    try:
        return os.path.dirname(find_file_across_path(dirname, filename))
    except RuntimeError as error:
        raise RuntimeError('History file not found!', error)


def delete(entries, history_dir, line_length):
    files = _list_history_files(str(history_dir))
    files = zip(_str_count(1), files)

    if entries:
        register = {item[0]: item[1] for item in files}
        for entry in entries:
            try:
                file_to_delete = register[entry]
                os.remove(file_to_delete)
            except KeyError:
                pass
    else:
        lines = []
        for entry in files:
            with open(entry[1]) as file_handler:
                prefix = '{}. '.format(entry[0])
                line = _format_line(prefix, file_handler.read(), line_length)
                lines.append(line)

        lines = chain(lines, ['\n', '(Delete by choosing entries numbers.)'])
        print('\n' + ''.join(lines))


def _str_count(start=None):
    items = count(start)
    for item in items:
        yield str(item)
