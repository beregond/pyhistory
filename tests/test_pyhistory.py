import os
import shutil

from verify import expect
from click.testing import CliRunner

from pyhistory.utilities import split_into_lines
from pyhistory.cli import main
from . import (
    TEST_DIR, load_fixture, get_fixture_content, get_test_file_content
)


def run(command):
    runner = CliRunner()
    return runner.invoke(main, command)


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
        result = run(['list'])
        expect(result.output).to_be_equal(_join_lines(['', '']))

    def test_add_list_and_clear(self):
        open('HISTORY.rst', 'w').close()

        run(['add', 'some_message'])
        result = run(['list'])
        expect(result.output).to_be_equal(
            _join_lines(['', '* some_message', ''])
        )
        run(['add', 'next message'])
        result = run(['list'])
        expect(result.output).to_be_equal(
            _join_lines(['', '* some_message', '* next message', ''])
        )

        run(['clear', '--yes'])
        result = run(['list'])
        expect(result.output).to_be_equal(_join_lines(['', '']))

    def test_update(self):
        load_fixture('history.rst', 'HISTORY.rst')
        run(['add', 'some_message'])
        run(['add', 'next message'])
        run(['update', '1.0.6', '--date', 'today'])

        content = get_fixture_content('history_after.rst')
        file_content = get_test_file_content('HISTORY.rst')
        expect(content).to_be_equal(file_content)

    def test_update_with_special_headlines(self):
        load_fixture('history_special.rst', 'HISTORY.rst')
        run(['add', 'some_message'])
        run(['add', 'next message'])
        run(['update', '1.0.6', '--date', 'today'])

        content = get_fixture_content('history_special_after.rst')
        file_content = get_test_file_content('HISTORY.rst')
        expect(content).to_be_equal(file_content)

    def test_update_at_line(self):
        load_fixture('history.rst', 'HISTORY.rst')
        run(['add', 'some_message'])
        run(['add', 'next message'])
        run(['update', '1.0.6', '--date', 'today', '--at-line', '1'])

        content = get_fixture_content('history_at_line_after.rst')
        file_content = get_test_file_content('HISTORY.rst')
        expect(content).to_be_equal(file_content)

        load_fixture('history.rst', 'HISTORY.rst')
        run(['add', 'some_message'])
        run(['add', 'next message'])
        run(['update', '1.0.6', '--date', 'today', '--at-line', '0'])

        content = get_fixture_content('history_at_line_after.rst')
        file_content = get_test_file_content('HISTORY.rst')
        expect(content).to_be_equal(file_content)

        load_fixture('history.rst', 'HISTORY.rst')
        run(['add', 'some_message'])
        run(['add', 'next message'])
        run(['update', '1.0.6', '--date', 'today', '--at-line', '7'])

        content = get_fixture_content('history_at_line_after2.rst')
        file_content = get_test_file_content('HISTORY.rst')
        expect(content).to_be_equal(file_content)

    def test_update_with_line_too_long(self):
        load_fixture('history.rst', 'HISTORY.rst')
        run([
            'add', 'some very long and sophisticated message, which is too '
            'long to fit 79 characters'
        ])
        run([
            'add', 'next message, which also is very long, but should fit '
            'into 79 characters aaaa'
        ])
        run([
            'add', 'let just say Lorem ipsum dolor sit amet consectetur '
            'adipisicing elit, sed do eiusmod tempor incididunt ut labore et '
            'dolore magna aliqua. Ut enim ad minim veniam, quis nostrud '
            'exercitation ullamco'
        ])

        run(['update', '1.0.6', '--date', 'today'])

        content = get_fixture_content('history_update_long_line.rst')
        file_content = get_test_file_content('HISTORY.rst')
        expect(content).to_be_equal(file_content)

    def test_list_long_line(self):
        load_fixture('history.rst', 'HISTORY.rst')

        run([
            'add', 'some very long and sophisticated message, which is too '
            'long to fit 79 characters'
        ])

        result = run(['list'])
        expect(result.output).to_be_equal(
            '\n'
            '* some very long and sophisticated message, which is too long to '
            'fit 79\n'
            '  characters\n'
            '\n'
        )

    def test_list_long_line_when_disabled(self):
        load_fixture('history.rst', 'HISTORY.rst')

        run([
            'add', 'some very long and sophisticated message, which is too '
            'long to fit 79 characters'
        ])

        result = run(['list', '--line-length', '0'])
        expect(result.output).to_be_equal(
            '\n'
            '* some very long and sophisticated message, which is too long to '
            'fit 79 characters\n'
            '\n'
        )

    def test_line_length_disabled_when_negative(self):
        load_fixture('history.rst', 'HISTORY.rst')

        run([
            'add', 'some very long and sophisticated message, which is too '
            'long to fit 79 characters'
        ])

        result = run(['list', '--line-length', '0'])
        expect(result.output).to_be_equal(
            '\n'
            '* some very long and sophisticated message, which is too long to '
            'fit 79 characters\n'
            '\n'
        )

    def test_pyhistory_when_not_in_history_file_directory(self):
        load_fixture('history.rst', 'HISTORY.rst')

        original_working_dir = os.getcwd()
        os.makedirs('one/two')
        os.chdir('one/two')

        run(['add', 'some_message'])
        run(['add', 'next message'])

        expect(len(_list_dir_without_dotfiles(os.getcwd()))).to_be_equal(0)

        result = run(['list'])
        expect(result.output).to_be_equal(_join_lines(
            ['', '* some_message', '* next message', ''])
        )

        os.chdir(original_working_dir)
        result = run(['list'])
        expect(result.output).to_be_equal(_join_lines(
            ['', '* some_message', '* next message', ''])
        )

        os.chdir('one/two')
        run(['update', '1.0.6', '--date', 'today'])
        os.chdir(original_working_dir)

        content = get_fixture_content('history_after.rst')
        file_content = get_test_file_content('HISTORY.rst')
        expect(content).to_be_equal(file_content)

    def test_delete(self):
        load_fixture('history.rst', 'HISTORY.rst')

        run(['add', 'some_message'])
        run(['add', 'next message'])

        result = run(['list'])
        expect(result.output).to_be_equal(_join_lines(
            ['', '* some_message', '* next message', ''])
        )

        result = run(['delete'])
        expect(result.output).to_be_equal(_join_lines([
            '', '1. some_message', '2. next message', '',
            '(Delete by choosing entries numbers.)',
        ]))

        run(['delete', '1'])
        result = run(['list'])
        expect(result.output).to_be_equal(
            _join_lines(['', '* next message', ''])
        )

        run(['add', 'test'])
        run(['add', 'test2'])

        result = run(['delete'])
        expect(result.output).to_be_equal(_join_lines([
            '', '1. next message', '2. test', '3. test2', '',
            '(Delete by choosing entries numbers.)',
        ]))

        run(['delete', '10'])
        result = run(['delete'])
        expect(result.output).to_be_equal(_join_lines([
            '', '1. next message', '2. test', '3. test2', '',
            '(Delete by choosing entries numbers.)',
        ]))

        run(['delete', '2', '3', '5', '101'])
        result = run(['list'])
        expect(result.output).to_be_equal(
            _join_lines(['', '* next message', ''])
        )

    def test_delete_long_lines(self):
        load_fixture('history.rst', 'HISTORY.rst')

        run([
            'add', 'some very long and sophisticated message, which is too '
            'long to fit 79 characters'
        ])
        messages = [
            'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
        ]
        for message in messages:
            run(['add', message])
        run([
            'add', 'next message, which also is very long, and should not '
            'fit into 79 characters'
        ])

        result = run(['delete'])
        expect(result.output).to_be_equal(
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


class TestUtilities(object):

    def test_split_simple_case(self):
        expect(split_into_lines('text', 10)).to_be_equal(['text'])

    def test_split_empty_string(self):
        expect(split_into_lines('', 10)).to_be_equal([''])

    def test_split_negative_line_length(self):
        split = split_into_lines
        expect(split('cha cha cha', -1)).to_be_equal(['cha cha cha'])

    def test_split_zero_line_length(self):
        expect(split_into_lines('cha cha cha', 0)).to_be_equal(['cha cha cha'])

    def test_split_line(self):
        split = split_into_lines
        expect(split('cha cha cha', 1)).to_be_equal(['cha', 'cha', 'cha'])
        expect(split('cha cha cha', 2)).to_be_equal(['cha', 'cha', 'cha'])
        expect(split('cha cha cha', 3)).to_be_equal(['cha', 'cha', 'cha'])
        expect(split('cha cha cha', 6)).to_be_equal(['cha', 'cha', 'cha'])
        expect(split('cha cha cha', 7)).to_be_equal(['cha cha', 'cha'])

    def test_split_with_words_too_long(self):
        expect(split_into_lines('aaaaaaaaa bbb ccc', 4)).to_be_equal(
            ['aaaaaaaaa', 'bbb', 'ccc']
        )
        expect(split_into_lines('bbb ccc aaaaaaaaa ddd', 4)).to_be_equal(
            ['bbb', 'ccc', 'aaaaaaaaa', 'ddd']
        )

    def test_split_line_with_line_feed_at_the_end(self):
        expect(split_into_lines('cha cha\n', 6)).to_be_equal(['cha', 'cha\n'])
        expect(split_into_lines('cha cha\n', 7)).to_be_equal(['cha cha\n'])


def _join_lines(output):
    return '\n'.join(output) + '\n'
