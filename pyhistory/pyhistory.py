from __future__ import print_function


import os.path
import shutil
import time
from itertools import count, chain
from datetime import date
from hashlib import md5


def add(args):

    history_dir = _select_history_dir(args)

    _check_history_dir(history_dir)
    hashed = '{}-{}'.format(
        time.time(), md5(args.message.encode('utf-8')).hexdigest()[:7])

    filepath = os.path.join(history_dir, hashed)
    if os.path.exists(filepath):
        raise RuntimeError("Collision you lucky bastard!")

    with open(filepath, 'w') as entry_file:
        entry_file.write(args.message + '\n')


def list_history(args):
    history_dir = _select_history_dir(args)
    lines = _list_history(history_dir)
    print('\n' + ''.join(lines))


def update(args):
    history_dir = _select_history_dir(args)
    history_file = os.path.join(history_dir, '..', args.history_file)

    with open(history_file) as hfile:
        lines = hfile.readlines()

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

    result += _list_history(history_dir)
    result.append('\n')

    result += lines[start + 3:]

    result = ''.join(result)

    with open(history_file, 'w') as hfile:
        hfile.write(result)

    _delete_history_dir(history_dir)


def clear(args):
    history_dir = _select_history_dir(args)
    _delete_history_dir(history_dir)


def _list_history(history_dir):
    result = []
    for root, _, files in os.walk(history_dir):
        files.sort()
        for f in files:
            fullpath = os.path.join(root, f)
            with open(fullpath) as file_handler:
                result.append('* ' + file_handler.read())

    return result


def _list_history_files(history_dir):
    result = []
    for root, _, files in os.walk(history_dir):
        files.sort()
        result += [os.path.join(root, f) for f in files]

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


def _select_history_dir(args):
    filepath = os.path.join(os.getcwd(), args.history_file)
    return os.path.join(select_dir_with_file(filepath), args.history_dir)


def select_dir_with_file(filepath):
    dirname = os.path.dirname(filepath)
    if os.path.exists(filepath):
        return dirname

    new_dirname = os.path.abspath(os.path.join(dirname, '..'))

    if dirname == new_dirname:
        raise RuntimeError('File not found!')

    new_filepath = os.path.join(new_dirname, os.path.basename(filepath))

    return select_dir_with_file(new_filepath)


def delete(args):
    history_dir = _select_history_dir(args)

    files = _list_history_files(history_dir)
    files = zip(_str_count(1), files)

    if args.entry:
        register = {item[0]: item[1] for item in files}
        for entry in args.entry:
            try:
                file_to_delete = register[entry]
                os.remove(file_to_delete)
            except KeyError:
                pass
    else:
        lines = []
        for entry in files:
            with open(entry[1]) as file_handler:
                lines.append('{}. {}'.format(entry[0], file_handler.read()))

        lines = chain(lines, ['\n', '(Delete by choosing entries numbers.)'])
        print('\n' + ''.join(lines))


def _str_count(start=None):
    items = count(start)
    for item in items:
        yield str(item)
