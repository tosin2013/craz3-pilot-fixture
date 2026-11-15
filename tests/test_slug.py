"""Tests for slugify and its constants."""

import pytest
from slugkit import slugify, SEPARATOR, SLUG_MAX, EMPTY_SLUG
from slugkit.slug import slugify as slugify_direct


# --- Constants ---

def test_separator_value():
    assert SEPARATOR == "~"


def test_slug_max_value():
    assert SLUG_MAX == 37


def test_empty_slug_value():
    assert EMPTY_SLUG == "n~a"


# --- Rule 1: Lowercase ---

def test_lowercases_input():
    assert slugify("Hello World") == "hello~world"


def test_all_uppercase():
    assert slugify("PYTHON") == "python"


# --- Rule 2: Non-alphanumeric runs become a single separator ---

def test_spaces_become_tilde():
    assert slugify("foo bar") == "foo~bar"


def test_multiple_spaces_become_one_tilde():
    assert slugify("foo   bar") == "foo~bar"


def test_mixed_separators_become_one_tilde():
    assert slugify("foo!@# bar") == "foo~bar"


def test_hyphens_become_tilde():
    assert slugify("foo-bar") == "foo~bar"


def test_underscores_become_tilde():
    assert slugify("foo_bar") == "foo~bar"


def test_digits_are_kept():
    assert slugify("foo123bar") == "foo123bar"


# --- Rule 3: Strip leading/trailing separators ---

def test_leading_separator_removed():
    assert slugify("  hello") == "hello"


def test_trailing_separator_removed():
    assert slugify("hello  ") == "hello"


def test_leading_and_trailing_removed():
    assert slugify("  hello world  ") == "hello~world"


def test_leading_non_alnum_removed():
    assert slugify("!!!hello") == "hello"


# --- Rule 4: Max length is SLUG_MAX (37) ---

def test_short_slug_not_truncated():
    text = "a" * 37
    assert slugify(text) == text


def test_long_slug_truncated_to_37():
    text = "a" * 50
    result = slugify(text)
    assert len(result) <= SLUG_MAX


def test_truncation_removes_trailing_tilde():
    # Build a string that produces a tilde right at position 37 after truncation.
    # "a" * 36 + separator + "b" * 20  -> after slugify: "a"*36 + "~" + "b"*20
    # Truncated to 37 chars: "a"*36 + "~" -> trailing tilde must be stripped -> "a"*36
    text = "a" * 36 + "!!!" + "b" * 20
    result = slugify(text)
    assert len(result) == 36
    assert not result.endswith("~")


def test_truncation_keeps_valid_ending():
    text = "a" * 37 + "b" * 10
    result = slugify(text)
    assert len(result) == SLUG_MAX
    assert not result.endswith("~")


# --- Rule 5: Empty result returns EMPTY_SLUG ---

def test_empty_string_returns_empty_slug():
    assert slugify("") == EMPTY_SLUG


def test_only_separators_returns_empty_slug():
    assert slugify("!!!") == EMPTY_SLUG


def test_only_spaces_returns_empty_slug():
    assert slugify("   ") == EMPTY_SLUG


def test_empty_slug_literal():
    assert EMPTY_SLUG == "n~a"


# --- Import from package root ---

def test_importable_from_package():
    from slugkit import slugify as sf
    assert sf("Hello World") == "hello~world"
