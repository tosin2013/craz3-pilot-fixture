"""Tests for unique_slug."""

import pytest
from slugkit import unique_slug, SEPARATOR, SLUG_MAX, EMPTY_SLUG
from slugkit.unique import unique_slug as unique_slug_direct


# --- Rule 1: base not in existing => return base as-is ----------------------

def test_base_not_in_existing_returns_base():
    assert unique_slug("hello world", set()) == "hello~world"


def test_base_not_in_existing_no_mutation():
    existing = {"other~slug"}
    result = unique_slug("hello", existing)
    assert result == "hello"
    assert existing == {"other~slug"}


# --- Rule 2: base in existing => try suffixes --------------------------------

def test_collision_adds_suffix_2():
    existing = {"hello~world"}
    assert unique_slug("hello world", existing) == "hello~world~2"


def test_collision_adds_suffix_3_when_2_taken():
    existing = {"hello~world", "hello~world~2"}
    assert unique_slug("hello world", existing) == "hello~world~3"


def test_collision_advances_through_multiple_suffixes():
    existing = {"abc", "abc~2", "abc~3", "abc~4"}
    assert unique_slug("abc", existing) == "abc~5"


# --- Rule 3: existing is never modified -------------------------------------

def test_existing_not_modified_on_collision():
    existing = {"hello"}
    before = set(existing)
    unique_slug("hello", existing)
    assert existing == before


def test_existing_not_modified_no_collision():
    existing = {"other"}
    before = set(existing)
    unique_slug("hello", existing)
    assert existing == before


# --- Rule 4: suffix format is SEPARATOR + str(n) ----------------------------

def test_suffix_uses_separator_constant():
    existing = {"foo"}
    result = unique_slug("foo", existing)
    assert result == f"foo{SEPARATOR}2"


def test_suffix_n_starts_at_2_not_1():
    existing = {"foo"}
    result = unique_slug("foo", existing)
    assert result.endswith("2")
    assert SEPARATOR + "1" not in result


# --- Rule 5: full result must be <= SLUG_MAX --------------------------------

def test_long_base_truncated_to_fit_suffix():
    # Build a base that is exactly SLUG_MAX characters long
    long_text = "a" * SLUG_MAX
    base = "a" * SLUG_MAX  # slugify gives exactly SLUG_MAX 'a's
    existing = {base}
    result = unique_slug(long_text, existing)
    assert len(result) <= SLUG_MAX


def test_long_base_no_trailing_separator_after_cut():
    # Craft text whose slug is SLUG_MAX chars; force a suffix
    long_text = "a" * SLUG_MAX
    base = "a" * SLUG_MAX
    existing = {base}
    result = unique_slug(long_text, existing)
    # The part before the final suffix should not contain a trailing separator
    suffix = SEPARATOR + "2"
    trimmed_base = result[: -len(suffix)]
    assert not trimmed_base.endswith(SEPARATOR)


def test_result_never_exceeds_slug_max():
    # Even with many collisions, every returned value must fit
    base_text = "z" * 100
    from slugkit import slugify
    base = slugify(base_text)
    existing = {base}
    # Add a bunch of collisions
    for n in range(2, 20):
        existing.add(unique_slug(base_text, existing))
    # Every slug in existing must be <= SLUG_MAX
    for slug in existing:
        assert len(slug) <= SLUG_MAX, f"{slug!r} exceeds SLUG_MAX"


# --- Rule 6: EMPTY_SLUG base still gets suffixed if taken -------------------

def test_empty_slug_base_is_suffixed_when_taken():
    existing = {EMPTY_SLUG}
    result = unique_slug("", existing)
    assert result == f"{EMPTY_SLUG}{SEPARATOR}2"


def test_empty_slug_base_advances_suffix():
    existing = {EMPTY_SLUG, f"{EMPTY_SLUG}{SEPARATOR}2"}
    result = unique_slug("", existing)
    assert result == f"{EMPTY_SLUG}{SEPARATOR}3"


# --- Export: importable from top-level package ------------------------------

def test_importable_from_package():
    from slugkit import unique_slug as us
    assert callable(us)


def test_uses_slugify_internally():
    # unique_slug should apply slugify rules (e.g. lowercasing)
    existing = set()
    result = unique_slug("Hello World", existing)
    assert result == "hello~world"


# --- Edge cases -------------------------------------------------------------

def test_empty_existing_set():
    result = unique_slug("test", set())
    assert result == "test"


def test_punctuation_input():
    existing = set()
    result = unique_slug("!!!", existing)
    assert result == EMPTY_SLUG


def test_suffix_cut_base_fits_exactly():
    # suffix "~2" is 2 chars; base can be SLUG_MAX - 2 chars max
    # construct a slug that is SLUG_MAX chars, force collision, check length
    long_text = "b" * SLUG_MAX
    from slugkit import slugify
    base = slugify(long_text)
    assert len(base) == SLUG_MAX
    existing = {base}
    result = unique_slug(long_text, existing)
    assert len(result) <= SLUG_MAX
    assert result.endswith(f"{SEPARATOR}2")
