from verify import expect

from pyhistory.utilities import split_into_lines


def test_split_simple_case():
    expect(split_into_lines("text", 10)).to_be_equal(["text"])


def test_split_empty_string():
    expect(split_into_lines("", 10)).to_be_equal([""])


def test_split_negative_line_length():
    split = split_into_lines
    expect(split("cha cha cha", -1)).to_be_equal(["cha cha cha"])


def test_split_zero_line_length():
    expect(split_into_lines("cha cha cha", 0)).to_be_equal(["cha cha cha"])


def test_split_line():
    split = split_into_lines
    expect(split("cha cha cha", 1)).to_be_equal(["cha", "cha", "cha"])
    expect(split("cha cha cha", 2)).to_be_equal(["cha", "cha", "cha"])
    expect(split("cha cha cha", 3)).to_be_equal(["cha", "cha", "cha"])
    expect(split("cha cha cha", 6)).to_be_equal(["cha", "cha", "cha"])
    expect(split("cha cha cha", 7)).to_be_equal(["cha cha", "cha"])


def test_split_with_words_too_long():
    expect(split_into_lines("aaaaaaaaa bbb ccc", 4)).to_be_equal(
        ["aaaaaaaaa", "bbb", "ccc"]
    )
    expect(split_into_lines("bbb ccc aaaaaaaaa ddd", 4)).to_be_equal(
        ["bbb", "ccc", "aaaaaaaaa", "ddd"]
    )


def test_split_line_with_line_feed_at_the_end():
    expect(split_into_lines("cha cha\n", 6)).to_be_equal(["cha", "cha\n"])
    expect(split_into_lines("cha cha\n", 7)).to_be_equal(["cha cha\n"])
