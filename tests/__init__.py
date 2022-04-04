import os
import shutil
import tempfile
from pathlib import Path

FIXTURES_DIR_PATH = Path(__file__).parent / "fixtures"
TEST_DIR_NAME = "test_dir"
TEST_DIR = Path.cwd() / TEST_DIR_NAME


def load_fixture(fixture_name, destination):
    with (FIXTURES_DIR_PATH / fixture_name).open() as fixture:
        with (Path.cwd() / destination).open("w") as dest:
            dest.write(fixture.read())


def load_fixture_to(fixture_name, destination):
    with (FIXTURES_DIR_PATH / fixture_name).open() as fixture:
        with destination.open("w") as dest:
            dest.write(fixture.read())


def get_test_file_content(name):
    with (Path.cwd() / name).open() as test_file:
        return test_file.read()


def get_fixture_content(name):
    with (FIXTURES_DIR_PATH / name).open() as fixture:
        return fixture.read()


def isolated_workdir(test_function):
    def wrapped():
        temp_dir = tempfile.mkdtemp()
        original_working_dir = os.getcwd()
        os.chdir(temp_dir)

        try:
            test_function()
        finally:
            os.chdir(original_working_dir)
            shutil.rmtree(temp_dir)

    return wrapped


def isolated_env(test_function):
    def wrapped(*args, **kwargs):
        temp_dir = tempfile.mkdtemp()
        history_file = Path(temp_dir) / "HISTORY.rst"
        history_dir = Path(temp_dir) / "history"
        try:
            test_function(history_dir, history_file, *args, **kwargs)
        finally:
            shutil.rmtree(temp_dir)

    return wrapped
