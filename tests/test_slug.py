"""Tests for every rule in the slugify spec (001)."""

import pytest
from slugkit import slugify
from slugkit.slug import SEPARATOR, SLUG_MAX, EMPTY_SLUG


# Constants
def test_separator_value():
    assert SEPARATOR == "~"


def test_slug_max_value():
    assert SLUG_MAX == 37


def test_empty_slug_value():
    assert EMPTY_SLUG == "n~a"


# Rule 1: lowercase
def test_lowercases_input():
    assert slugify("HELLO") == "hello"


def test_lowercases_mixed_case():
    assert slugify("FooBar") == "foobar"


# Rule 2: runs of non-alphanumeric chars become one separator
def test_spaces_become_tilde():
    assert slugify("hello world") == "hello~world"


def test_multiple_spaces_become_single_tilde():
    assert slugify("hello   world") == "hello~world"


def test_punctuation_becomes_tilde():
    assert slugify("hello, world!") == "hello~world"


def test_mixed_separators_become_single_tilde():
    assert slugify("hello---world") == "hello~world"


def test_uses_tilde_not_hyphen():
    result = slugify("hello world")
    assert "~" in result
    assert "-" not in result


# Rule 3: strip leading/trailing separators
def test_leading_space_stripped():
    assert slugify("  hello") == "hello"


def test_trailing_space_stripped():
    assert slugify("hello  ") == "hello"


def test_leading_and_trailing_stripped():
    assert slugify("  Hello World  ") == "hello~world"


def test_leading_punctuation_stripped():
    assert slugify("!!!hello") == "hello"


def test_trailing_punctuation_stripped():
    assert slugify("hello!!!") == "hello"


# Truncation at SLUG_MAX
def test_no_truncation_when_at_max():
    # 37 lowercase letters
    text = "a" * SLUG_MAX
    assert slugify(text) == text


def test_truncates_to_slug_max():
    text = "a" * (SLUG_MAX + 10)
    result = slugify(text)
    assert len(result) <= SLUG_MAX


def test_truncation_removes_trailing_tilde():
    # Create a slug that, when cut at SLUG_MAX, ends with a tilde
    # 36 'a's + separator + more 'a's → cut at 37 gives "aaa...a~" → strip trailing ~
    part1 = "a" * 36
    part2 = "b" * 10
    text = part1 + " " + part2  # separator lands at position 36 (0-indexed)
    result = slugify(text)
    assert len(result) <= SLUG_MAX
    assert not result.endswith(SEPARATOR)


def test_truncated_slug_has_no_trailing_tilde():
    # Build a long string that would produce a tilde at position 37
    text = "x" * 36 + " " + "y" * 10
    result = slugify(text)
    assert not result.endswith("~")


# Empty result fallback
def test_empty_string_returns_empty_slug():
    assert slugify("") == EMPTY_SLUG


def test_only_special_chars_returns_empty_slug():
    assert slugify("!!!") == EMPTY_SLUG


def test_only_whitespace_returns_empty_slug():
    assert slugify("   ") == EMPTY_SLUG


def test_empty_slug_literal():
    assert EMPTY_SLUG == "n~a"


# General integration
def test_typical_title():
    assert slugify("Hello, World!") == "hello~world"


def test_numbers_preserved():
    assert slugify("chapter 42") == "chapter~42"


def test_alphanumeric_only():
    assert slugify("abc123") == "abc123"
