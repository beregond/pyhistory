import os


def find_file_across_path(dirname, filename):
    filepath = os.path.join(dirname, filename)
    if os.path.exists(filepath):
        return filepath

    new_dirname = os.path.abspath(os.path.join(dirname, '..'))

    if dirname == new_dirname:
        raise RuntimeError('File not found!', filename)

    return find_file_across_path(new_dirname, filename)


def split_into_lines(text, line_length):
    if line_length < 1:
        return [text]
    return list(_make_lines_from_words(text.split(' '), line_length))


def _make_lines_from_words(words, line_length):
    if len(words) < 2:
        for word in words:
            yield word
        raise StopIteration()

    line = _LineBuffer()
    for word in words:
        if len(line) and line.length_if_add(word) > line_length:
            yield line.flush()
        line.add(word)

    yield line.flush()


class _LineBuffer(object):

    def __init__(self):
        self.line = ''
        self.length = 0

    def __str__(self):
        return self.line

    def __len__(self):
        return self.length

    def add(self, word):
        if self.line:
            self.line += ' ' + word
        else:
            self.line += word
        self.length = len(self.line)

    def length_if_add(self, word):
        length = len(self) + len(word)
        if len(self):
            length += 1
        return length

    def flush(self):
        value = self.line
        self.__init__()
        return value
