"""Tests for spec 001: slugify."""

from slugkit import slugify
from slugkit.slug import EMPTY_SLUG, SEPARATOR, SLUG_MAX


def test_constants():
    assert SEPARATOR == "~"
    assert SLUG_MAX == 37
    assert EMPTY_SLUG == "n~a"


def test_lowercases():
    assert slugify("Hello World") == "hello~world"
    assert slugify("ABC") == "abc"


def test_runs_of_non_alnum_collapse_to_one_separator():
    assert slugify("hello  world") == "hello~world"
    assert slugify("hello---world") == "hello~world"
    assert slugify("hello___world") == "hello~world"
    assert slugify("a!@#$%^&*()b") == "a~b"


def test_strips_leading_and_trailing_separators():
    assert slugify("  hello  ") == "hello"
    assert slugify("---hello---") == "hello"
    assert slugify("  Hello World  ") == "hello~world"


def test_empty_input_returns_empty_slug():
    assert slugify("") == EMPTY_SLUG
    assert slugify("   ") == EMPTY_SLUG
    assert slugify("!!!") == EMPTY_SLUG


def test_long_slug_is_cut_to_slug_max():
    result = slugify("a" * 100)
    assert result == "a" * SLUG_MAX
    assert len(result) == SLUG_MAX


def test_cut_removes_trailing_separator():
    # slug before cut is "a"*36 + "~" + "b" (length 38); cutting to 37 leaves a
    # trailing separator which must be removed.
    result = slugify("a" * 36 + "---b")
    assert result == "a" * 36
