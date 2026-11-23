"""Tests for the unique_slug function (spec 002)."""

from slugkit import slugify, unique_slug
from slugkit.slug import EMPTY_SLUG, SEPARATOR, SLUG_MAX


def test_returns_base_when_free():
    assert unique_slug("Hello World", set()) == slugify("Hello World")


def test_returns_base_when_not_in_existing():
    assert unique_slug("abc", {"xyz"}) == "abc"


def test_uses_suffix_2_when_base_taken():
    assert unique_slug("abc", {"abc"}) == "abc~2"


def test_skips_taken_suffixes():
    assert unique_slug("abc", {"abc", "abc~2"}) == "abc~3"
    assert unique_slug("abc", {"abc", "abc~2", "abc~3", "abc~4"}) == "abc~5"


def test_suffix_uses_separator():
    assert unique_slug("abc", {"abc"}) == "abc" + SEPARATOR + "2"


def test_result_never_exceeds_max():
    # base is at SLUG_MAX already; the suffix must still fit.
    result = unique_slug("a" * SLUG_MAX, {"a" * SLUG_MAX})
    assert len(result) <= SLUG_MAX
    assert result == ("a" * (SLUG_MAX - 2)) + "~2"


def test_cut_base_removes_trailing_separator():
    # base = 34 a's + "~" + "b" (36 chars). Cutting to 35 leaves a trailing "~".
    base = ("a" * 34) + "~" + "b"
    assert slugify(("a" * 34) + " " + "b") == base
    result = unique_slug(("a" * 34) + " " + "b", {base})
    assert result == ("a" * 34) + "~2"
    assert not result.endswith(SEPARATOR + SEPARATOR)


def test_empty_slug_taken_uses_suffix():
    assert unique_slug("", {EMPTY_SLUG}) == EMPTY_SLUG + "~2"
    assert unique_slug("!!!", {EMPTY_SLUG, EMPTY_SLUG + "~2"}) == EMPTY_SLUG + "~3"


def test_does_not_modify_existing():
    existing = {"abc", "abc~2"}
    snapshot = set(existing)
    unique_slug("abc", existing)
    assert existing == snapshot
