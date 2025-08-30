from pyhistory.utilities import split_into_lines


def test_split_simple_case():
    assert split_into_lines("text", 10) == ["text"]


def test_split_empty_string():
    assert split_into_lines("", 10) == [""]


def test_split_negative_line_length():
    split = split_into_lines
    assert split("cha cha cha", -1) == ["cha cha cha"]


def test_split_zero_line_length():
    assert split_into_lines("cha cha cha", 0) == ["cha cha cha"]


def test_split_line():
    split = split_into_lines
    assert split("cha cha cha", 1) == ["cha", "cha", "cha"]
    assert split("cha cha cha", 2) == ["cha", "cha", "cha"]
    assert split("cha cha cha", 3) == ["cha", "cha", "cha"]
    assert split("cha cha cha", 6) == ["cha", "cha", "cha"]
    assert split("cha cha cha", 7) == ["cha cha", "cha"]


def test_split_with_words_too_long():
    assert split_into_lines("aaaaaaaaa bbb ccc", 4) == ["aaaaaaaaa", "bbb", "ccc"]
    assert split_into_lines("bbb ccc aaaaaaaaa ddd", 4) == [
        "bbb",
        "ccc",
        "aaaaaaaaa",
        "ddd",
    ]


def test_split_line_with_line_feed_at_the_end():
    assert split_into_lines("cha cha\n", 6) == ["cha", "cha\n"]
    assert split_into_lines("cha cha\n", 7) == ["cha cha\n"]
