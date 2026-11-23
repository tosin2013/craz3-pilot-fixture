"""Tests for the slugify function (spec 001)."""

from slugkit import slugify
from slugkit.slug import EMPTY_SLUG, SEPARATOR, SLUG_MAX


def test_constants():
    assert SEPARATOR == "~"
    assert SLUG_MAX == 37
    assert EMPTY_SLUG == "n~a"


def test_lowercases():
    assert slugify("Hello WORLD") == "hello~world"


def test_non_alnum_run_becomes_single_separator():
    assert slugify("Hello,  World!") == "hello~world"


def test_strips_leading_and_trailing_separators():
    assert slugify("  Hello World  ") == "hello~world"
    assert slugify("!!Hello!!") == "hello"


def test_non_ascii_letters_are_separators():
    assert slugify("héllo") == "h~llo"


def test_empty_input_returns_empty_slug():
    assert slugify("") == EMPTY_SLUG


def test_only_separators_returns_empty_slug():
    assert slugify("!!!   ???") == EMPTY_SLUG


def test_truncates_to_slug_max():
    assert slugify("a" * 40) == "a" * SLUG_MAX


def test_truncation_removes_trailing_separator():
    # 36 'a' characters, a separator, then 'b': cut to 37 leaves a trailing '~'.
    assert slugify("a" * 36 + " b") == "a" * 36


def test_result_has_no_trailing_separator():
    assert not slugify("hello world").endswith(SEPARATOR)
