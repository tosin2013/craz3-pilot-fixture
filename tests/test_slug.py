"""Tests for slugify and its exported constants."""

import pytest
from slugkit import slugify
from slugkit.slug import SEPARATOR, SLUG_MAX, EMPTY_SLUG


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

def test_separator_value():
    assert SEPARATOR == "~"


def test_slug_max_value():
    assert SLUG_MAX == 37


def test_empty_slug_value():
    assert EMPTY_SLUG == "n~a"


# ---------------------------------------------------------------------------
# Basic behaviour
# ---------------------------------------------------------------------------

def test_lowercase():
    assert slugify("Hello") == "hello"


def test_all_uppercase():
    assert slugify("HELLO WORLD") == "hello~world"


def test_simple_words():
    assert slugify("hello world") == "hello~world"


def test_tilde_separator_not_hyphen():
    result = slugify("foo bar")
    assert "~" in result
    assert "-" not in result


def test_run_of_separators_becomes_one():
    # Multiple non-alphanumeric characters → single separator
    assert slugify("foo   bar") == "foo~bar"
    assert slugify("foo!@#bar") == "foo~bar"


def test_leading_separator_removed():
    assert slugify("  hello") == "hello"
    assert slugify("!!!hello") == "hello"


def test_trailing_separator_removed():
    assert slugify("hello  ") == "hello"
    assert slugify("hello!!!") == "hello"


def test_leading_and_trailing_removed():
    assert slugify("  hello world  ") == "hello~world"


def test_digits_preserved():
    assert slugify("abc 123") == "abc~123"


def test_mixed_chars():
    assert slugify("Héllo") == "h~llo"


# ---------------------------------------------------------------------------
# Truncation to SLUG_MAX
# ---------------------------------------------------------------------------

def test_short_slug_not_truncated():
    text = "a" * SLUG_MAX
    assert slugify(text) == text


def test_long_slug_truncated_to_max():
    text = "a" * (SLUG_MAX + 10)
    result = slugify(text)
    assert len(result) <= SLUG_MAX


def test_truncation_removes_trailing_tilde():
    # Construct a slug that would end with ~ after truncation.
    # "a" * 36 + "~" + "b" is 38 chars before truncation.
    # Cutting to 37 gives "aaa...a~" → trailing ~ must be stripped.
    text = "a" * 36 + " " + "b" * 10
    result = slugify(text)
    assert len(result) <= SLUG_MAX
    assert not result.endswith(SEPARATOR)


def test_exactly_max_length_no_tilde():
    text = "a" * SLUG_MAX
    assert slugify(text) == "a" * SLUG_MAX


# ---------------------------------------------------------------------------
# Empty result → EMPTY_SLUG
# ---------------------------------------------------------------------------

def test_empty_string_returns_empty_slug():
    assert slugify("") == EMPTY_SLUG


def test_only_separators_returns_empty_slug():
    assert slugify("   ") == EMPTY_SLUG
    assert slugify("!!!") == EMPTY_SLUG


def test_empty_slug_literal():
    assert EMPTY_SLUG == "n~a"


# ---------------------------------------------------------------------------
# Export from top-level package
# ---------------------------------------------------------------------------

def test_importable_from_slugkit():
    from slugkit import slugify as sf
    assert callable(sf)
