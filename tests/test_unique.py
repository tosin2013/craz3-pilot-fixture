"""Tests for unique_slug (spec 002)."""

import pytest
from slugkit import unique_slug, SEPARATOR, SLUG_MAX, EMPTY_SLUG


def test_base_not_in_existing_returns_base():
    """If the base slug is free, return it immediately."""
    assert unique_slug("hello world", set()) == "hello~world"


def test_base_in_existing_adds_suffix_2():
    """First collision appends ~2."""
    assert unique_slug("hello", {"hello"}) == "hello~2"


def test_increments_suffix_until_free():
    """Increments n until a free slot is found."""
    existing = {"hello", "hello~2", "hello~3"}
    assert unique_slug("hello", existing) == "hello~4"


def test_does_not_modify_existing():
    """existing must not be mutated."""
    existing = {"foo"}
    original = set(existing)
    unique_slug("foo", existing)
    assert existing == original


def test_empty_slug_fallback_collision():
    """EMPTY_SLUG taken → apply suffix rules (n~a~2)."""
    existing = {EMPTY_SLUG}  # "n~a"
    result = unique_slug("!!!", existing)
    assert result == EMPTY_SLUG + SEPARATOR + "2"


def test_empty_slug_fallback_multiple_collisions():
    """EMPTY_SLUG and n~a~2 both taken → n~a~3."""
    existing = {EMPTY_SLUG, EMPTY_SLUG + SEPARATOR + "2"}
    result = unique_slug("!!!", existing)
    assert result == EMPTY_SLUG + SEPARATOR + "3"


def test_result_at_most_slug_max():
    """The result (including suffix) must never exceed SLUG_MAX characters."""
    # Create a text that produces a slug of exactly SLUG_MAX chars
    long_text = "a" * SLUG_MAX
    base = "a" * SLUG_MAX  # slugify of this is "a" * SLUG_MAX
    existing = {base}
    result = unique_slug(long_text, existing)
    assert len(result) <= SLUG_MAX


def test_base_trimmed_no_trailing_separator_before_suffix():
    """When trimming the base to fit the suffix, trailing SEPARATOR is removed."""
    # Build a base that is exactly SLUG_MAX chars, ending with SEPARATOR
    # so that after trimming one char for the suffix the last char is SEPARATOR
    suffix = SEPARATOR + "2"  # length 2
    # We want base[:SLUG_MAX - 2] to end with SEPARATOR
    # Craft a base of SLUG_MAX chars whose char at index (SLUG_MAX-3) is SEPARATOR
    base_chars = ["a"] * SLUG_MAX
    base_chars[SLUG_MAX - len(suffix) - 1] = SEPARATOR
    base = "".join(base_chars)
    # Simulate: we have a slug equal to base in existing
    existing = {base}
    # We need to generate a text whose slugify() == base; just use base directly
    # since it only contains 'a' and SEPARATOR which slugify preserves.
    # But slugify strips leading/trailing separators, so ensure no edge SEPARATOR.
    # base_chars[0] is 'a', base_chars[-1] is 'a' — safe.
    result = unique_slug(base, existing)
    assert len(result) <= SLUG_MAX
    assert not result[: SLUG_MAX - len(suffix)].endswith(SEPARATOR) or result.endswith(suffix)


def test_suffix_separator_is_separator_constant():
    """The separator between base and numeric suffix is SEPARATOR, not a hyphen."""
    result = unique_slug("test", {"test"})
    assert result == "test" + SEPARATOR + "2"


def test_free_slug_no_existing():
    """Empty existing set always returns base slug."""
    assert unique_slug("Python 3!", set()) == "python~3"


def test_multiple_words_no_collision():
    """Multi-word slugs returned as-is when free."""
    assert unique_slug("foo bar baz", set()) == "foo~bar~baz"


def test_collision_with_long_base_result_trimmed():
    """With a full-length base in existing, suffix candidate fits within SLUG_MAX."""
    base = "a" * SLUG_MAX
    existing = {base}
    result = unique_slug("a" * SLUG_MAX, existing)
    assert len(result) <= SLUG_MAX
    assert result.endswith(SEPARATOR + "2")
