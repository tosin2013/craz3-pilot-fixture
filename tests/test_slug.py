"""Tests for slugify covering every rule in spec 001."""
import pytest
from slugkit import slugify
from slugkit.slug import SEPARATOR, SLUG_MAX, EMPTY_SLUG


def test_separator_constant():
    assert SEPARATOR == "~"


def test_slug_max_constant():
    assert SLUG_MAX == 37


def test_empty_slug_constant():
    assert EMPTY_SLUG == "n~a"


# --- Rule 1: lowercase ---

def test_lowercase():
    assert slugify("Hello World") == "hello~world"


def test_already_lowercase():
    assert slugify("hello") == "hello"


# --- Rule 2: runs of non-alphanumeric become one separator ---

def test_single_space_separator():
    assert slugify("foo bar") == "foo~bar"


def test_multiple_spaces_become_one_separator():
    assert slugify("foo   bar") == "foo~bar"


def test_mixed_non_alnum_run():
    assert slugify("foo!@#bar") == "foo~bar"


def test_hyphen_becomes_separator():
    assert slugify("foo-bar") == "foo~bar"


def test_underscore_becomes_separator():
    assert slugify("foo_bar") == "foo~bar"


# --- Rule 3: leading / trailing separators removed ---

def test_leading_spaces_stripped():
    assert slugify("  hello") == "hello"


def test_trailing_spaces_stripped():
    assert slugify("hello  ") == "hello"


def test_both_sides_stripped():
    assert slugify("  Hello World  ") == "hello~world"


def test_leading_non_alnum_stripped():
    assert slugify("---hello---") == "hello"


# --- Rule 4: standard library only (import check) ---

def test_uses_tilde_not_hyphen():
    result = slugify("hello world")
    assert "~" in result
    assert "-" not in result


# --- Truncation at SLUG_MAX ---

def test_no_truncation_at_max_length():
    text = "a" * SLUG_MAX
    assert slugify(text) == text


def test_truncated_to_slug_max():
    text = "a" * (SLUG_MAX + 10)
    result = slugify(text)
    assert len(result) <= SLUG_MAX


def test_truncation_removes_trailing_tilde():
    # Build a string whose slug is exactly SLUG_MAX chars ending in a tilde after cut
    # 36 'a's + separator word so the 37th char would be '~'
    text = "a" * 36 + " extra"
    result = slugify(text)
    assert len(result) <= SLUG_MAX
    assert not result.endswith(SEPARATOR)


def test_long_slug_still_valid():
    text = "word " * 20  # many words
    result = slugify(text)
    assert len(result) <= SLUG_MAX
    assert not result.endswith(SEPARATOR)


# --- Empty / blank input → EMPTY_SLUG ---

def test_empty_string():
    assert slugify("") == EMPTY_SLUG


def test_whitespace_only():
    assert slugify("   ") == EMPTY_SLUG


def test_non_alnum_only():
    assert slugify("!@#$%") == EMPTY_SLUG


def test_empty_slug_value():
    assert slugify("") == "n~a"
