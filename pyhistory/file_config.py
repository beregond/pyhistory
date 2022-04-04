from configparser import ConfigParser, NoOptionError, NoSectionError
from pathlib import Path

from .utilities import find_file_across_parents

FILE_TO_CHECK = "setup.cfg"
CONFIG_SECTION = "pyhistory"


def get_defaults_from_config_file_if_exists(file_to_check=FILE_TO_CHECK):
    try:
        config_file = find_file_across_parents(Path.cwd(), file_to_check)
    except RuntimeError:
        return {}

    return _get_config_from_file(config_file)


def _get_config_from_file(config_file):
    parser = ConfigParser()
    parser.read(str(config_file))
    return _ConfigGetter(parser, CONFIG_SECTION)


class _ConfigGetter(object):
    def __init__(self, parser, section):
        self.parser = parser
        self.section = section

    def get(self, key, default=None):
        try:
            return self.parser.get(self.section, key)
        except (NoSectionError, NoOptionError):
            return default
