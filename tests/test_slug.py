"""Tests for slugkit.slugify covering every rule in spec 001."""

import pytest
from slugkit import slugify, SEPARATOR, SLUG_MAX, EMPTY_SLUG


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
# Rule 1: lowercasing
# ---------------------------------------------------------------------------

def test_lowercase_basic():
    assert slugify("Hello") == "hello"


def test_lowercase_mixed():
    assert slugify("FooBAR") == "foobar"


# ---------------------------------------------------------------------------
# Rule 2: separator replacement
# ---------------------------------------------------------------------------

def test_space_becomes_separator():
    assert slugify("hello world") == "hello~world"


def test_hyphen_becomes_separator():
    assert slugify("foo-bar") == "foo~bar"


def test_run_of_separators_collapsed():
    assert slugify("foo   ---   bar") == "foo~bar"


def test_non_ascii_char_becomes_separator():
    # Non-ASCII characters are not ASCII letters/digits, so they become separators.
    # A trailing separator is stripped, so "café" -> "caf~" -> "caf".
    result = slugify("café")
    assert result == "caf"

    # ö in the middle becomes a separator between w and rld
    result = slugify("hello wörld")
    assert result == "hello~w~rld"


def test_punctuation_becomes_separator():
    assert slugify("hello, world!") == "hello~world"


def test_digits_preserved():
    assert slugify("abc123") == "abc123"


def test_mixed_separators_collapsed():
    assert slugify("a!@#b") == "a~b"


# ---------------------------------------------------------------------------
# Rule 3: strip leading/trailing separators
# ---------------------------------------------------------------------------

def test_leading_separator_stripped():
    assert slugify("  hello") == "hello"


def test_trailing_separator_stripped():
    assert slugify("hello  ") == "hello"


def test_both_ends_stripped():
    assert slugify("  hello world  ") == "hello~world"


def test_leading_non_alnum_stripped():
    assert slugify("---hello") == "hello"


# ---------------------------------------------------------------------------
# Rule 4: SLUG_MAX truncation
# ---------------------------------------------------------------------------

def test_exactly_max_length_unchanged():
    text = "a" * SLUG_MAX
    assert slugify(text) == text


def test_over_max_truncated():
    text = "a" * (SLUG_MAX + 10)
    result = slugify(text)
    assert len(result) <= SLUG_MAX


def test_truncation_removes_trailing_tilde():
    # Construct a string that would place a ~ exactly at position SLUG_MAX
    # e.g. 36 'a's + separator + more content -> cut lands on the ~
    part = "a" * (SLUG_MAX - 1) + " extra words"
    result = slugify(part)
    assert not result.endswith(SEPARATOR)
    assert len(result) <= SLUG_MAX


def test_truncation_at_tilde_boundary():
    # 36 a's then a space then more a's: after slugify the ~ lands at index 36
    base = "a" * 36 + " " + "b" * 10
    result = slugify(base)
    assert len(result) <= SLUG_MAX
    assert not result.endswith(SEPARATOR)


# ---------------------------------------------------------------------------
# Rule 5: empty result returns EMPTY_SLUG
# ---------------------------------------------------------------------------

def test_empty_string_returns_empty_slug():
    assert slugify("") == EMPTY_SLUG


def test_only_separators_returns_empty_slug():
    assert slugify("   ") == EMPTY_SLUG


def test_only_non_alnum_returns_empty_slug():
    assert slugify("!@#$%") == EMPTY_SLUG


# ---------------------------------------------------------------------------
# Integration / typical usage
# ---------------------------------------------------------------------------

def test_typical_title():
    assert slugify("Hello, World!") == "hello~world"


def test_url_like():
    assert slugify("My Blog Post Title 2024") == "my~blog~post~title~2024"


def test_import_from_package():
    from slugkit import slugify as sf
    assert sf("Test") == "test"
