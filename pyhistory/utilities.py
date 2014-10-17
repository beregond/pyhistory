import os


def find_file_across_path(dirname, filename):
    filepath = os.path.join(dirname, filename)
    if os.path.exists(filepath):
        return filepath

    new_dirname = os.path.abspath(os.path.join(dirname, '..'))

    if dirname == new_dirname:
        raise RuntimeError('File not found!', filename)

    return find_file_across_path(new_dirname, filename)
