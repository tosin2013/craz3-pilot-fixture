"""Tests for unique_slug."""

import pytest
from slugkit import unique_slug
from slugkit.slug import SEPARATOR, SLUG_MAX, EMPTY_SLUG


# ---------------------------------------------------------------------------
# Basic behaviour
# ---------------------------------------------------------------------------

def test_base_not_in_existing_returns_base():
    assert unique_slug("hello world", set()) == "hello~world"


def test_base_not_in_existing_no_suffix():
    result = unique_slug("hello", {"other"})
    assert result == "hello"


def test_base_in_existing_returns_with_suffix_2():
    result = unique_slug("hello", {"hello"})
    assert result == "hello~2"


def test_suffix_increments_until_free():
    existing = {"hello", "hello~2", "hello~3"}
    result = unique_slug("hello", existing)
    assert result == "hello~4"


def test_suffix_separator_is_tilde():
    result = unique_slug("abc", {"abc"})
    assert result == "abc~2"


# ---------------------------------------------------------------------------
# existing is never modified
# ---------------------------------------------------------------------------

def test_existing_not_modified():
    existing = {"hello"}
    original = set(existing)
    unique_slug("hello", existing)
    assert existing == original


def test_existing_not_modified_multiple_collisions():
    existing = {"abc", "abc~2", "abc~3"}
    original = set(existing)
    unique_slug("abc", existing)
    assert existing == original


# ---------------------------------------------------------------------------
# SLUG_MAX enforcement with suffix
# ---------------------------------------------------------------------------

def test_result_within_slug_max_when_suffix_added():
    # Base that fills SLUG_MAX exactly; adding suffix must still respect SLUG_MAX.
    long_text = "a" * (SLUG_MAX + 10)
    base = "a" * SLUG_MAX
    existing = {base}
    result = unique_slug(long_text, existing)
    assert len(result) <= SLUG_MAX


def test_base_truncated_to_fit_suffix():
    # Build a base that is exactly SLUG_MAX chars, all 'a's.
    base = "a" * SLUG_MAX
    existing = {base}
    result = unique_slug("a" * (SLUG_MAX + 10), existing)
    suffix = SEPARATOR + "2"
    expected_base = ("a" * SLUG_MAX)[:SLUG_MAX - len(suffix)]
    assert result == expected_base + suffix


def test_trailing_separator_stripped_before_suffix():
    # Craft a base where truncation to fit suffix leaves a trailing SEPARATOR.
    # SLUG_MAX=37, suffix="~2" (len=2), so max_base_len=35.
    # If the base is "a"*34 + "~" + "a"*2 = 37 chars, cutting to 35 gives
    # "a"*34 + "~" → trailing "~" must be stripped before appending suffix.
    text = "a" * 34 + " " + "a" * 2  # slugify → "a"*34 + "~" + "aa" = 37 chars
    base = "a" * 34 + SEPARATOR + "aa"
    assert len(base) == SLUG_MAX
    existing = {base}
    result = unique_slug(text, existing)
    assert len(result) <= SLUG_MAX
    # The cut base at position 35 is "a"*34 + "~"; after rstrip it's "a"*34
    expected = "a" * 34 + SEPARATOR + "2"
    assert result == expected


# ---------------------------------------------------------------------------
# EMPTY_SLUG base case
# ---------------------------------------------------------------------------

def test_empty_text_returns_empty_slug_when_free():
    result = unique_slug("", set())
    assert result == EMPTY_SLUG


def test_empty_slug_taken_uses_suffix():
    existing = {EMPTY_SLUG}
    result = unique_slug("", existing)
    assert result == EMPTY_SLUG + SEPARATOR + "2"


def test_empty_slug_multiple_taken():
    existing = {EMPTY_SLUG, EMPTY_SLUG + SEPARATOR + "2"}
    result = unique_slug("", existing)
    assert result == EMPTY_SLUG + SEPARATOR + "3"


# ---------------------------------------------------------------------------
# Import from top-level package
# ---------------------------------------------------------------------------

def test_importable_from_slugkit():
    from slugkit import unique_slug as us
    assert callable(us)
