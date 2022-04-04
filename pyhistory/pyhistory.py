import time
from datetime import date as date_module
from hashlib import md5
from itertools import count

from .utilities import format_line


def add(message, history_dir):
    _check_history_dir(history_dir)
    message = str(message)
    hashed = _make_hash_name(message)
    filepath = history_dir / hashed
    with filepath.open("w") as history_entry:
        history_entry.write(message + "\n")


def _make_hash_name(message):
    message_hash = md5(message.encode("utf-8"))
    short_hash = message_hash.hexdigest()[:7]
    timestamp = int(time.time() * 10**6)
    return "{}-{}".format(timestamp, short_hash)


def _check_history_dir(history_dir):
    if not history_dir.exists():
        history_dir.mkdir()


def list_(history_dir):
    return {key: _read(file) for key, file in _list_files(history_dir).items()}


def _list_files(history_dir):
    lines = sorted(history_dir.iterdir()) if history_dir.exists() else []
    return dict(zip(count(1), lines))


def update(
    version,
    history_dir,
    history_file,
    at_line=None,
    date=None,
    line_length=0,
    prefix="",
):
    date = date or date_module.today().strftime("%Y-%m-%d")
    content = _get_paragraph(version, history_dir, date, line_length, prefix)
    history = _calculate_new_history(history_file, at_line, content)
    with history_file.open("w") as file:
        file.write(history)
    clear(history_dir)


def _calculate_new_history(history_file, at_line, content):
    old_lines = _readlines(history_file)
    break_line = _calculate_break_line(old_lines, at_line)
    result = old_lines[:break_line] + content + old_lines[break_line:]
    return "".join(result)


def _get_paragraph(version, history_dir, date, line_length, prefix):
    header = "{} ({})".format(version, date)
    content = [
        header + "\n",
        "+" * len(header) + "\n\n",
    ]
    lines = [
        format_line(prefix, line, line_length)
        for line in list_(history_dir).values()
    ]
    content += lines
    content.append("\n")
    return content


def _calculate_break_line(lines, at_line):
    if at_line is not None:
        return max(int(at_line) - 1, 0)

    start = 0
    for line in lines:
        if not line.startswith("..") and line != "\n":
            break
        start += 1

    return start + 3


def clear(history_dir):
    [history_file.unlink() for history_file in history_dir.iterdir()]


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
