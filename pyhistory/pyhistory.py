import time
from itertools import count
from datetime import date as date_module
from hashlib import md5

from six import text_type as unicode

from .utilities import format_line


def add(message, history_dir):
    _check_history_dir(history_dir)
    message = unicode(message)
    hashed = _make_hash_name(message)
    filepath = history_dir / hashed
    with filepath.open('w') as file:
        file.write(message + '\n')


def _make_hash_name(message):
    return '{}-{}'.format(
        int(time.time() * 10 ** 6),
        md5(message.encode('utf-8')).hexdigest()[:7],
    )


def _check_history_dir(history_dir):
    if not history_dir.exists():
        history_dir.mkdir()


def list_(history_dir):
    return {key: _read(file) for key, file in _list_files(history_dir).items()}


def _list_files(history_dir):
    if not history_dir.exists():
        return {}

    return dict(zip(count(1), sorted(history_dir.iterdir())))


def update(
        version, history_dir, history_file, at_line=None, date=None,
        line_length=0, prefix=''):
    lines = _readlines(history_file)

    if at_line is not None:
        at_line = (max(int(at_line), 1))

    break_line = _calculate_break_line(lines, at_line)
    result = lines[:break_line]

    release_date = date or date_module.today().strftime('%Y-%m-%d')
    header = '{} ({})'.format(version, release_date)
    result.append(header + '\n')
    result.append('+' * len(header) + '\n\n')

    new_lines = [
        format_line(prefix, line, line_length)
        for line
        in list_(history_dir).values()
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
    [file.unlink() for file in history_dir.iterdir()]


def _list_history_files(history_dir):
    if not history_dir.exists():
        return []

    return [_read(file) for file in sorted(history_dir.iterdir())]


def _read(src):
    with src.open() as file:
        return file.read()


def _readlines(src):
    with src.open() as file:
        return file.readlines()


def delete(entries, history_dir):
    files = _list_files(history_dir)
    for entry in entries:
        try:
            files[entry].unlink()
        except KeyError:
            pass
