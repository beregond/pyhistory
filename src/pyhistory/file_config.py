import toml
from typing import Any

from configparser import ConfigParser
from pathlib import Path

from .utilities import find_file_across_parents
from .exceptions import FileNotFound

CFG_FILE_TO_CHECK = "setup.cfg"
TOML_FILE_TO_CHECK = "pyproject.toml"
CONFIG_SECTION = "pyhistory"


def get_defaults_from_config_file_if_exists() -> dict[str, Any]:
    try:
        config_file = find_file_across_parents(Path.cwd(), CFG_FILE_TO_CHECK)
    except FileNotFound:
        pass
    else:
        parser = ConfigParser()
        parser.read(str(config_file))
        return (
            dict(parser.items(CONFIG_SECTION))
            if parser.has_section(CONFIG_SECTION)
            else {}
        )

    try:
        config_file = find_file_across_parents(Path.cwd(), TOML_FILE_TO_CHECK)
    except FileNotFound:
        return {}
    else:
        with config_file.open() as f:
            data = toml.load(f)
            return data.get("tool", {}).get(CONFIG_SECTION, {})
