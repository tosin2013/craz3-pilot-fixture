"""Tests for every rule in spec 001: Slug function."""

import pytest
from slugkit import slugify
from slugkit.slug import SEPARATOR, SLUG_MAX, EMPTY_SLUG


# --- constants ---

def test_separator_value():
    assert SEPARATOR == "~"


def test_slug_max_value():
    assert SLUG_MAX == 37


def test_empty_slug_value():
    assert EMPTY_SLUG == "n~a"


# --- rule 1: lowercase ---

def test_lowercases_ascii():
    assert slugify("Hello") == "hello"


def test_lowercases_mixed_case():
    assert slugify("FooBAR") == "foobar"


# --- rule 2: runs of non-alphanumeric chars become one separator ---

def test_spaces_become_separator():
    assert slugify("hello world") == "hello~world"


def test_multiple_spaces_become_one_separator():
    assert slugify("hello   world") == "hello~world"


def test_punctuation_becomes_separator():
    assert slugify("hello-world") == "hello~world"


def test_mixed_non_alnum_run_becomes_one_separator():
    assert slugify("hello---world") == "hello~world"


def test_separator_char_is_tilde_not_dash():
    result = slugify("a b")
    assert "~" in result
    assert "-" not in result


# --- rule 3: no leading or trailing separator ---

def test_leading_spaces_stripped():
    result = slugify("  hello")
    assert not result.startswith("~")


def test_trailing_spaces_stripped():
    result = slugify("hello  ")
    assert not result.endswith("~")


def test_leading_and_trailing_stripped():
    result = slugify("  hello world  ")
    assert result == "hello~world"


# --- rule 4: standard library only (no third-party imports) ---

def test_no_third_party_imports():
    import importlib
    import slugkit.slug as mod
    # Verify the module imports only stdlib modules
    import sys
    for name in vars(mod).values():
        if callable(name) and hasattr(name, "__module__"):
            assert name.__module__ in (None, "slugkit.slug", "re", "builtins")


# --- max length truncation ---

def test_slug_within_max_length_unchanged():
    text = "a" * SLUG_MAX
    assert slugify(text) == text


def test_slug_exceeding_max_is_cut():
    text = "a" * (SLUG_MAX + 10)
    result = slugify(text)
    assert len(result) <= SLUG_MAX


def test_truncation_removes_trailing_tilde():
    # Construct input so the cut falls on a separator
    # 36 'a's + separator + more letters → cut at 37 may land on '~'
    word1 = "a" * 36
    word2 = "b" * 5
    text = word1 + " " + word2  # slug would be "aaa...a~bbbbb"
    result = slugify(text)
    assert len(result) <= SLUG_MAX
    assert not result.endswith("~")


def test_truncation_exact_boundary():
    # slug of exactly SLUG_MAX characters should be untouched
    slug_text = "x" * SLUG_MAX
    assert slugify(slug_text) == slug_text


# --- empty result ---

def test_empty_string_returns_empty_slug():
    assert slugify("") == EMPTY_SLUG


def test_only_separators_returns_empty_slug():
    assert slugify("   ---   ") == EMPTY_SLUG


def test_empty_slug_literal():
    assert EMPTY_SLUG == "n~a"


# --- combined behaviour ---

def test_full_example():
    result = slugify("  Hello, World!  ")
    assert result == "hello~world"


def test_digits_preserved():
    assert slugify("abc 123") == "abc~123"


def test_alphanumeric_only_no_separator():
    assert slugify("abc123") == "abc123"
