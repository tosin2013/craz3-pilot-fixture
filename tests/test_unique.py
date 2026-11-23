"""Tests for every rule in spec 002 (unique slug function)."""

from slugkit import unique_slug
from slugkit import slug


def test_returns_base_when_free():
    assert unique_slug("Hello World", set()) == "hello~world"


def test_does_not_modify_existing():
    existing = {"hello~world"}
    snapshot = set(existing)
    unique_slug("Hello World", existing)
    assert existing == snapshot


def test_suffix_starts_at_two():
    existing = {"hello~world"}
    assert unique_slug("Hello World", existing) == "hello~world~2"


def test_suffix_increments_until_free():
    existing = {"abc", "abc~2", "abc~3"}
    assert unique_slug("abc", existing) == "abc~4"


def test_suffix_uses_separator_not_dash():
    existing = {"abc"}
    result = unique_slug("abc", existing)
    assert result == "abc~2"
    assert "~" in result


def test_result_respects_slug_max():
    existing = {"a" * slug.SLUG_MAX}
    result = unique_slug("a" * 100, existing)
    assert len(result) <= slug.SLUG_MAX


def test_cut_base_strips_trailing_separator_before_suffix():
    # A 37-char base with a separator at index 34: cutting to 35 chars for the
    # "~2" suffix lands on the separator, which must be stripped first.
    text = "a" * (slug.SLUG_MAX - 3) + " " + "b" * 2
    base = slug.slugify(text)
    assert base == "a" * (slug.SLUG_MAX - 3) + "~" + "b" * 2
    assert len(base) == slug.SLUG_MAX

    existing = {base}
    result = unique_slug(text, existing)
    assert result == "a" * (slug.SLUG_MAX - 3) + "~2"
    assert len(result) <= slug.SLUG_MAX
    assert "~~" not in result


def test_empty_slug_taken_gets_suffix():
    existing = {slug.EMPTY_SLUG}
    assert unique_slug("", existing) == "n~a~2"


def test_empty_slug_suffix_increments():
    existing = {slug.EMPTY_SLUG, "n~a~2"}
    assert unique_slug("", existing) == "n~a~3"
