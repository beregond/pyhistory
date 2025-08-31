import os

from click.testing import CliRunner

from pyhistory.cli import main

from . import (
    get_fixture_content,
    get_test_file_content,
    isolated_env,
    isolated_workdir,
    load_fixture,
)


def test_add_list_delete_and_clear():
    with isolated_env():
        open("HISTORY.rst", "w").close()

        result = _run(["list"])
        assert result.output == _join_lines(["", ""])

        _run(["add", "some_message"])
        result = _run(["list"])
        assert result.output == _join_lines(["", "* some_message", ""])
        _run(["add", "next message"])
        result = _run(["list"])
        assert result.output == _join_lines(
            ["", "* some_message", "* next message", ""]
        )

        result = _run(["delete"])
        assert result.output == _join_lines(
            [
                "",
                "1. some_message",
                "2. next message",
                "",
                "(Delete by choosing entries numbers.)",
            ]
        )

        _run(["delete", "1"])
        result = _run(["list"])
        assert result.output == _join_lines(["", "* next message", ""])

        _run(["add", "some_message"])
        _run(["clear", "--yes"])
        result = _run(["list"])
        assert result.output == _join_lines(["", ""])


def test_update():
    with isolated_env():
        load_fixture("history.rst", "HISTORY.rst")
        _run(["add", "some_message"])
        _run(["add", "next message"])
        _run(["update", "1.0.6", "--date", "today"])

        content = get_fixture_content("history_after.rst")
        file_content = get_test_file_content("HISTORY.rst")
        assert content == file_content


def test_update_with_special_headlines():
    with isolated_env():
        load_fixture("history_special.rst", "HISTORY.rst")
        _run(["add", "some_message"])
        _run(["add", "next message"])
        _run(["update", "1.0.6", "--date", "today"])

        content = get_fixture_content("history_special_after.rst")
        file_content = get_test_file_content("HISTORY.rst")
        assert content == file_content


def test_update_at_line():
    with isolated_env():
        load_fixture("history.rst", "HISTORY.rst")
        _run(["add", "some_message"])
        _run(["add", "next message"])
        _run(["update", "1.0.6", "--date", "today", "--at-line", "1"])

        content = get_fixture_content("history_at_line_after.rst")
        file_content = get_test_file_content("HISTORY.rst")
        assert content == file_content


def test_update_at_wrong_line():
    with isolated_env():
        load_fixture("history.rst", "HISTORY.rst")
        res = _run(["update", "1.0.6", "--date", "today", "--at-line", "0"])
        assert res.exit_code == 1
        assert res.output == '"at_line" must be greater or equal to 1.\nAborted!\n'


def test_update_at_negative_line():
    with isolated_env():
        load_fixture("history.rst", "HISTORY.rst")
        result = _run(["update", "1.0.6", "--date", "today", "--at-line", "-1"])
        assert result.exit_code == 1


def test_update_with_line_too_long():
    with isolated_env():
        load_fixture("history.rst", "HISTORY.rst")
        _run(
            [
                "add",
                "some very long and sophisticated message, which is too "
                "long to fit 79 characters",
            ]
        )
        _run(
            [
                "add",
                "next message, which also is very long, but should fit "
                "into 79 characters aaaa",
            ]
        )
        _run(
            [
                "add",
                "let just say Lorem ipsum dolor sit amet consectetur "
                "adipisicing elit, sed do eiusmod tempor incididunt ut labore et "
                "dolore magna aliqua. Ut enim ad minim veniam, quis nostrud "
                "exercitation ullamco",
            ]
        )

        _run(["update", "1.0.6", "--date", "today"])

        content = get_fixture_content("history_update_long_line.rst")
        file_content = get_test_file_content("HISTORY.rst")
        assert content == file_content


def test_list_long_line():
    with isolated_env():
        load_fixture("history.rst", "HISTORY.rst")

        result = _run(
            [
                "add",
                "some very long and sophisticated message, which is too "
                "long to fit 79 characters",
            ]
        )

        result = _run(["list"])
        assert result.output == (
            "\n"
            "* some very long and sophisticated message, which is too long to "
            "fit 79\n"
            "  characters\n"
            "\n"
        )


def test_pyhistory_when_not_in_history_file_directory():
    with isolated_env():
        load_fixture("history.rst", "HISTORY.rst")

        original_working_dir = os.getcwd()
        os.makedirs("one/two")
        os.chdir("one/two")

        _run(["add", "some_message"])
        _run(["add", "next message"])

        assert len(os.listdir(os.getcwd())) == 0

        result = _run(["list"])
        assert result.output == _join_lines(
            ["", "* some_message", "* next message", ""]
        )

        os.chdir(original_working_dir)
        result = _run(["list"])
        assert result.output == _join_lines(
            ["", "* some_message", "* next message", ""]
        )

        os.chdir("one/two")
        _run(["update", "1.0.6", "--date", "today"])
        os.chdir(original_working_dir)

        content = get_fixture_content("history_after.rst")
        file_content = get_test_file_content("HISTORY.rst")
        assert content == file_content


def test_delete_long_lines():
    with isolated_env():
        load_fixture("history.rst", "HISTORY.rst")

        _run(
            [
                "add",
                "some very long and sophisticated message, which is too "
                "long to fit 79 characters",
            ]
        )
        messages = [
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
        ]
        for message in messages:
            _run(["add", message])
        _run(
            [
                "add",
                "next message, which also is very long, and should not "
                "fit into 79 characters",
            ]
        )

        result = _run(["delete"])
        assert result.output == (
            "\n"
            "1. some very long and sophisticated message, which is too long "
            "to fit 79\n"
            "   characters\n"
            "2. two\n"
            "3. three\n"
            "4. four\n"
            "5. five\n"
            "6. six\n"
            "7. seven\n"
            "8. eight\n"
            "9. nine\n"
            "10. next message, which also is very long, and should not fit "
            "into 79\n"
            "    characters\n"
            "\n"
            "(Delete by choosing entries numbers.)\n"
        )


def test_delete_in_non_root():
    with isolated_env():
        os.makedirs("one/two")
        os.chdir("one")
        test_delete_long_lines()


def test_history_file_not_found():
    with isolated_env():
        result = _run(["update", "1.0.6", "--date", "today"])
        assert result.exit_code == 1


def _join_lines(output):
    return "\n".join(output) + "\n"


def _run(command):
    runner = CliRunner()
    return runner.invoke(main, command)
