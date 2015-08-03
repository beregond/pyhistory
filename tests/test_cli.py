import os

from verify import expect
from click.testing import CliRunner

from pyhistory.cli import main
from . import (
    load_fixture, get_fixture_content, get_test_file_content, isolated_workdir,
)


def run(command):
    runner = CliRunner()
    return runner.invoke(main, command)


@isolated_workdir
def test_list_empty():
    open('HISTORY.rst', 'w').close()
    result = run(['list'])
    expect(result.output).to_be_equal(_join_lines(['', '']))


@isolated_workdir
def test_add_list_and_clear():
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


@isolated_workdir
def test_update():
    load_fixture('history.rst', 'HISTORY.rst')
    run(['add', 'some_message'])
    run(['add', 'next message'])
    run(['update', '1.0.6', '--date', 'today'])

    content = get_fixture_content('history_after.rst')
    file_content = get_test_file_content('HISTORY.rst')
    expect(content).to_be_equal(file_content)


@isolated_workdir
def test_update_with_special_headlines():
    load_fixture('history_special.rst', 'HISTORY.rst')
    run(['add', 'some_message'])
    run(['add', 'next message'])
    run(['update', '1.0.6', '--date', 'today'])

    content = get_fixture_content('history_special_after.rst')
    file_content = get_test_file_content('HISTORY.rst')
    expect(content).to_be_equal(file_content)


@isolated_workdir
def test_update_at_line():
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


@isolated_workdir
def test_update_with_line_too_long():
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


@isolated_workdir
def test_list_long_line():
    load_fixture('history.rst', 'HISTORY.rst')

    result = run([
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


@isolated_workdir
def test_list_long_line_when_disabled():
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


@isolated_workdir
def test_line_length_disabled_when_negative():
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


@isolated_workdir
def test_pyhistory_when_not_in_history_file_directory():
    load_fixture('history.rst', 'HISTORY.rst')

    original_working_dir = os.getcwd()
    os.makedirs('one/two')
    os.chdir('one/two')

    run(['add', 'some_message'])
    run(['add', 'next message'])

    expect(len(os.listdir(os.getcwd()))).to_be_equal(0)

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


@isolated_workdir
def test_delete():
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


@isolated_workdir
def test_delete_long_lines():
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


@isolated_workdir
def test_delete_in_non_root():
    os.makedirs('one/two')
    os.chdir('one')
    test_delete()


def _join_lines(output):
    return '\n'.join(output) + '\n'
