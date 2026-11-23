"""Tests for every rule in spec 001 (slug function)."""

from slugkit import slugify
from slugkit import slug


def test_constants():
    assert slug.SEPARATOR == "~"
    assert slug.SLUG_MAX == 37
    assert slug.EMPTY_SLUG == "n~a"


def test_lowercases_input():
    assert slugify("Hello World") == "hello~world"
    assert slugify("ABC") == "abc"


def test_separator_is_tilde_not_dash():
    assert slugify("hello-world") == "hello~world"
    assert "~" in slugify("a b")


def test_runs_of_non_alnum_collapse_to_one_separator():
    assert slugify("a   b") == "a~b"
    assert slugify("a---b") == "a~b"
    assert slugify("a?!_b") == "a~b"
    assert slugify("a\t\nb") == "a~b"


def test_leading_and_trailing_separators_removed():
    assert slugify("  hello  ") == "hello"
    assert slugify("~hello~") == "hello"
    assert slugify("---hello---") == "hello"


def test_non_ascii_letters_are_separators():
    assert slugify("café") == "caf"


def test_digits_are_kept():
    assert slugify("room 101") == "room~101"
    assert slugify("a1b2") == "a1b2"


def test_truncates_to_slug_max():
    long = "a" * 100
    result = slugify(long)
    assert len(result) == slug.SLUG_MAX


def test_truncation_strips_trailing_separator():
    # 36 letters, then a separator, then more content: truncation leaves a
    # trailing "~" that must be removed.
    text = "a" * 36 + " " + "b"
    assert slugify(text) == "a" * 36


def test_exactly_slug_max_is_unchanged():
    assert slugify("a" * slug.SLUG_MAX) == "a" * slug.SLUG_MAX


def test_empty_input_returns_empty_slug():
    assert slugify("") == slug.EMPTY_SLUG == "n~a"


def test_all_separators_returns_empty_slug():
    assert slugify("   ") == "n~a"
    assert slugify("~~~") == "n~a"
    assert slugify("?!") == "n~a"
