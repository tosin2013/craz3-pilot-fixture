"""Tests for the unique_slug function."""

from slugkit import slugify, unique_slug
from slugkit.slug import EMPTY_SLUG, SEPARATOR, SLUG_MAX


def test_returns_base_when_free():
    assert unique_slug("Hello World", set()) == slugify("Hello World")


def test_returns_base_when_not_in_existing():
    base = slugify("Hello World")
    assert unique_slug("Hello World", {"other"}) == base


def test_appends_numeric_suffix_starting_at_two():
    base = slugify("abc")
    assert unique_slug("abc", {base}) == "abc~2"


def test_increments_suffix_until_free():
    base = slugify("abc")
    existing = {base, "abc~2", "abc~3"}
    assert unique_slug("abc", existing) == "abc~4"


def test_suffix_uses_separator_constant():
    base = slugify("abc")
    assert unique_slug("abc", {base}) == base + SEPARATOR + "2"


def test_result_within_slug_max():
    base = "a" * SLUG_MAX
    result = unique_slug(base, {base})
    assert len(result) <= SLUG_MAX


def test_cuts_base_to_fit_suffix():
    base = "a" * SLUG_MAX
    result = unique_slug(base, {base})
    assert result == "a" * (SLUG_MAX - 2) + "~2"


def test_removes_trailing_separator_from_cut_base():
    # The cut lands on a separator, so the cut base ends with "~".
    text = "a" * 34 + " " + "b"
    base = slugify(text)
    assert base == "a" * 34 + "~" + "b"
    result = unique_slug(text, {base})
    assert result == "a" * 34 + "~2"
    assert "~~" not in result


def test_empty_slug_taken_gets_suffix():
    assert unique_slug("", {EMPTY_SLUG}) == EMPTY_SLUG + "~2"


def test_never_modifies_existing():
    existing = {slugify("abc")}
    original = set(existing)
    unique_slug("abc", existing)
    assert existing == original
