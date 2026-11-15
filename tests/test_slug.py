"""Tests for slugify covering every rule in spec 001."""

import pytest
from slugkit import slugify
from slugkit.slug import SEPARATOR, SLUG_MAX, EMPTY_SLUG


# --- Constants ---

def test_separator_value():
    assert SEPARATOR == "~"


def test_slug_max_value():
    assert SLUG_MAX == 37


def test_empty_slug_value():
    assert EMPTY_SLUG == "n~a"


# --- Rule 1: Lowercase ---

def test_lowercases_ascii():
    assert slugify("Hello") == "hello"


def test_lowercases_mixed_case():
    assert slugify("FoO BaR") == "foo~bar"


# --- Rule 2: Non-alphanumeric runs become one separator ---

def test_single_space_becomes_separator():
    assert slugify("foo bar") == "foo~bar"


def test_multiple_spaces_become_one_separator():
    assert slugify("foo   bar") == "foo~bar"


def test_special_chars_become_separator():
    assert slugify("foo!@#bar") == "foo~bar"


def test_mixed_separators_collapse():
    assert slugify("foo - bar") == "foo~bar"


def test_separator_char_in_input_treated_as_separator():
    assert slugify("foo~bar") == "foo~bar"


# --- Rule 3: Strip leading/trailing separators ---

def test_leading_spaces_stripped():
    assert slugify("  hello") == "hello"


def test_trailing_spaces_stripped():
    assert slugify("hello  ") == "hello"


def test_leading_and_trailing_specials_stripped():
    assert slugify("---hello---") == "hello"


def test_leading_trailing_mixed_stripped():
    assert slugify("  Hello World  ") == "hello~world"


# --- Rule 4: Maximum length ---

def test_short_slug_not_truncated():
    slug = slugify("a" * 37)
    assert slug == "a" * 37


def test_slug_truncated_to_max():
    # 38 'a's → slug is 38 chars, should be cut to 37
    slug = slugify("a" * 38)
    assert len(slug) <= SLUG_MAX


def test_truncation_removes_trailing_separator():
    # Construct input so that cut falls on a separator
    # 36 a's + separator + more chars → after cut the 37th char is '~'
    text = "a" * 36 + " " + "b" * 10
    slug = slugify(text)
    assert len(slug) <= SLUG_MAX
    assert not slug.endswith(SEPARATOR)


def test_long_slug_exact_length():
    long_text = "ab cd " * 10  # alternating word and space
    slug = slugify(long_text)
    assert len(slug) <= SLUG_MAX


# --- Rule 5: Empty result returns EMPTY_SLUG ---

def test_empty_string_returns_empty_slug():
    assert slugify("") == EMPTY_SLUG


def test_whitespace_only_returns_empty_slug():
    assert slugify("   ") == EMPTY_SLUG


def test_special_chars_only_returns_empty_slug():
    assert slugify("!@#$%") == EMPTY_SLUG


# --- Export from package ---

def test_slugify_importable_from_package():
    from slugkit import slugify as sf
    assert callable(sf)


def test_constants_importable_from_package():
    from slugkit import SEPARATOR, SLUG_MAX, EMPTY_SLUG
    assert SEPARATOR == "~"
    assert SLUG_MAX == 37
    assert EMPTY_SLUG == "n~a"
