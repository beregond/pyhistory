from itertools import chain

from .exceptions import FileNotFound


def split_into_lines(text, line_length):
    if line_length < 1:
        return [text]
    have_line_feed = text.endswith("\n")
    if have_line_feed:
        text = text.rstrip("\n")
    lines = list(_make_lines_from_words(text.split(" "), line_length))
    if have_line_feed:
        lines[-1] = lines[-1] + "\n"
    return lines


def _make_lines_from_words(words, line_length):
    line = _LineBuffer()
    for word in words:
        if len(line) and line.length_if_add(word) > line_length:
            yield line.flush()
        line.add(word)

    yield line.flush()


class _LineBuffer(object):
    def __init__(self, words=[]):
        self.words = words or []

    @property
    def line(self):
        return " ".join(self.words)

    def __len__(self):
        return len(self.line)

    def add(self, word):
        self.words.append(word)

    def length_if_add(self, word):
        return len(_LineBuffer(self.words + [word]))

    def flush(self):
        value = self.line
        self.__init__()
        return value


def find_file_across_parents(directory, file):
    wanted = directory / file
    while not wanted.exists() and wanted.parent != wanted.parent.parent:
        wanted = wanted.parent.parent / wanted.name

    if not wanted.exists():
        raise FileNotFound("File not found!", file)

    return wanted


def format_line(prefix, content, line_length):
    prefix_length = len(prefix)
    content = split_into_lines(content, line_length - prefix_length)
    secondary_prefix = " " * prefix_length
    lines = chain(
        [_prefix_line(prefix, content[0])],
        [_prefix_line(secondary_prefix, line) for line in content[1:]],
    )
    return "\n".join(lines)


def _prefix_line(prefix, content):
    return "{}{}".format(prefix, content)
