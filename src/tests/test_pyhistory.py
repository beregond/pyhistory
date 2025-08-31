from pyhistory.pyhistory import add, clear, list_

from . import isolated_env


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
