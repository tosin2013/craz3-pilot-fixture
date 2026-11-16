"""Tests for slugify and its exported constants (spec 001)."""

import pytest
from slugkit import slugify, SEPARATOR, SLUG_MAX, EMPTY_SLUG


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

def test_separator_is_tilde():
    assert SEPARATOR == "~"


def test_slug_max_is_37():
    assert SLUG_MAX == 37


def test_empty_slug_value():
    assert EMPTY_SLUG == "n~a"


# ---------------------------------------------------------------------------
# Rule 1: lowercase
# ---------------------------------------------------------------------------

def test_lowercases_ascii():
    assert slugify("HELLO") == "hello"


def test_lowercases_mixed_case():
    result = slugify("HelloWorld")
    assert result == result.lower()


# ---------------------------------------------------------------------------
# Rule 2: runs of non-alphanumeric chars become one separator
# ---------------------------------------------------------------------------

def test_space_becomes_separator():
    assert slugify("hello world") == "hello~world"


def test_multiple_spaces_become_one_separator():
    assert slugify("hello   world") == "hello~world"


def test_punctuation_becomes_separator():
    assert slugify("foo-bar_baz") == "foo~bar~baz"


def test_mixed_non_alnum_run_becomes_one_separator():
    assert slugify("foo ---!-- bar") == "foo~bar"


def test_separator_char_in_input_treated_as_separator():
    assert slugify("foo~bar") == "foo~bar"


# ---------------------------------------------------------------------------
# Rule 3: no leading or trailing separators
# ---------------------------------------------------------------------------

def test_leading_spaces_stripped():
    result = slugify("  hello")
    assert not result.startswith(SEPARATOR)


def test_trailing_spaces_stripped():
    result = slugify("hello  ")
    assert not result.endswith(SEPARATOR)


def test_leading_and_trailing_stripped():
    assert slugify("  Hello World  ") == "hello~world"


def test_leading_punctuation_stripped():
    result = slugify("---hello")
    assert not result.startswith(SEPARATOR)


# ---------------------------------------------------------------------------
# Rule 4 (acceptance): truncation to SLUG_MAX
# ---------------------------------------------------------------------------

def test_short_slug_not_truncated():
    text = "a" * SLUG_MAX
    assert slugify(text) == text


def test_slug_at_exact_max_length():
    text = "a" * SLUG_MAX
    result = slugify(text)
    assert len(result) == SLUG_MAX


def test_long_slug_truncated_to_max():
    text = "a" * (SLUG_MAX + 10)
    result = slugify(text)
    assert len(result) <= SLUG_MAX


def test_truncation_removes_trailing_tilde():
    # Construct a string where the 37th character would be a tilde after slugifying.
    # e.g. 36 'a' chars + separator + more chars => slug is 36 a's + ~ + ...
    # After truncating to 37, the last char is '~', which must be stripped.
    part = "a" * 36          # 36 chars
    text = part + " extra"   # separator lands at index 36
    result = slugify(text)
    assert not result.endswith(SEPARATOR)
    assert len(result) <= SLUG_MAX


def test_truncation_no_trailing_tilde_when_unnecessary():
    text = "b" * (SLUG_MAX + 5)
    result = slugify(text)
    assert not result.endswith(SEPARATOR)


# ---------------------------------------------------------------------------
# Rule 5 (acceptance): empty result returns EMPTY_SLUG
# ---------------------------------------------------------------------------

def test_empty_string_returns_empty_slug():
    assert slugify("") == EMPTY_SLUG


def test_only_non_alnum_returns_empty_slug():
    assert slugify("   ---   ") == EMPTY_SLUG


def test_empty_slug_constant_format():
    assert slugify("!!!") == "n~a"


# ---------------------------------------------------------------------------
# Integration / combined rules
# ---------------------------------------------------------------------------

def test_typical_title():
    assert slugify("Hello, World!") == "hello~world"


def test_numbers_preserved():
    assert slugify("Version 2 0") == "version~2~0"


def test_alphanumeric_only_unchanged():
    assert slugify("abc123") == "abc123"


def test_unicode_non_ascii_treated_as_separator():
    result = slugify("caf\u00e9 au lait")
    assert SEPARATOR in result
    assert not result.startswith(SEPARATOR)
    assert not result.endswith(SEPARATOR)
