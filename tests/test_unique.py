"""Tests for spec 002: unique_slug."""

from slugkit import unique_slug
from slugkit.slug import EMPTY_SLUG, SEPARATOR, SLUG_MAX, slugify


def test_returns_base_when_free():
    assert unique_slug("Hello World", set()) == slugify("Hello World")
    assert unique_slug("abc", {"xyz", "def"}) == "abc"


def test_uses_numeric_suffixes_from_two():
    existing = {"abc"}
    assert unique_slug("abc", existing) == "abc" + SEPARATOR + "2"


def test_skips_taken_suffixes():
    existing = {"abc", "abc~2", "abc~3"}
    assert unique_slug("abc", existing) == "abc~4"


def test_does_not_modify_existing():
    existing = {"abc", "abc~2"}
    before = set(existing)
    unique_slug("abc", existing)
    assert existing == before


def test_full_result_at_most_slug_max():
    # A very long base that is already at SLUG_MAX must be cut to fit the suffix.
    existing = {"a" * SLUG_MAX}
    result = unique_slug("a" * 100, existing)
    assert result == "a" * (SLUG_MAX - len(SEPARATOR + "2")) + SEPARATOR + "2"
    assert len(result) <= SLUG_MAX


def test_cut_removes_trailing_separator():
    # base has a separator just after the cut point; the cut base ends in "~"
    # which must be stripped before the suffix is added.
    text = "a" * 34 + "~b"
    base = slugify(text)  # "a" * 34 + "~" + "b"
    assert base.endswith("~b")
    existing = {base}
    result = unique_slug(text, existing)
    assert result == "a" * 34 + SEPARATOR + "2"
    assert len(result) <= SLUG_MAX


def test_empty_slug_taken_gets_suffix():
    existing = {EMPTY_SLUG}
    assert unique_slug("!!!", existing) == EMPTY_SLUG + SEPARATOR + "2"
