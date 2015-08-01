import os
import shutil
from functools import wraps
from pathlib import Path


FIXTURES_DIR_PATH = Path(__file__).parent / 'fixtures'
TEST_DIR_NAME = 'test_dir'
TEST_DIR = Path.cwd() / TEST_DIR_NAME


def load_fixture(fixture_name, destination):
    with (FIXTURES_DIR_PATH / fixture_name).open() as fixture:
        with (TEST_DIR / destination).open('w') as dest:
            dest.write(fixture.read())


def get_test_file_content(name):
    with (TEST_DIR / name).open() as test_file:
        return test_file.read()


def get_fixture_content(name):
    with (FIXTURES_DIR_PATH / name).open() as fixture:
        return fixture.read()


def isolated_workdir(test_function):

    @wraps(test_function)
    def wrapped():
        try:
            shutil.rmtree(TEST_DIR_NAME)
        except OSError:
            pass
        os.mkdir(TEST_DIR_NAME)

        original_working_dir = os.getcwd()
        os.chdir(TEST_DIR_NAME)

        try:
            test_function()
        finally:
            os.chdir(original_working_dir)
            shutil.rmtree(TEST_DIR_NAME)

    return wrapped
