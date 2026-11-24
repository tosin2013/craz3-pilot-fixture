"""Tests for every rule in spec 001 (Slug function)."""

from slugkit import slugify
from slugkit.slug import EMPTY_SLUG, SEPARATOR, SLUG_MAX


def test_lowercases_input():
    assert slugify("HELLO") == "hello"
    assert slugify("Hello World") == "hello~world"


def test_non_ascii_letters_or_digits_become_separator():
    # A single run of non-alphanumeric characters collapses to one separator.
    assert slugify("hello world") == "hello~world"
    assert slugify("hello   world") == "hello~world"
    assert slugify("hello_world") == "hello~world"
    assert slugify("hello---world") == "hello~world"


def test_ascii_letters_and_digits_are_preserved():
    assert slugify("abc123") == "abc123"


def test_non_ascii_characters_become_separator():
    assert slugify("h\u00e9llo") == "h~llo"


def test_strips_separators_at_start_and_end():
    assert slugify("~~hello~~") == "hello"
    assert slugify("  Hello World  ") == "hello~world"
    assert slugify("...hello...") == "hello"


def test_separator_constant_is_tilde():
    assert SEPARATOR == "~"


def test_truncates_when_longer_than_slug_max():
    assert SLUG_MAX == 37
    assert slugify("a" * 40) == "a" * SLUG_MAX
    # A cut that lands on a separator leaves no trailing separator.
    assert slugify("a" * 36 + "!" + "b") == "a" * 36


def test_empty_result_returns_empty_slug():
    assert EMPTY_SLUG == "n~a"
    assert slugify("") == EMPTY_SLUG
    assert slugify("~~~") == EMPTY_SLUG
    assert slugify("   ") == EMPTY_SLUG
