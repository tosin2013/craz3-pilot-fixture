"""Tests for Spec 001: slugify."""

from slugkit import EMPTY_SLUG, SEPARATOR, SLUG_MAX, slugify


def test_constants():
    assert SEPARATOR == "~"
    assert SLUG_MAX == 37
    assert EMPTY_SLUG == "n~a"


def test_lowercases():
    assert slugify("Hello World") == "hello~world"


def test_collapses_non_alphanumeric_runs_to_one_separator():
    assert slugify("a--b__c  d") == "a~b~c~d"


def test_uses_tilde_separator():
    assert "~" in slugify("a b")
    assert "-" not in slugify("a b")


def test_strips_leading_and_trailing_separators():
    assert slugify("  hello world  ") == "hello~world"
    assert slugify("!!!hello!!!") == "hello"


def test_non_ascii_treated_as_separator():
    assert slugify("café au lait") == "caf~au~lait"


def test_truncates_to_max_length():
    long_text = "a" * 100
    assert slugify(long_text) == "a" * SLUG_MAX
    assert len(slugify(long_text)) <= SLUG_MAX


def test_truncation_removes_trailing_separator():
    text = "a" * SLUG_MAX + " b"
    assert slugify(text) == "a" * SLUG_MAX


def test_truncation_strips_trailing_separator_when_cut_lands_on_separator():
    # "a" * 36 + "~b" -> cut at 37 gives "a"*36 + "~", trailing "~" removed.
    text = "a" * 36 + " b"
    assert slugify(text) == "a" * 36


def test_empty_returns_empty_slug():
    assert slugify("") == EMPTY_SLUG
    assert slugify("!!!") == EMPTY_SLUG
    assert slugify("   ") == EMPTY_SLUG
