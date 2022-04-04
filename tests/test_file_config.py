from verify import expect

from pyhistory.file_config import get_defaults_from_config_file_if_exists

from . import isolated_workdir, load_fixture


@isolated_workdir
def test_get_config_from_file():
    load_fixture("setup.cfg", "empty.txt")
    pattern = {
        "history_dir": None,
        "history_file": None,
        "at_line": None,
        "line_length": None,
    }
    values = get_defaults_from_config_file_if_exists()
    for key, value in pattern.items():
        expect(value).to_be_equal(values.get(key))


@isolated_workdir
def test_load_config_from_setup_cfg():
    load_fixture("setup.cfg", "setup.cfg")
    pattern = {
        "history_dir": None,
        "history_file": "HISTORY.rst",
        "at_line": "42",
        "line_length": "92",
    }
    values = get_defaults_from_config_file_if_exists()
    for key, value in pattern.items():
        expect(value).to_be_equal(values.get(key))


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
        expect(value).to_be_equal(values.get(key))
