import os.path
from hashlib import md5


def add(args):
    _check_history_dir(args.history_dir)
    hashed = md5(args.message).hexdigest()[:7]

    filepath = os.path.join(args.history_dir, hashed)
    if os.path.exists(filepath):
        raise RuntimeError("Given entry already exists!")

    with open(filepath, 'w') as entry_file:
        entry_file.write(args.message + '\n')


def _check_history_dir(history_dir):
    try:
        os.stat(history_dir)
    except OSError:
        os.mkdir(history_dir)
