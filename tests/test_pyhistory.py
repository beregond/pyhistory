import os
import time
import shutil

import pytest
from invoke import run as original_run
from invoke.exceptions import Failure
from verify import expect

from pyhistory.pyhistory import select_dir_with_file
from pyhistory.file_config import get_defaults_from_config_file_if_exists
from pyhistory.utilities import split_into_lines

FIXTURES_DIR_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'fixtures'
)
TEST_DIR = 'test_dir'
TEST_DIR_PATH = os.path.join(os.getcwd(), TEST_DIR)


def run(command):
    return original_run(command, hide=True)


def _list_dir_without_dotfiles(path):
    return [item for item in os.listdir(path) if not item.startswith('.')]


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
        _load_fixture('history1.rst', 'HISTORY.rst')
        run('pyhi add some_message')
        _sleep()
        run('pyhi add "next message"')
        run('pyhi update 1.0.6 --date today')

        content = _get_fixture_content('history1_after.rst')
        file_content = _get_test_file_content('HISTORY.rst')
        assert content == file_content

    def test_update_at_line(self):
        _load_fixture('history1.rst', 'HISTORY.rst')
        run('pyhi add some_message')
        _sleep()
        run('pyhi add "next message"')
        run('pyhi update 1.0.6 --date today --at-line 1')

        content = _get_fixture_content('history1_at_line_after.rst')
        file_content = _get_test_file_content('HISTORY.rst')
        assert content == file_content

        _load_fixture('history1.rst', 'HISTORY.rst')
        run('pyhi add some_message')
        _sleep()
        run('pyhi add "next message"')
        run('pyhi update 1.0.6 --date today --at-line 0')

        content = _get_fixture_content('history1_at_line_after.rst')
        file_content = _get_test_file_content('HISTORY.rst')
        assert content == file_content

        _load_fixture('history1.rst', 'HISTORY.rst')
        run('pyhi add some_message')
        _sleep()
        run('pyhi add "next message"')
        run('pyhi update 1.0.6 --date today --at-line 7')

        content = _get_fixture_content('history1_at_line_after2.rst')
        file_content = _get_test_file_content('HISTORY.rst')
        expect(content).Equal(file_content)

    def test_update_with_line_too_long(self):
        _load_fixture('history1.rst', 'HISTORY.rst')
        run(
            'pyhi add "some very long and sophisticated message, which is too '
            'long to fit 79 characters"'
        )
        _sleep()
        run(
            'pyhi add "next message, which also is very long, but should fit '
            'into 79 characters aaaa"'
        )
        _sleep()
        run(
            'pyhi add "let just say Lorem ipsum dolor sit amet consectetur '
            'adipisicing elit, sed do eiusmod tempor incididunt ut labore et '
            'dolore magna aliqua. Ut enim ad minim veniam, quis nostrud '
            'exercitation ullamco"'
        )

        run('pyhi update 1.0.6 --date today')

        content = _get_fixture_content('history1_update_long_line.rst')
        file_content = _get_test_file_content('HISTORY.rst')
        expect(content).Equal(file_content)

    def test_list_long_line(self):
        _load_fixture('history1.rst', 'HISTORY.rst')

        run(
            'pyhi add "some very long and sophisticated message, which is too '
            'long to fit 79 characters"'
        )

        result = run('pyhi list')
        expect(result.stdout).Equal(
            '\n'
            '* some very long and sophisticated message, which is too long to '
            'fit 79\n'
            '  characters\n'
            '\n'
        )

    def test_list_long_line_when_disabled(self):
        _load_fixture('history1.rst', 'HISTORY.rst')

        run(
            'pyhi add "some very long and sophisticated message, which is too '
            'long to fit 79 characters"'
        )

        result = run('pyhi list --line-length=0')
        expect(result.stdout).Equal(
            '\n'
            '* some very long and sophisticated message, which is too long to '
            'fit 79 characters\n'
            '\n'
        )

    def test_line_length_disabled_when_negative(self):
        _load_fixture('history1.rst', 'HISTORY.rst')

        run(
            'pyhi add "some very long and sophisticated message, which is too '
            'long to fit 79 characters"'
        )

        result = run('pyhi list --line-length=0')
        expect(result.stdout).Equal(
            '\n'
            '* some very long and sophisticated message, which is too long to '
            'fit 79 characters\n'
            '\n'
        )

    def test_line_length_default_if_not_integer_provided(self):
        _load_fixture('history1.rst', 'HISTORY.rst')

        run(
            'pyhi add "some very long and sophisticated message, which is too '
            'long to fit 79 characters"'
        )

        with pytest.raises(Failure):
            run('pyhi list --line-length=asdf')

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

    def test_delete_long_lines(self):
        _load_fixture('history1.rst', 'HISTORY.rst')

        run(
            'pyhi add "some very long and sophisticated message, which is too '
            'long to fit 79 characters"'
        )
        _sleep()
        messages = [
            'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
        ]
        for message in messages:
            run('pyhi add {}'.format(message))
            _sleep()
        run(
            'pyhi add "next message, which also is very long, and should not '
            'fit into 79 characters"'
        )

        result = run('pyhi delete')
        expect(result.stdout).Equal(
            '\n'
            '1. some very long and sophisticated message, which is too long '
            'to fit 79\n'
            '   characters\n'
            '2. two\n'
            '3. three\n'
            '4. four\n'
            '5. five\n'
            '6. six\n'
            '7. seven\n'
            '8. eight\n'
            '9. nine\n'
            '10. next message, which also is very long, and should not fit '
            'into 79\n'
            '    characters\n'
            '\n'
            '(Delete by choosing entries numbers.)\n'
        )

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
            'line_length': None,
        }
        assert pattern == get_defaults_from_config_file_if_exists()

    def test_load_config_from_setup_cfg(self):
        _load_fixture('setup.cfg', 'setup.cfg')
        pattern = {
            'history_dir': None,
            'history_file': 'HISTORY.rst',
            'at_line': '42',
            'line_length': '92',
        }
        assert pattern == get_defaults_from_config_file_if_exists()

    def test_load_config_when_file_doesnt_exist(self):
        pattern = {
            'history_dir': None,
            'history_file': None,
            'at_line': None,
            'line_length': None,
        }
        assert pattern == get_defaults_from_config_file_if_exists('!wrong')


class TestUtilities(object):

    def test_split_simple_case(self):
        expect(split_into_lines('text', 10)).Equal(['text'])

    def test_split_empty_string(self):
        expect(split_into_lines('', 10)).Equal([''])

    def test_split_negative_line_length(self):
        expect(split_into_lines('cha cha cha', -1)).Equal(['cha cha cha'])

    def test_split_zero_line_length(self):
        expect(split_into_lines('cha cha cha', 0)).Equal(['cha cha cha'])

    def test_split_line(self):
        expect(split_into_lines('cha cha cha', 1)).Equal(['cha', 'cha', 'cha'])
        expect(split_into_lines('cha cha cha', 2)).Equal(['cha', 'cha', 'cha'])
        expect(split_into_lines('cha cha cha', 3)).Equal(['cha', 'cha', 'cha'])
        expect(split_into_lines('cha cha cha', 6)).Equal(['cha', 'cha', 'cha'])
        expect(split_into_lines('cha cha cha', 7)).Equal(['cha cha', 'cha'])

    def test_split_with_words_too_long(self):
        expect(split_into_lines('aaaaaaaaa bbb ccc', 4)).Equal(
            ['aaaaaaaaa', 'bbb', 'ccc']
        )
        expect(split_into_lines('bbb ccc aaaaaaaaa ddd', 4)).Equal(
            ['bbb', 'ccc', 'aaaaaaaaa', 'ddd']
        )

    def test_split_line_with_line_feed_at_the_end(self):
        expect(split_into_lines('cha cha\n', 6)).Equal(['cha', 'cha\n'])
        expect(split_into_lines('cha cha\n', 7)).Equal(['cha cha\n'])


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
