"""Tests for the slugify function and its constants."""

from slugkit import slugify
from slugkit.slug import EMPTY_SLUG, SEPARATOR, SLUG_MAX


def test_constants():
    assert SEPARATOR == "~"
    assert SLUG_MAX == 37
    assert EMPTY_SLUG == "n~a"


def test_lowercases_input():
    assert slugify("Hello World") == "hello~world"


def test_replaces_non_alnum_runs_with_separator():
    assert slugify("a  b") == "a~b"
    assert slugify("a---b") == "a~b"
    assert slugify("a!@#b") == "a~b"


def test_separator_is_tilde_not_dash():
    assert slugify("a b") == "a~b"
    assert "~" in slugify("a b")
    assert "-" not in slugify("a b")


def test_strips_leading_and_trailing_separators():
    assert slugify("  hello  ") == "hello"
    assert slugify("---hello---") == "hello"
    assert slugify("~hello~") == "hello"


def test_keeps_ascii_letters_and_digits():
    assert slugify("abc123") == "abc123"


def test_truncates_to_slug_max_and_strips_trailing_separator():
    long_text = "a" * 40 + " " + "b" * 40
    slug = slugify(long_text)
    assert len(slug) <= SLUG_MAX
    assert not slug.endswith(SEPARATOR)


def test_truncation_at_boundary():
    # A slug exactly at SLUG_MAX is unchanged.
    text = "a" * SLUG_MAX
    assert slugify(text) == "a" * SLUG_MAX


def test_empty_input_returns_empty_slug():
    assert slugify("") == EMPTY_SLUG
    assert slugify("   ") == EMPTY_SLUG
    assert slugify("!@#$%^&*()") == EMPTY_SLUG
