import os
import time
import shutil

import pytest
from invoke import run as original_run

from pyhistory.pyhistory import select_dir_with_file
from pyhistory.file_config import get_defaults_from_config_file_if_exists

FIXTURES_DIR_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'fixtures'
)
TEST_DIR = 'test_dir'
TEST_DIR_PATH = os.path.join(os.getcwd(), TEST_DIR)


def run(command):
    return original_run(command, hide=True)


def _list_dir_without_dotfiles(path):
    dirs = os.listdir(path)
    return [d for d in dirs if not d.startswith('.')]


class TestPyhistory(object):

    def setup_method(self, method):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass
        os.mkdir(TEST_DIR)

        self.original_working_dir = os.getcwd()
        os.chdir(TEST_DIR)

    def teardown_method(self, method):
        os.chdir(self.original_working_dir)
        shutil.rmtree(TEST_DIR)

    def test_list_empty(self):
        open('HISTORY.rst', 'w').close()
        result = run('pyhi list')
        assert result.stdout == _join_lines(['', ''])

    def test_add_list_and_clear(self):
        open('HISTORY.rst', 'w').close()

        run('pyhi add some_message')
        result = run('pyhi list')
        assert result.stdout == _join_lines(['', '* some_message', ''])

        _sleep()

        run('pyhi add "next message"')
        result = run('pyhi list')
        assert result.stdout == _join_lines(
            ['', '* some_message', '* next message', ''])

        run('pyhi clear')
        result = run('pyhi list')
        assert result.stdout == _join_lines(['', ''])

    def test_update(self):
        self._test_update('update')

    def test_squash(self):
        self._test_update('squash')

    def _test_update(self, command):
        _load_fixture('history1.rst', 'HISTORY.rst')
        run('pyhi add some_message')
        _sleep()
        run('pyhi add "next message"')
        run('pyhi {} 1.0.6 --date today'.format(command))

        content = _get_fixture_content('history1_after.rst')
        file_content = _get_test_file_content('HISTORY.rst')
        assert content == file_content

    def test_update_at_line(self):
        self._test_update_at_line('update')

    def test_squash_at_line(self):
        self._test_update_at_line('squash')

    def _test_update_at_line(self, command):
        _load_fixture('history1.rst', 'HISTORY.rst')
        run('pyhi add some_message')
        _sleep()
        run('pyhi add "next message"')
        run('pyhi {} 1.0.6 --date today --at-line 1'.format(command))

        content = _get_fixture_content('history1_at_line_after.rst')
        file_content = _get_test_file_content('HISTORY.rst')
        assert content == file_content

        _load_fixture('history1.rst', 'HISTORY.rst')
        run('pyhi add some_message')
        _sleep()
        run('pyhi add "next message"')
        run('pyhi {} 1.0.6 --date today --at-line 0'.format(command))

        content = _get_fixture_content('history1_at_line_after.rst')
        file_content = _get_test_file_content('HISTORY.rst')
        assert content == file_content

        _load_fixture('history1.rst', 'HISTORY.rst')
        run('pyhi add some_message')
        _sleep()
        run('pyhi add "next message"')
        run('pyhi {} 1.0.6 --date today --at-line 7'.format(command))

        content = _get_fixture_content('history1_at_line_after2.rst')
        file_content = _get_test_file_content('HISTORY.rst')
        assert content == file_content

    def test_pyhistory_when_not_in_history_file_directory(self):
        _load_fixture('history1.rst', 'HISTORY.rst')

        original_working_dir = os.getcwd()
        os.makedirs('one/two')
        os.chdir('one/two')

        run('pyhi add some_message')
        _sleep()
        run('pyhi add "next message"')
        _sleep()

        assert 0 == len(_list_dir_without_dotfiles(os.getcwd()))

        result = run('pyhi list')
        assert result.stdout == _join_lines(
            ['', '* some_message', '* next message', ''])

        os.chdir(original_working_dir)
        result = run('pyhi list')
        assert result.stdout == _join_lines(
            ['', '* some_message', '* next message', ''])

        os.chdir('one/two')
        run('pyhi update 1.0.6 --date today')
        os.chdir(original_working_dir)

        content = _get_fixture_content('history1_after.rst')
        file_content = _get_test_file_content('HISTORY.rst')
        assert content == file_content

    def test_select_dir_with_file(self):
        os.makedirs('one/two')
        os.chdir('one')
        proper_dir = os.getcwd()
        open('some_file.rst', 'w').close()
        os.chdir('two')

        selected_dir = select_dir_with_file(
            os.path.join(os.getcwd(), 'some_file.rst'))

        assert proper_dir == selected_dir

    def test_select_dir_with_fails_when_not_found(self):

        with pytest.raises(RuntimeError):
            select_dir_with_file('/!hope_this_does_not_exist')

    def test_delete(self):
        _load_fixture('history1.rst', 'HISTORY.rst')

        run('pyhi add some_message')
        _sleep()
        run('pyhi add "next message"')
        _sleep()

        result = run('pyhi list')
        assert result.stdout == _join_lines(
            ['', '* some_message', '* next message', ''])

        result = run('pyhi delete')
        assert result.stdout == _join_lines([
            '', '1. some_message', '2. next message', '',
            '(Delete by choosing entries numbers.)',
        ])

        run('pyhi delete 1')
        result = run('pyhi list')
        assert result.stdout == _join_lines(['', '* next message', ''])

        run('pyhi add test')
        _sleep()
        run('pyhi add test2')

        result = run('pyhi delete')
        assert result.stdout == _join_lines([
            '', '1. next message', '2. test', '3. test2', '',
            '(Delete by choosing entries numbers.)',
        ])

        run('pyhi delete 10')
        result = run('pyhi delete')
        assert result.stdout == _join_lines([
            '', '1. next message', '2. test', '3. test2', '',
            '(Delete by choosing entries numbers.)',
        ])

        run('pyhi delete 2 3 5 101')
        result = run('pyhi list')
        assert result.stdout == _join_lines(['', '* next message', ''])

    def test_delete_in_non_root(self):
        os.makedirs('one/two')
        os.chdir('one')
        self.test_delete()

    def test_get_config_from_file(self):
        _load_fixture('setup.cfg', 'empty.txt')
        pattern = {
            'history_dir': None,
            'history_file': None,
            'at_line': None,
        }
        assert pattern == get_defaults_from_config_file_if_exists()

    def test_load_config_from_setup_cfg(self):
        _load_fixture('setup.cfg', 'setup.cfg')
        pattern = {
            'history_dir': None,
            'history_file': 'HISTORY.rst',
            'at_line': '42',
        }
        assert pattern == get_defaults_from_config_file_if_exists()

    def test_load_config_when_file_doesnt_exist(self):
        pattern = {
            'history_dir': None,
            'history_file': None,
            'at_line': None,
        }
        assert pattern == get_defaults_from_config_file_if_exists('!wrong')

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


def _sleep():
    time.sleep(0.001)
