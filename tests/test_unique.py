"""Tests for ``slugkit.unique.unique_slug``."""

from slugkit import EMPTY_SLUG, SEPARATOR, SLUG_MAX, slugify, unique_slug


def test_returns_base_when_not_in_existing():
    assert unique_slug("Hello World", set()) == "hello~world"
    assert unique_slug("abc", {"xyz"}) == "abc"


def test_appends_separator_and_2_when_base_taken():
    assert unique_slug("abc", {"abc"}) == "abc" + SEPARATOR + "2"


def test_skips_taken_suffixes_until_free():
    existing = {"abc", "abc~2", "abc~3", "abc~4"}
    assert unique_slug("abc", existing) == "abc~5"


def test_does_not_modify_existing():
    existing = {"abc", "abc~2"}
    snapshot = set(existing)
    unique_slug("abc", existing)
    assert existing == snapshot


def test_empty_slug_taken_still_gets_suffix():
    assert unique_slug("", {EMPTY_SLUG}) == EMPTY_SLUG + "~2"
    assert unique_slug("!!!", {EMPTY_SLUG}) == EMPTY_SLUG + "~2"


def test_long_base_is_cut_to_fit_suffix():
    base = "a" * SLUG_MAX
    assert unique_slug("a" * SLUG_MAX, {base}) == "a" * (SLUG_MAX - 2) + "~2"


def test_cut_base_removes_trailing_separator_before_suffix():
    # slugify produces "a" * 34 + "~" + "bb"; cutting at 35 leaves a trailing
    # "~" which must be stripped before the suffix is appended.
    text = "a" * 34 + "-" + "b" * 10
    base = slugify(text)
    result = unique_slug(text, {base})
    assert result == "a" * 34 + "~2"
    assert "~~" not in result


def test_result_never_exceeds_slug_max():
    existing = {slugify("a" * 50)}
    for _ in range(5):
        result = unique_slug("a" * 50, existing)
        assert len(result) <= SLUG_MAX
        existing.add(result)


def test_longer_suffix_cuts_more_of_base():
    base = "a" * SLUG_MAX
    existing = {base}
    for n in range(2, 10):
        existing.add("a" * (SLUG_MAX - 2) + "~" + str(n))
    assert unique_slug("a" * SLUG_MAX, existing) == "a" * (SLUG_MAX - 3) + "~10"
