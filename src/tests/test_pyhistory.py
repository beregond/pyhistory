import pytest

from pyhistory.pyhistory import add, clear, delete, list_, update

from . import get_fixture_content, load_fixture_to, isolated_env


def test_list_empty():
    with isolated_env() as temp_dir:
        history_dir = temp_dir / "history"
        assert list_(history_dir) == {}


def test_add_list_and_clear():
    with isolated_env() as temp_dir:
        history_dir = temp_dir / "history"
        add("some_message", history_dir)
        assert list_(history_dir) == {1: "some_message\n"}

        add("next message", history_dir)

        assert list_(history_dir) == {1: "some_message\n", 2: "next message\n"}

        clear(history_dir)
        assert list_(history_dir) == {}


def test_update():
    with isolated_env() as temp_dir:
        history_dir = temp_dir / "history"
        history_file = temp_dir / "HISTORY.rst"
        load_fixture_to("history.rst", history_file)
        add("some_message", history_dir)
        add("next message", history_dir)
        update("1.0.6", history_dir, history_file, date="today", prefix="* ")

        content = get_fixture_content("history_after.rst")
        with history_file.open() as src:
            file_content = src.read()
        assert content == file_content


def test_update_empty_file():
    with isolated_env() as temp_dir:
        history_dir = temp_dir / "history"
        history_file = temp_dir / "HISTORY.rst"
        load_fixture_to("empty.txt", history_file)
        add("some_message", history_dir)
        add("next message", history_dir)
        update("1.0.6", history_dir, history_file, date="today", prefix="* ")

        content = get_fixture_content("empty_after.rst")
        with history_file.open() as src:
            file_content = src.read()
        assert content.rstrip("\n") == file_content.rstrip("\n")


def test_update_with_special_headlines():
    with isolated_env() as temp_dir:
        history_dir = temp_dir / "history"
        history_file = temp_dir / "HISTORY.rst"
        load_fixture_to("history_special.rst", history_file)
        add("some_message", history_dir)
        add("next message", history_dir)
        update("1.0.6", history_dir, history_file, date="today", prefix="* ")

        content = get_fixture_content("history_special_after.rst")
        with history_file.open() as src:
            file_content = src.read()
        assert content == file_content


@pytest.mark.parametrize(
    ["at_line", "fixture_name"],
    [
        (1, "history_at_line_after.rst"),
        (0, "history_at_line_after.rst"),
        (7, "history_at_line_after2.rst"),
    ],
)
def test_update_at_line(at_line, fixture_name):
    _test_update_at_line(at_line, fixture_name)


def _test_update_at_line(at_line, fixture_name):
    with isolated_env() as temp_dir:
        history_dir = temp_dir / "history"
        history_file = temp_dir / "HISTORY.rst"
        load_fixture_to("history.rst", history_file)
        add("some_message", history_dir)
        add("next message", history_dir)
        update(
            "1.0.6",
            history_dir,
            history_file,
            date="today",
            at_line=at_line,
            prefix="* ",
        )

        content = get_fixture_content(fixture_name)
        with history_file.open() as src:
            file_content = src.read()
        assert content == file_content


def test_update_with_line_too_long():
    with isolated_env() as temp_dir:
        history_dir = temp_dir / "history"
        history_file = temp_dir / "HISTORY.rst"
        load_fixture_to("history.rst", history_file)
        add(
            "some very long and sophisticated message, which is too long to fit 79"
            " characters",
            history_dir,
        )
        add(
            "next message, which also is very long, but should fit into 79 characters aaaa",
            history_dir,
        )
        add(
            "let just say Lorem ipsum dolor sit amet consectetur "
            "adipisicing elit, sed do eiusmod tempor incididunt ut labore et "
            "dolore magna aliqua. Ut enim ad minim veniam, quis nostrud "
            "exercitation ullamco",
            history_dir,
        )

        update(
            "1.0.6",
            history_dir,
            history_file,
            date="today",
            prefix="* ",
            line_length=79,
        )

        content = get_fixture_content("history_update_long_line.rst")
        with history_file.open() as src:
            file_content = src.read()
        assert content == file_content


def test_delete():
    with isolated_env() as temp_dir:
        history_dir = temp_dir / "history"
        history_file = temp_dir / "HISTORY.rst"
        load_fixture_to("history.rst", history_file)

        add("some_message", history_dir)
        add("next message", history_dir)

        assert list_(history_dir) == {1: "some_message\n", 2: "next message\n"}

        delete([1], history_dir)
        assert list_(history_dir) == {1: "next message\n"}

        add("test", history_dir)
        add("test2", history_dir)

        expected_output = {1: "next message\n", 2: "test\n", 3: "test2\n"}
        assert list_(history_dir) == expected_output
        delete([10], history_dir)
        assert list_(history_dir) == expected_output

        delete([2, 3, 5, 101], history_dir)
        assert list_(history_dir) == {1: "next message\n"}
