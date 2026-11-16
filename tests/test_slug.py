"""Tests for slugify and its constants (spec 001)."""

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


# --- Rule 1: lowercase ---

def test_lowercases_input():
    assert slugify("Hello World") == "hello~world"


def test_all_uppercase():
    assert slugify("PYTHON") == "python"


# --- Rule 2: separator replaces non-alphanumeric runs ---

def test_spaces_become_separator():
    assert slugify("foo bar") == "foo~bar"


def test_hyphens_become_separator():
    assert slugify("foo-bar") == "foo~bar"


def test_mixed_separators_collapsed():
    assert slugify("foo  --  bar") == "foo~bar"


def test_special_chars_become_separator():
    assert slugify("hello!@#world") == "hello~world"


def test_digits_preserved():
    assert slugify("test123") == "test123"


def test_letters_and_digits_mix():
    assert slugify("v1.2.3") == "v1~2~3"


# --- Rule 3: leading/trailing separators removed ---

def test_leading_separator_removed():
    assert slugify("  hello") == "hello"


def test_trailing_separator_removed():
    assert slugify("hello  ") == "hello"


def test_leading_and_trailing_removed():
    assert slugify("---hello---") == "hello"


# --- Rule 4: max length truncation ---

def test_short_slug_unchanged():
    text = "a" * 10
    assert slugify(text) == text


def test_slug_at_max_length():
    text = "a" * SLUG_MAX
    result = slugify(text)
    assert result == text
    assert len(result) == SLUG_MAX


def test_slug_truncated_to_max():
    text = "a" * (SLUG_MAX + 10)
    result = slugify(text)
    assert len(result) == SLUG_MAX


def test_truncation_removes_trailing_separator():
    # Construct a string that after slugification would be cut mid-separator
    # 36 'a' chars + separator word boundary so the 37th char would be '~'
    text = "a" * 36 + " extra words"
    result = slugify(text)
    assert len(result) <= SLUG_MAX
    assert not result.endswith(SEPARATOR)


def test_truncation_then_strip_separator():
    # 'a'*36 + '~' + 'b'*10 -> cut at 37 gives 'a'*36 + '~' -> strip trailing '~'
    text = "a" * 36 + "-" + "b" * 10
    result = slugify(text)
    assert len(result) <= SLUG_MAX
    assert not result.endswith(SEPARATOR)


# --- Rule 5: empty result returns EMPTY_SLUG ---

def test_empty_string_returns_empty_slug():
    assert slugify("") == EMPTY_SLUG


def test_only_special_chars_returns_empty_slug():
    assert slugify("!!!") == EMPTY_SLUG


def test_only_whitespace_returns_empty_slug():
    assert slugify("   ") == EMPTY_SLUG


# --- Export check ---

def test_importable_from_package():
    from slugkit import slugify as sf
    assert callable(sf)


def test_slugify_simple():
    assert slugify("hello world") == "hello~world"
