import os
from ConfigParser import ConfigParser, NoSectionError, NoOptionError

from .utilities import find_file_across_path

FILE_TO_CHECK = 'setup.cfg'
CONFIG_SECTION = 'pyhistory'


def get_defaults_from_config_file_if_exists(file_to_check=FILE_TO_CHECK):
    keys = [
        'history_dir',
        'history_file',
        'at_line',
    ]

    try:
        config_file = find_file_across_path(os.getcwd(), file_to_check)
    except RuntimeError:
        return {key: None for key in keys}

    config = _get_config_from_file(config_file)
    return {key: config.get_or_default(key) for key in keys}

def _get_config_from_file(config_file):
    parser = ConfigParser()
    parser.read(config_file)
    return _ConfigGetter(parser, CONFIG_SECTION)


class _ConfigGetter(object):

    def __init__(self, parser, section):
        self.parser = parser
        self.section = section

    def get_or_default(self, key, default=None):
        try:
            return self.parser.get(self.section, key)
        except (NoSectionError, NoOptionError):
            return default
