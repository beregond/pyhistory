import os
import unittest
import shutil

from invoke import run

from pyhistory.pyhistory import select_dir_with_file

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
        open('HISTORY.rst', 'w').close()
        result = run('pyhi list')
        self.assertEqual(result.stdout, _join_lines(['', '']))

    def test_add_list_and_clear(self):
        open('HISTORY.rst', 'w').close()

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
        self._test_update('update')

    def test_squash(self):
        self._test_update('squash')

    def _test_update(self, command):
        _load_fixture('history1.rst', 'HISTORY.rst')
        run('pyhi add some_message')
        run('pyhi add "next message"')
        run('pyhi {} 1.0.6 --date today'.format(command))
        self.assertEqual(
            _get_fixture_content('history1_after.rst'),
            _get_test_file_content('HISTORY.rst')
        )

    def test_pyhistory_when_not_in_history_file_directory(self):
        command = 'update'

        _load_fixture('history1.rst', 'HISTORY.rst')

        original_working_dir = os.getcwd()
        os.makedirs('one/two')
        os.chdir('one/two')

        run('pyhi add some_message')
        run('pyhi add "next message"')

        self.assertEqual(0, len(os.listdir(os.getcwd())))

        result = run('pyhi list')
        self.assertEqual(result.stdout, _join_lines(
            ['', '* some_message', '* next message', '']))

        os.chdir(original_working_dir)
        result = run('pyhi list')
        self.assertEqual(result.stdout, _join_lines(
            ['', '* some_message', '* next message', '']))

        os.chdir('one/two')
        run('pyhi {} 1.0.6 --date today'.format(command))
        os.chdir(original_working_dir)

        self.assertEqual(
            _get_fixture_content('history1_after.rst'),
            _get_test_file_content('HISTORY.rst')
        )

    def test_select_dir_with_file(self):
        os.makedirs('one/two')
        os.chdir('one')
        proper_dir = os.getcwd()
        open('some_file.rst', 'w').close()
        os.chdir('two')

        selected_dir = select_dir_with_file(
            os.path.join(os.getcwd(), 'some_file.rst'))

        self.assertEqual(proper_dir, selected_dir)

    def test_select_dir_with_fails_when_not_found(self):
        self.assertRaises(
            RuntimeError, select_dir_with_file, '/!hope_this_not_exists')

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
