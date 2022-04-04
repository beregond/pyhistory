import pytest
from verify import expect

from pyhistory.pyhistory import add, clear, delete, list_, update

from . import get_fixture_content, isolated_env, load_fixture_to


@isolated_env
def test_list_empty(history_dir, history_file):
    expect(list_(history_dir)).to_be_equal({})


@isolated_env
def test_add_list_and_clear(history_dir, history_file):
    add("some_message", history_dir)
    expect(list_(history_dir)).to_be_equal({1: "some_message\n"})

    add("next message", history_dir)

    expect(list_(history_dir)).to_be_equal(
        {1: "some_message\n", 2: "next message\n"}
    )

    clear(history_dir)
    expect(list_(history_dir)).to_be_equal({})


@isolated_env
def test_update(history_dir, history_file):
    load_fixture_to("history.rst", history_file)
    add("some_message", history_dir)
    add("next message", history_dir)
    update("1.0.6", history_dir, history_file, date="today", prefix="* ")

    content = get_fixture_content("history_after.rst")
    with history_file.open() as src:
        file_content = src.read()
    expect(content).to_be_equal(file_content)


@isolated_env
def test_update_empty_file(history_dir, history_file):
    load_fixture_to("empty.txt", history_file)
    add("some_message", history_dir)
    add("next message", history_dir)
    update("1.0.6", history_dir, history_file, date="today", prefix="* ")

    content = get_fixture_content("empty_after.rst")
    with history_file.open() as src:
        file_content = src.read()
    expect(content.rstrip("\n")).to_be_equal(file_content.rstrip("\n"))


@isolated_env
def test_update_with_special_headlines(history_dir, history_file):
    load_fixture_to("history_special.rst", history_file)
    add("some_message", history_dir)
    add("next message", history_dir)
    update("1.0.6", history_dir, history_file, date="today", prefix="* ")

    content = get_fixture_content("history_special_after.rst")
    with history_file.open() as src:
        file_content = src.read()
    expect(content).to_be_equal(file_content)


@pytest.mark.parametrize(
    ["at_line", "fixture_name"],
    [
        (1, "history_at_line_after.rst"),
        (0, "history_at_line_after.rst"),
        (7, "history_at_line_after2.rst"),
    ],
)
def test_update_at_line(at_line, fixture_name):
    _test_update_at_line(at_line=at_line, fixture_name=fixture_name)


@isolated_env
def _test_update_at_line(history_dir, history_file, at_line, fixture_name):
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
    expect(content).to_be_equal(file_content)


@isolated_env
def test_update_with_line_too_long(history_dir, history_file):
    load_fixture_to("history.rst", history_file)
    add(
        "some very long and sophisticated message, which is too long to fit 79"
        " characters",
        history_dir,
    )
    add(
        "next message, which also is very long, but should fit into 79"
        " characters aaaa",
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
    expect(content).to_be_equal(file_content)


@isolated_env
def test_delete(history_dir, history_file):
    load_fixture_to("history.rst", history_file)

    add("some_message", history_dir)
    add("next message", history_dir)

    expect(list_(history_dir)).to_be_equal(
        {1: "some_message\n", 2: "next message\n"}
    )

    delete([1], history_dir)
    expect(list_(history_dir)).to_be_equal({1: "next message\n"})

    add("test", history_dir)
    add("test2", history_dir)

    expected_output = {1: "next message\n", 2: "test\n", 3: "test2\n"}
    expect(list_(history_dir)).to_be_equal(expected_output)
    delete([10], history_dir)
    expect(list_(history_dir)).to_be_equal(expected_output)

    delete([2, 3, 5, 101], history_dir)
    expect(list_(history_dir)).to_be_equal({1: "next message\n"})
