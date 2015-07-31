from __future__ import print_function

import time
from itertools import count, chain
from datetime import date
from hashlib import md5

from six import text_type as unicode

from .utilities import split_into_lines

LINE_PREFIX = '* '
DEFAULT_LINE_LENGTH = 79


def add(message, history_dir):
    _check_history_dir(history_dir)
    message = unicode(message)
    hashed = _make_hash_name(message)
    filepath = history_dir / hashed
    if filepath.exists():
        raise RuntimeError("Collision, you lucky bastard!")
    with filepath.open('w') as file:
        file.write(message + '\n')


def _make_hash_name(message):
    return '{}-{}'.format(
        int(time.time() * 1000),
        md5(message.encode('utf-8')).hexdigest()[:7],
    )


def _check_history_dir(history_dir):
    if not history_dir.exists():
        history_dir.mkdir()


def list_history(history_dir, line_length):
    lines = _list_history_lines(history_dir)
    lines = [
        _format_line(LINE_PREFIX, line, line_length)
        for line
        in lines
    ]
    print('\n' + ''.join(lines))


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
    lines = _readlines(history_file)

    break_line = _calculate_break_line(lines, at_line)
    result = lines[:break_line]

    release_date = date_ or date.today().strftime('%Y-%m-%d')
    header = '{} ({})'.format(version, release_date)
    result.append(header + '\n')
    result.append('+' * len(header) + '\n\n')

    new_lines = [
        _format_line(LINE_PREFIX, line, line_length)
        for line
        in _list_history_lines(history_dir)
    ]
    result += new_lines
    result.append('\n')

    result += lines[break_line:]

    result = ''.join(result)

    with history_file.open('w') as file:
        file.write(result)

    clear(history_dir)


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
    for file in history_dir.iterdir():
        if file.is_dir():
            clear(file)
            file.rmdir()
        else:
            file.unlink()


def _list_history_lines(history_dir):
    if not history_dir.exists():
        return []
    return [_read(file) for file in sorted(history_dir.iterdir())]


def _read(src):
    with src.open() as file:
        return file.read()


def _readlines(src):
    with src.open() as file:
        return file.readlines()


def delete(entries, history_dir, line_length):
    files = _list_history_files(history_dir)
    files = dict(zip(count(1), files))

    if entries:
        for entry in entries:
            try:
                files[entry].unlink()
            except KeyError:
                pass
    else:
        lines = []
        for number, file in files.items():
            prefix = '{}. '.format(number)
            line = _format_line(prefix, _read(file), line_length)
            lines.append(line)

        lines = chain(lines, ['\n', '(Delete by choosing entries numbers.)'])
        print('\n' + ''.join(lines))


def _list_history_files(history_dir):
    if not history_dir.exists():
        return []
    return sorted(history_dir.iterdir())
