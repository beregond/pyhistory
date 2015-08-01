import time
from itertools import count
from datetime import date
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


def list_history(history_dir):
    return [_read(file) for file in _list_history_files(history_dir)]


def update(
        history_dir, history_file, version, at_line, date_, line_length,
        prefix):
    lines = _readlines(history_file)

    break_line = _calculate_break_line(lines, at_line)
    result = lines[:break_line]

    release_date = date_ or date.today().strftime('%Y-%m-%d')
    header = '{} ({})'.format(version, release_date)
    result.append(header + '\n')
    result.append('+' * len(header) + '\n\n')

    new_lines = [
        format_line(prefix, line, line_length)
        for line
        in list_history(history_dir)
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
    if history_dir.exists():
        return sorted(history_dir.iterdir())
    return []


def _read(src):
    with src.open() as file:
        return file.read()


def _readlines(src):
    with src.open() as file:
        return file.readlines()


def delete(entries, history_dir):
    files = list_for_delete(history_dir)
    for entry in entries:
        try:
            files[entry].unlink()
        except KeyError:
            pass


def list_for_delete(history_dir):
    return dict(zip(count(1), _list_history_files(history_dir)))
