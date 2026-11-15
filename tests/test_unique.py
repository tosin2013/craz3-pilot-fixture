"""Tests for unique_slug."""

import pytest
from slugkit import unique_slug, SEPARATOR, SLUG_MAX, EMPTY_SLUG


# --- Basic behaviour ---

def test_base_not_in_existing_returned_as_is():
    assert unique_slug("Hello World", set()) == "hello~world"


def test_base_free_no_suffix():
    result = unique_slug("foo", {"bar", "baz"})
    assert result == "foo"


def test_base_taken_returns_suffix_2():
    result = unique_slug("foo", {"foo"})
    assert result == "foo~2"


def test_base_and_2_taken_returns_suffix_3():
    result = unique_slug("foo", {"foo", "foo~2"})
    assert result == "foo~3"


def test_suffix_increments_until_free():
    existing = {"foo", "foo~2", "foo~3", "foo~4"}
    result = unique_slug("foo", existing)
    assert result == "foo~5"


# --- existing is never modified ---

def test_existing_not_modified():
    existing = {"foo"}
    original = set(existing)
    unique_slug("foo", existing)
    assert existing == original


# --- Result length is at most SLUG_MAX ---

def test_result_length_at_most_slug_max_no_suffix():
    long_text = "a" * 100
    result = unique_slug(long_text, set())
    assert len(result) <= SLUG_MAX


def test_result_length_at_most_slug_max_with_suffix():
    long_text = "a" * 100
    base = "a" * SLUG_MAX
    result = unique_slug(long_text, {base})
    assert len(result) <= SLUG_MAX


def test_base_cut_so_suffix_fits():
    # Create a base that is exactly SLUG_MAX characters.
    # With suffix "~2" (len 2), the base must be trimmed to SLUG_MAX - 2 = 35 chars.
    long_text = "a" * 100
    base = "a" * SLUG_MAX
    result = unique_slug(long_text, {base})
    suffix = SEPARATOR + "2"
    assert result == "a" * (SLUG_MAX - len(suffix)) + suffix
    assert len(result) == SLUG_MAX


# --- Trailing separator stripped from trimmed base ---

def test_trailing_separator_removed_before_suffix():
    # Construct a base of exactly SLUG_MAX chars ending in SEPARATOR at cut point.
    # base = "a" * 35 + "~" + "a"  (37 chars total, that's SLUG_MAX)
    # With suffix "~2" (len 2), max_base_len = 35, so trimmed = ("a"*35+"~"+"a")[:35] = "a"*35+"~"
    # After rstrip("~"): "a"*35, then candidate = "a"*35 + "~2"
    base_str = "a" * 35 + "~a"  # 37 chars
    # We need unique_slug to produce this base; craft text that slugifies to it.
    # Instead, test directly by creating a scenario where the cut falls on a separator.
    # Build text: 35 a's + separator chars + 1 a (so slugify gives "a"*35 + "~" + "a")
    text = "a" * 35 + "!!!" + "a"
    base = "a" * 35 + "~a"
    assert len(base) == SLUG_MAX

    existing = {base}
    result = unique_slug(text, existing)
    suffix = SEPARATOR + "2"
    # trimmed base at cut = 35 chars: "a"*35 + "~" -> rstrip -> "a"*35
    expected = "a" * 35 + suffix
    assert result == expected
    assert len(result) <= SLUG_MAX
    assert not result[: SLUG_MAX - len(suffix)].endswith(SEPARATOR)


# --- EMPTY_SLUG base ---

def test_empty_slug_free():
    result = unique_slug("", set())
    assert result == EMPTY_SLUG


def test_empty_slug_taken():
    result = unique_slug("", {EMPTY_SLUG})
    assert result == EMPTY_SLUG + "~2"


def test_empty_slug_and_2_taken():
    result = unique_slug("", {EMPTY_SLUG, EMPTY_SLUG + "~2"})
    assert result == EMPTY_SLUG + "~3"


# --- Import from package root ---

def test_importable_from_package():
    from slugkit import unique_slug as us
    assert us("hello", set()) == "hello"
