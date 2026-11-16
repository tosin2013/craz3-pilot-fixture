"""Tests for slugkit.unique_slug covering every rule in spec 002."""

import pytest
from slugkit import unique_slug, SEPARATOR, SLUG_MAX, EMPTY_SLUG


# ---------------------------------------------------------------------------
# Rule 1: base = slugify(text); return if not in existing
# ---------------------------------------------------------------------------

def test_base_not_in_existing_returned_directly():
    assert unique_slug("Hello World", set()) == "hello~world"


def test_base_absent_from_existing_no_suffix():
    existing = {"other~slug"}
    assert unique_slug("Hello World", existing) == "hello~world"


# ---------------------------------------------------------------------------
# Rule 2 & 3: Suffix sequence starts at ~2 and increments
# ---------------------------------------------------------------------------

def test_suffix_starts_at_2():
    base = "hello~world"
    existing = {base}
    result = unique_slug("Hello World", existing)
    assert result == f"hello~world{SEPARATOR}2"


def test_suffix_increments_to_3():
    base = "hello~world"
    existing = {base, f"hello~world{SEPARATOR}2"}
    result = unique_slug("Hello World", existing)
    assert result == f"hello~world{SEPARATOR}3"


def test_suffix_increments_to_large_n():
    base = "abc"
    existing = {base} | {f"abc{SEPARATOR}{n}" for n in range(2, 10)}
    result = unique_slug("abc", existing)
    assert result == f"abc{SEPARATOR}10"


# ---------------------------------------------------------------------------
# Rule 4: existing is never modified
# ---------------------------------------------------------------------------

def test_existing_not_modified():
    existing = {"abc"}
    original = set(existing)
    unique_slug("abc", existing)
    assert existing == original


def test_existing_not_modified_with_suffixes():
    existing = {"abc", f"abc{SEPARATOR}2"}
    original = set(existing)
    unique_slug("abc", existing)
    assert existing == original


# ---------------------------------------------------------------------------
# Rule 5: Full result (including suffix) must not exceed SLUG_MAX
# ---------------------------------------------------------------------------

def test_result_within_slug_max():
    # Build a base slug exactly SLUG_MAX chars long
    long_text = "a" * SLUG_MAX
    base = "a" * SLUG_MAX  # slugify will produce this
    existing = {base}
    result = unique_slug(long_text, existing)
    assert len(result) <= SLUG_MAX


def test_result_with_suffix_within_slug_max_multiple():
    long_text = "a" * SLUG_MAX
    base = "a" * SLUG_MAX
    suffix2 = SEPARATOR + "2"
    suffix3 = SEPARATOR + "3"
    # Pre-populate both ~2 and ~3 candidates
    trimmed_for_2 = base[: SLUG_MAX - len(suffix2)].rstrip(SEPARATOR)
    trimmed_for_3 = base[: SLUG_MAX - len(suffix3)].rstrip(SEPARATOR)
    existing = {base, trimmed_for_2 + suffix2, trimmed_for_3 + suffix3}
    result = unique_slug(long_text, existing)
    assert len(result) <= SLUG_MAX


def test_base_trimmed_trailing_separator_removed():
    # Construct text whose slug is exactly SLUG_MAX chars; force a suffix that
    # would land a SEPARATOR at the trim boundary.
    # 'a' * 35 + SEPARATOR = 36 chars; full slug would need trimming.
    # We want the trimmed base (before suffix) to end with SEPARATOR so it
    # gets stripped.
    # Base: 'a'*35 + '~' + 'b'  (37 chars)
    # With suffix '~2' (2 chars), max_base_len = 35, trimmed = 'a'*35, no trailing ~.
    # Let's make a base that has '~' exactly at the cut point.
    # base = 'a' * 34 + '~' + 'b' * 2  = 37 chars
    # suffix '~2': max_base_len = 35, base[:35] = 'a'*34 + '~', rstrip('~') = 'a'*34
    text = "a" * 34 + "!" + "b" * 2 + "extra"
    from slugkit import slugify
    base = slugify(text)
    existing = {base}
    result = unique_slug(text, existing)
    assert len(result) <= SLUG_MAX
    # The separator should not appear right before the numeric suffix's own separator
    suffix = SEPARATOR + "2"
    assert not result[: -len(suffix)].endswith(SEPARATOR)


# ---------------------------------------------------------------------------
# Rule 6: EMPTY_SLUG base still gets suffixed if taken
# ---------------------------------------------------------------------------

def test_empty_slug_base_gets_suffix():
    existing = {EMPTY_SLUG}
    result = unique_slug("", existing)
    assert result == f"{EMPTY_SLUG}{SEPARATOR}2"


def test_empty_slug_base_increments():
    existing = {EMPTY_SLUG, f"{EMPTY_SLUG}{SEPARATOR}2"}
    result = unique_slug("!!!", existing)
    assert result == f"{EMPTY_SLUG}{SEPARATOR}3"


# ---------------------------------------------------------------------------
# Import check
# ---------------------------------------------------------------------------

def test_import_from_package():
    from slugkit import unique_slug as us
    assert us("Test", set()) == "test"
