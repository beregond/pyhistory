from __future__ import print_function

import os.path
import shutil
from datetime import date
from hashlib import md5


def add(args):
    _check_history_dir(args.history_dir)
    hashed = md5(args.message).hexdigest()[:7]

    filepath = os.path.join(args.history_dir, hashed)
    if os.path.exists(filepath):
        raise RuntimeError("Given entry already exists!")

    with open(filepath, 'w') as entry_file:
        entry_file.write(args.message + '\n')


def list_history(args):
    lines = _list_history(args.history_dir)
    print('\n' + ''.join(lines))


def update(args):
    with open(args.history_file) as history_file:
        lines = history_file.readlines()

    start = 0
    for line in lines:
        if not line.startswith('..') and line != '\n':
            break
        start += 1

    result = lines[:start + 3]

    release_date = args.date or date.today().strftime('%Y-%m-%d')
    header = '{} ({})'.format(args.version, release_date)
    result.append(header + '\n')
    result.append('+' * len(header) + '\n\n')

    result += _list_history(args.history_dir)
    result.append('\n')

    result += lines[start + 3:]

    result = ''.join(result)

    with open(args.history_file, 'w') as history_file:
        history_file.write(result)

    _delete_history_dir(args.history_dir)


def clear(args):
    _delete_history_dir(args.history_dir)


def _list_history(history_dir):
    result = []
    for root, _, files in os.walk(history_dir):
        for f in files:
            fullpath = os.path.join(root, f)
            with open(fullpath) as file_handler:
                result.append('* ' + file_handler.read())

    return result


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
