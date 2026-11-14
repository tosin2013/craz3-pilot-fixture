"""Tests for slugify and its exported constants."""

import pytest
from slugkit import slugify, SEPARATOR, SLUG_MAX, EMPTY_SLUG
from slugkit.slug import slugify as slugify_direct


# --- Constant values --------------------------------------------------------

def test_separator_value():
    assert SEPARATOR == "~"


def test_slug_max_value():
    assert SLUG_MAX == 37


def test_empty_slug_value():
    assert EMPTY_SLUG == "n~a"


# --- Rule 1: Lowercase ------------------------------------------------------

def test_uppercase_is_lowercased():
    assert slugify("Hello World") == "hello~world"


def test_mixed_case():
    assert slugify("FooBAR") == "foobar"


# --- Rule 2: Non-alphanumeric runs become a single separator ----------------

def test_spaces_become_separator():
    assert slugify("foo bar") == "foo~bar"


def test_multiple_spaces_become_one_separator():
    assert slugify("foo   bar") == "foo~bar"


def test_punctuation_becomes_separator():
    assert slugify("foo-bar") == "foo~bar"


def test_mixed_punctuation_run_becomes_one_separator():
    assert slugify("foo ---!!! bar") == "foo~bar"


def test_separator_char_is_tilde():
    result = slugify("a b")
    assert "~" in result
    assert "-" not in result


# --- Rule 3: Strip leading/trailing separators ------------------------------

def test_leading_separator_stripped():
    assert slugify("  hello") == "hello"


def test_trailing_separator_stripped():
    assert slugify("hello  ") == "hello"


def test_both_ends_stripped():
    assert slugify("  hello world  ") == "hello~world"


# --- Rule 4: Maximum length truncation --------------------------------------

def test_short_slug_not_truncated():
    text = "a" * 37
    assert slugify(text) == text


def test_long_slug_truncated_to_max():
    text = "a" * 50
    result = slugify(text)
    assert len(result) <= SLUG_MAX


def test_truncation_removes_trailing_tilde():
    # Build a string that, when slugified, hits exactly the cut point with a separator
    # "aaa...~bbb" where the cut falls on the tilde
    part_a = "a" * 36
    part_b = "b" * 10
    text = part_a + " " + part_b  # slug would be "aaa...~bbb..." length > 37
    result = slugify(text)
    assert len(result) <= SLUG_MAX
    assert not result.endswith("~")


def test_exact_max_length_no_truncation():
    text = "a" * SLUG_MAX
    assert slugify(text) == text
    assert len(slugify(text)) == SLUG_MAX


# --- Rule 5: Empty result returns EMPTY_SLUG --------------------------------

def test_empty_string_returns_empty_slug():
    assert slugify("") == EMPTY_SLUG


def test_whitespace_only_returns_empty_slug():
    assert slugify("   ") == EMPTY_SLUG


def test_punctuation_only_returns_empty_slug():
    assert slugify("!!! ---") == EMPTY_SLUG


def test_empty_slug_literal():
    assert slugify("") == "n~a"


# --- Export: importable from top-level package ------------------------------

def test_importable_from_package():
    from slugkit import slugify as sf
    assert callable(sf)


def test_slugify_basic_roundtrip():
    assert slugify("Hello, World!") == "hello~world"
