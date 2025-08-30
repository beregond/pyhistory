from pyhistory.file_config import get_defaults_from_config_file_if_exists

from . import isolated_workdir, load_fixture


@isolated_workdir
def test_get_config_from_empty_cfg_file():
    load_fixture("empty.txt", "setup.cfg")
    pattern = {
        "history_dir": None,
        "history_file": None,
        "at_line": None,
        "line_length": None,
    }
    values = get_defaults_from_config_file_if_exists()
    for key, value in pattern.items():
        assert value == values.get(key)


@isolated_workdir
def test_load_config_from_setup_cfg():
    load_fixture("setup.cfg", "setup.cfg")
    pattern = {
        "history_dir": None,
        "history_file": "HISTORY.rst",
        "at_line": "42",
        "line_length": "92",
        "md_header_level": "3",
    }
    values = get_defaults_from_config_file_if_exists()
    for key, value in pattern.items():
        assert value == values.get(key)


@isolated_workdir
def test_load_config_when_file_doesnt_exist():
    pattern = {
        "history_dir": None,
        "history_file": None,
        "at_line": None,
        "line_length": None,
    }
    values = get_defaults_from_config_file_if_exists()
    for key, value in pattern.items():
        assert value == values.get(key)


@isolated_workdir
def test_get_config_from_empty_toml_file():
    load_fixture("empty.txt", "pyproject.toml")
    pattern = {
        "history_dir": None,
        "history_file": None,
        "at_line": None,
        "line_length": None,
    }
    values = get_defaults_from_config_file_if_exists()
    for key, value in pattern.items():
        assert value == values.get(key)


@isolated_workdir
def test_load_config_from_pyproject_file():
    load_fixture("pyproject.toml", "pyproject.toml")
    pattern = {
        "history_dir": None,
        "history_file": "history.md",
        "at_line": 7,
        "line_length": None,
        "md_header_level": 2,
    }
    values = get_defaults_from_config_file_if_exists()
    for key, value in pattern.items():
        assert value == values.get(key)


@isolated_workdir
def test_load_config_from_setup_cfg_has_precedence():
    load_fixture("setup.cfg", "setup.cfg")
    load_fixture("pyproject.toml", "pyproject.toml")
    pattern = {
        "history_dir": None,
        "history_file": "HISTORY.rst",
        "at_line": "42",
        "line_length": "92",
        "md_header_level": "3",
    }
    values = get_defaults_from_config_file_if_exists()
    for key, value in pattern.items():
        assert value == values.get(key)
