import os
import shutil

from functools import wraps


FIXTURES_DIR_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'fixtures'
)

TEST_DIR = 'test_dir'
TEST_DIR_PATH = os.path.join(os.getcwd(), TEST_DIR)


def load_fixture(fixture_name, destination):
    with open(os.path.join(FIXTURES_DIR_PATH, fixture_name)) as fixture:
        with open(os.path.join(TEST_DIR_PATH, destination), 'w') as dest:
            dest.write(fixture.read())


def get_test_file_content(name):
    with open(os.path.join(TEST_DIR_PATH, name)) as test_file:
        return test_file.read()


def get_fixture_content(name):
    with open(os.path.join(FIXTURES_DIR_PATH, name)) as fixture:
        return fixture.read()


def isolated_workdir(func):

    @wraps(func)
    def wrapped():
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass
        os.mkdir(TEST_DIR)

        original_working_dir = os.getcwd()
        os.chdir(TEST_DIR)

        func()

        os.chdir(original_working_dir)
        shutil.rmtree(TEST_DIR)

    return wrapped
