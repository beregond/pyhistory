import os
import unittest
import shutil

from invoke import run

FIXTURES_DIR_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'fixtures'
)
TEST_DIR = 'test_dir'
TEST_DIR_PATH = os.path.join(os.getcwd(), TEST_DIR)


class TestPyhistory(unittest.TestCase):

    def setUp(self):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass
        os.mkdir(TEST_DIR)

        self.original_working_dir = os.getcwd()
        os.chdir(TEST_DIR)

    def test_list_empty(self):
        result = run('pyhi list')
        self.assertEqual(result.stdout, _join_lines(['', '']))

    def test_add_list_and_clear(self):
        run('pyhi add some_message')
        result = run('pyhi list')
        self.assertEqual(result.stdout, _join_lines(
            ['', '* some_message', '']))

        run('pyhi add "next message"')
        result = run('pyhi list')
        self.assertEqual(result.stdout, _join_lines(
            ['', '* some_message', '* next message', '']))

        run('pyhi clear')
        result = run('pyhi list')
        self.assertEqual(result.stdout, _join_lines(['', '']))

    def test_update(self):
        _load_fixture('history1.rst', 'HISTORY.rst')
        run('pyhi add some_message')
        run('pyhi add "next message"')
        run('pyhi update 1.0.6 --date today')
        self.assertEqual(
            _get_fixture_content('history1_after.rst'),
            _get_test_file_content('HISTORY.rst')
        )

    def tearDown(self):
        os.chdir(self.original_working_dir)
        shutil.rmtree(TEST_DIR)


def _get_test_file_content(name):
    with open(os.path.join(TEST_DIR_PATH, name)) as test_file:
        return test_file.read()

def _get_fixture_content(name):
    with open(os.path.join(FIXTURES_DIR_PATH, name)) as fixture:
        return fixture.read()


def _load_fixture(fixture_name, destination):
    with open(os.path.join(FIXTURES_DIR_PATH, fixture_name)) as fixture:
        with open(os.path.join(TEST_DIR_PATH, destination), 'w') as dest:
            dest.write(fixture.read())


def _join_lines(output):
    return '\n'.join(output) + '\n'
