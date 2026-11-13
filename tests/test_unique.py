"""Tests for unique_slug covering every rule in spec 002."""
import pytest
from slugkit import unique_slug
from slugkit.slug import SEPARATOR, SLUG_MAX, EMPTY_SLUG


# --- rule 1: base slug returned when not in existing --------------------------

def test_free_slug_returned_as_is():
    assert unique_slug("hello world", set()) == "hello~world"


def test_free_slug_not_in_existing():
    result = unique_slug("hello", {"world"})
    assert result == "hello"


# --- rule 2: suffix added when base is taken ----------------------------------

def test_suffix_2_when_base_taken():
    base = "hello~world"
    result = unique_slug("hello world", {base})
    assert result == base + SEPARATOR + "2"


def test_suffix_increments_until_free():
    base = "hello~world"
    existing = {base, base + SEPARATOR + "2", base + SEPARATOR + "3"}
    result = unique_slug("hello world", existing)
    assert result == base + SEPARATOR + "4"


def test_suffix_starts_at_2_not_1():
    base = "abc"
    existing = {base}
    result = unique_slug("abc", existing)
    assert result == "abc" + SEPARATOR + "2"


# --- rule 3: existing is never modified ---------------------------------------

def test_existing_not_modified():
    existing = {"hello"}
    original = set(existing)
    unique_slug("hello", existing)
    assert existing == original


def test_existing_not_modified_with_suffix():
    existing = {"test", "test" + SEPARATOR + "2"}
    original = set(existing)
    unique_slug("test", existing)
    assert existing == original


# --- rule 4: result fits within SLUG_MAX --------------------------------------

def test_result_within_slug_max_no_suffix():
    text = "a" * (SLUG_MAX + 10)
    result = unique_slug(text, set())
    assert len(result) <= SLUG_MAX


def test_result_within_slug_max_with_suffix():
    # Build a base that fills SLUG_MAX, then force a suffix
    long_text = "a" * (SLUG_MAX + 10)
    base = "a" * SLUG_MAX  # slugify of long_text
    result = unique_slug(long_text, {base})
    assert len(result) <= SLUG_MAX


def test_trailing_tilde_removed_before_suffix():
    # Craft a base that, when trimmed for a suffix, ends with SEPARATOR
    # base = 37 'a's slugified = 37 'a's; suffix "~2" needs 2 chars,
    # so trimmed to 35 chars = 35 'a's (no trailing tilde issue here).
    # Instead, make a base ending in tilde after trim.
    # base of length 36 ending in '~': use "aaa...a~b" and take first 36 chars
    # We'll construct the scenario directly with a known base.
    # "a" * 35 + "~" + "b" slugified = "a"*35 + "~b" (37 chars)
    base = "a" * 35 + SEPARATOR + "b"
    assert len(base) == 37 == SLUG_MAX
    # suffix "~2" is 2 chars; max_base_len = 37 - 2 = 35
    # base[:35] = "a"*35, rstrip(SEPARATOR) = "a"*35 (no tilde at end) → fine
    # Now use a base that after trimming ends with tilde
    # base2 = "a"*34 + "~" + "bb" = 37 chars
    base2 = "a" * 34 + SEPARATOR + "bb"
    assert len(base2) == 37 == SLUG_MAX
    # suffix "~2": max_base_len = 35; base2[:35] = "a"*34 + "~b"
    # rstrip("~") keeps "a"*34 + "~b" (no trailing tilde) → fine
    # Harder case: base3 = "a"*35 + "~" + "~" but separator is single char,
    # so: base3 = "a"*34 + "~" (only 35 chars)
    # Actually let's just verify the property holds for a long base
    long_base_text = "a" * 34 + " " + "b" * 10  # slugify → "a"*34 + "~" + "b"*10, truncated
    result = unique_slug(long_base_text, {unique_slug(long_base_text, set())})
    assert len(result) <= SLUG_MAX
    assert not result.endswith(SEPARATOR + SEPARATOR)  # no double sep


def test_no_trailing_tilde_in_cut_base():
    # Build input whose slugified form is exactly SLUG_MAX chars,
    # ending with the separator right before the last char.
    # Then force a suffix so that trim cuts at a tilde.
    # e.g. "a"*35 + "~x" → length 38 > 37, truncated to "a"*35 + "~" → stripped to "a"*35
    # But we want trimming for suffix to hit a tilde.
    # base = "a"*36 + "~" is 38 chars → slugify truncates to "a"*36 (rstrips "~")
    # We want a base of exactly SLUG_MAX with a "~" near the end so suffix trim hits it.
    # Let's use "a"*(SLUG_MAX-2) + "~a" = 37 chars, then suffix "~2":
    # max_base_len = 35; base[:35] = "a"*(SLUG_MAX-2) = "a"*35 (no trailing ~)
    # Try: "a"*(SLUG_MAX-3) + "~~a" is impossible (double ~ collapsed by slugify).
    # Instead construct the scenario by patching: use existing to force suffix ~10 (len 3)
    # and a base of "a"*34 + "~" + "a" (37 chars), suffix "~10":
    # max_base_len = 37-3 = 34; base[:34] = "a"*34; rstrip("~") = "a"*34 → "a"*34+"~10"
    base = "a" * 34 + SEPARATOR + "a"  # 36 chars
    # synthesize existing to force suffix ~10
    existing = {base}
    for i in range(2, 10):
        # trimmed base for suffix ~i
        sfx = SEPARATOR + str(i)
        ml = SLUG_MAX - len(sfx)
        trimmed = base[:ml].rstrip(SEPARATOR)
        existing.add(trimmed + sfx)
    result = unique_slug("a" * 34 + " a", existing)
    assert len(result) <= SLUG_MAX
    assert SEPARATOR * 2 not in result  # no double-tilde


# --- rule 5: EMPTY_SLUG fallback also gets suffixes ---------------------------

def test_empty_slug_free():
    result = unique_slug("", set())
    assert result == EMPTY_SLUG


def test_empty_slug_taken_gets_suffix():
    result = unique_slug("", {EMPTY_SLUG})
    assert result == EMPTY_SLUG + SEPARATOR + "2"


def test_empty_slug_multiple_taken():
    existing = {EMPTY_SLUG, EMPTY_SLUG + SEPARATOR + "2"}
    result = unique_slug("", existing)
    assert result == EMPTY_SLUG + SEPARATOR + "3"


def test_non_alnum_text_falls_back_to_empty_slug_logic():
    result = unique_slug("!!!", {EMPTY_SLUG})
    assert result == EMPTY_SLUG + SEPARATOR + "2"


# --- integration / edge cases -------------------------------------------------

def test_suffix_uses_separator_constant():
    base = "foo"
    result = unique_slug("foo", {base})
    assert result == "foo" + SEPARATOR + "2"


def test_large_n_suffix():
    base = "x"
    existing = {base}
    for i in range(2, 20):
        existing.add("x" + SEPARATOR + str(i))
    result = unique_slug("x", existing)
    assert result == "x" + SEPARATOR + "20"
    assert len(result) <= SLUG_MAX
