import pytest

from pyhistory.pyhistory import add, delete, list_, update

from . import get_fixture_content, load_fixture_to, isolated_env


def test_update_md():
    with isolated_env() as temp_dir:
        history_dir = temp_dir / "history"
        history_file = temp_dir / "history.md"
        load_fixture_to("history.md", history_file)
        add("some_message", history_dir)
        add("next message", history_dir)
        update("1.0.6", history_dir, history_file, date="today", prefix="* ")

        content = get_fixture_content("history_after.md")
        with history_file.open() as src:
            file_content = src.read()
        assert content == file_content


def test_update_empty_file():
    with isolated_env() as temp_dir:
        history_dir = temp_dir / "history"
        history_file = temp_dir / "history.md"
        load_fixture_to("empty.txt", history_file)
        add("some_message", history_dir)
        add("next message", history_dir)
        update("1.0.6", history_dir, history_file, date="today", prefix="* ")

        content = get_fixture_content("empty_after.md")
        with history_file.open() as src:
            file_content = src.read()
        assert content.rstrip("\n") == file_content.rstrip("\n")


def test_update_with_special_headlines():
    with isolated_env() as temp_dir:
        history_dir = temp_dir / "history"
        history_file = temp_dir / "history.md"
        load_fixture_to("history_special.md", history_file)
        add("some_message", history_dir)
        add("next message", history_dir)
        update("1.0.6", history_dir, history_file, date="today", prefix="* ")

        content = get_fixture_content("history_special_after.md")
        with history_file.open() as src:
            file_content = src.read()
        assert content == file_content


@pytest.mark.parametrize(
    ["at_line", "fixture_name"],
    [
        (1, "history_at_line_after.md"),
        (0, "history_at_line_after.md"),
        (5, "history_at_line_after2.md"),
    ],
)
def test_update_at_line(at_line, fixture_name):
    _test_update_at_line(at_line, fixture_name)


def _test_update_at_line(at_line, fixture_name):
    with isolated_env() as temp_dir:
        history_dir = temp_dir / "history"
        history_file = temp_dir / "history.md"
        load_fixture_to("history.md", history_file)
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


def test_delete():
    with isolated_env() as temp_dir:
        history_dir = temp_dir / "history"
        history_file = temp_dir / "history.md"
        load_fixture_to("history.md", history_file)

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
