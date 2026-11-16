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
# Rule 1: Lowercasing
# ---------------------------------------------------------------------------

def test_lowercase_basic():
    assert slugify("Hello") == "hello"


def test_lowercase_mixed_case():
    assert slugify("FooBAR") == "foobar"


def test_lowercase_all_upper():
    assert slugify("PYTHON") == "python"


# ---------------------------------------------------------------------------
# Rule 2: Separator replacement
# ---------------------------------------------------------------------------

def test_single_separator_between_words():
    assert slugify("hello world") == "hello~world"


def test_run_of_separators_becomes_one():
    assert slugify("hello   world") == "hello~world"


def test_non_ascii_chars_become_separator():
    assert slugify("café au lait") == "caf~au~lait"


def test_punctuation_becomes_separator():
    assert slugify("one, two. three!") == "one~two~three"


def test_mixed_non_alnum_run():
    assert slugify("a---b___c") == "a~b~c"


def test_digits_preserved():
    assert slugify("py3 rules") == "py3~rules"


def test_tilde_separator_used_not_hyphen():
    result = slugify("a b")
    assert "~" in result
    assert "-" not in result


# ---------------------------------------------------------------------------
# Rule 3: Leading/trailing separators removed
# ---------------------------------------------------------------------------

def test_leading_separator_stripped():
    assert slugify("  hello") == "hello"


def test_trailing_separator_stripped():
    assert slugify("hello  ") == "hello"


def test_both_sides_stripped():
    assert slugify("  hello world  ") == "hello~world"


def test_leading_punctuation_stripped():
    assert slugify("!hello") == "hello"


# ---------------------------------------------------------------------------
# Rule 4: Maximum length truncation
# ---------------------------------------------------------------------------

def test_short_slug_not_truncated():
    text = "a" * SLUG_MAX
    assert slugify(text) == text


def test_long_slug_truncated_to_slug_max():
    text = "a" * (SLUG_MAX + 10)
    result = slugify(text)
    assert len(result) <= SLUG_MAX


def test_truncation_removes_trailing_tilde():
    # Build a string that places a separator right at the cut boundary.
    # 36 'a' chars + separator + more chars => after cut at 37 chars we'd
    # have a trailing '~' that must be removed.
    text = "a" * 36 + " " + "b" * 10
    result = slugify(text)
    assert len(result) <= SLUG_MAX
    assert not result.endswith("~")


def test_truncation_exact_boundary_no_tilde():
    text = "a" * 37 + " extra"
    result = slugify(text)
    assert result == "a" * 37


# ---------------------------------------------------------------------------
# Rule 5: Empty result returns EMPTY_SLUG
# ---------------------------------------------------------------------------

def test_empty_string_returns_empty_slug():
    assert slugify("") == EMPTY_SLUG


def test_whitespace_only_returns_empty_slug():
    assert slugify("   ") == EMPTY_SLUG


def test_non_alnum_only_returns_empty_slug():
    assert slugify("!!! ###") == EMPTY_SLUG


def test_empty_slug_literal():
    assert slugify("") == "n~a"


# ---------------------------------------------------------------------------
# Integration / round-trip style
# ---------------------------------------------------------------------------

def test_typical_blog_title():
    assert slugify("Hello, World!") == "hello~world"


def test_version_string():
    assert slugify("Python 3.12 Release") == "python~3~12~release"


def test_already_slug_like():
    assert slugify("already~fine") == "already~fine"


def test_import_from_package():
    from slugkit import slugify as sf
    assert sf("Test Import") == "test~import"
