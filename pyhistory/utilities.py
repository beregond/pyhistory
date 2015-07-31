

def split_into_lines(text, line_length):
    if line_length < 1:
        return [text]
    have_line_feed = text.endswith('\n')
    if have_line_feed:
        text = text.rstrip('\n')
    lines = list(_make_lines_from_words(text.split(' '), line_length))
    if have_line_feed:
        lines[-1] = lines[-1] + '\n'
    return lines


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


def find_file_across_parents(directory, file):
    wanted = directory / file
    while not wanted.exists() and wanted.parent != wanted.parent.parent:
        wanted = wanted.parent.parent / wanted.name

    if not wanted.exists():
        raise RuntimeError('History file not found!', file)

    return wanted
