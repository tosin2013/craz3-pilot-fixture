"""Tests for slugkit.slug covering every rule in spec 001."""
import pytest
from slugkit import slugify
from slugkit.slug import SEPARATOR, SLUG_MAX, EMPTY_SLUG


# --- constants -----------------------------------------------------------------

def test_separator_value():
    assert SEPARATOR == "~"


def test_slug_max_value():
    assert SLUG_MAX == 37


def test_empty_slug_value():
    assert EMPTY_SLUG == "n~a"


# --- rule 1: lowercase ---------------------------------------------------------

def test_lowercases_ascii():
    assert slugify("Hello") == "hello"


def test_lowercases_mixed():
    assert slugify("FoO BAR") == "foo~bar"


# --- rule 2: runs of non-alphanumeric become one separator ---------------------

def test_single_space_becomes_separator():
    assert slugify("a b") == "a~b"


def test_multiple_spaces_become_one_separator():
    assert slugify("a   b") == "a~b"


def test_punctuation_becomes_separator():
    assert slugify("hello, world!") == "hello~world"


def test_mixed_non_alnum_run_becomes_one_separator():
    assert slugify("a---b") == "a~b"


def test_mixed_chars_in_run():
    assert slugify("a !@# b") == "a~b"


# --- rule 3: strip leading/trailing separators ---------------------------------

def test_leading_separator_removed():
    assert not slugify("  hello").startswith(SEPARATOR)


def test_trailing_separator_removed():
    assert not slugify("hello  ").endswith(SEPARATOR)


def test_leading_and_trailing_removed():
    result = slugify("  Hello World  ")
    assert not result.startswith(SEPARATOR)
    assert not result.endswith(SEPARATOR)
    assert "hello" in result
    assert "world" in result


# --- rule 4: separator is tilde, not hyphen ------------------------------------

def test_separator_is_tilde_not_hyphen():
    result = slugify("hello world")
    assert SEPARATOR in result
    assert "-" not in result


# --- truncation ----------------------------------------------------------------

def test_slug_within_max_not_truncated():
    text = "a" * SLUG_MAX
    assert slugify(text) == text


def test_slug_over_max_truncated_to_slug_max():
    text = "a" * (SLUG_MAX + 10)
    result = slugify(text)
    assert len(result) <= SLUG_MAX


def test_truncation_removes_trailing_tilde():
    # Construct input so a separator lands exactly at position SLUG_MAX
    # e.g. 36 'a's + separator + more chars  → cut at 37 gives trailing '~'
    part = "a" * (SLUG_MAX - 1)       # 36 chars
    text = part + " extra words here"  # separator at index 36 after slugify
    result = slugify(text)
    assert len(result) <= SLUG_MAX
    assert not result.endswith(SEPARATOR)


def test_truncation_exact_boundary():
    # slug is exactly SLUG_MAX chars — should be unchanged
    slug = "a" * SLUG_MAX
    assert slugify(slug) == slug
    assert len(slugify(slug)) == SLUG_MAX


# --- empty result fallback -----------------------------------------------------

def test_empty_string_returns_empty_slug():
    assert slugify("") == EMPTY_SLUG


def test_only_non_alnum_returns_empty_slug():
    assert slugify("!!!") == EMPTY_SLUG


def test_whitespace_only_returns_empty_slug():
    assert slugify("   ") == EMPTY_SLUG


def test_empty_slug_constant_is_returned():
    assert slugify("") == "n~a"
