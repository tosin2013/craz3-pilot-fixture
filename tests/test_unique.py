"""Tests for slugkit.unique covering every rule in spec 002."""

from slugkit import EMPTY_SLUG, SEPARATOR, SLUG_MAX, slugify, unique_slug


def test_returns_base_when_free():
    assert unique_slug("Hello World", set()) == slugify("Hello World")
    assert unique_slug("Hello World", {"other"}) == slugify("Hello World")


def test_uses_separator_and_starts_at_two():
    assert unique_slug("abc", {"abc"}) == "abc" + SEPARATOR + "2"


def test_tries_subsequent_suffixes_until_free():
    existing = {"abc", "abc~2", "abc~3"}
    assert unique_slug("abc", existing) == "abc~4"


def test_does_not_modify_existing():
    existing = {"abc", "abc~2"}
    before = set(existing)
    unique_slug("abc", existing)
    assert existing == before


def test_empty_slug_gets_suffix_when_taken():
    assert unique_slug("", {EMPTY_SLUG}) == EMPTY_SLUG + SEPARATOR + "2"
    assert unique_slug("!!!", {EMPTY_SLUG, EMPTY_SLUG + SEPARATOR + "2"}) == (
        EMPTY_SLUG + SEPARATOR + "3"
    )


def test_result_respects_slug_max():
    base = "a" * SLUG_MAX
    result = unique_slug(base, {base})
    assert len(result) <= SLUG_MAX
    assert result == "a" * (SLUG_MAX - 2) + SEPARATOR + "2"


def test_trailing_separator_removed_from_cut_base():
    # A base whose 35th character is a separator: cutting it for the "~2"
    # suffix leaves a trailing "~" that must be stripped before suffixing.
    base_text = "a" * (SLUG_MAX - 3) + SEPARATOR + "bb"
    assert len(slugify(base_text)) == SLUG_MAX

    result = unique_slug(base_text, {slugify(base_text)})
    assert result == "a" * (SLUG_MAX - 3) + SEPARATOR + "2"
    assert len(result) <= SLUG_MAX


def test_long_base_with_large_n_stays_within_max():
    base = "a" * SLUG_MAX
    existing = {base}
    # Occupy suffixes ~2 through ~9 so n reaches 10 (a longer suffix).
    for n in range(2, 10):
        suffix = SEPARATOR + str(n)
        existing.add(base[: SLUG_MAX - len(suffix)] + suffix)

    result = unique_slug(base, existing)
    assert len(result) <= SLUG_MAX
    assert result == "a" * (SLUG_MAX - 3) + SEPARATOR + "10"
