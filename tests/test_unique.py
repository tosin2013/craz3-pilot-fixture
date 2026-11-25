"""Tests for Spec 002: unique_slug."""

from slugkit import EMPTY_SLUG, SEPARATOR, SLUG_MAX, slugify, unique_slug


def test_returns_base_when_free():
    assert unique_slug("Hello World", set()) == slugify("Hello World")


def test_appends_suffix_when_base_taken():
    base = slugify("hello world")
    assert unique_slug("hello world", {base}) == base + SEPARATOR + "2"


def test_increments_suffix_until_free():
    base = slugify("hello world")
    existing = {base, base + SEPARATOR + "2"}
    assert unique_slug("hello world", existing) == base + SEPARATOR + "3"


def test_suffixes_start_at_two():
    base = slugify("abc")
    assert unique_slug("abc", {base}) == "abc" + SEPARATOR + "2"


def test_does_not_modify_existing():
    base = slugify("hello world")
    existing = {base}
    before = set(existing)
    unique_slug("hello world", existing)
    assert existing == before


def test_result_within_max_length():
    long_text = "a" * 100
    base = slugify(long_text)
    result = unique_slug(long_text, {base})
    assert len(result) <= SLUG_MAX


def test_cuts_base_and_removes_trailing_separator():
    # slugify("a"*34 + " b") == "a"*34 + "~b" (36 chars). With suffix "~2" the
    # base must be cut to 35 chars, landing on "~", which is then stripped.
    text = "a" * 34 + " b"
    base = slugify(text)
    assert unique_slug(text, {base}) == "a" * 34 + SEPARATOR + "2"


def test_empty_slug_taken_gets_suffix():
    assert unique_slug("!!!", {EMPTY_SLUG}) == EMPTY_SLUG + SEPARATOR + "2"
