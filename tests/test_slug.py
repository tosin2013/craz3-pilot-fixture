"""Tests for the slugify function and its constants (spec 001)."""

from slugkit import slugify
from slugkit.slug import EMPTY_SLUG, SEPARATOR, SLUG_MAX


def test_constants():
    assert SEPARATOR == "~"
    assert SLUG_MAX == 37
    assert EMPTY_SLUG == "n~a"


def test_lowercases():
    assert slugify("Hello World") == "hello~world"
    assert slugify("ABC") == "abc"


def test_runs_of_non_alnum_become_one_separator():
    assert slugify("a   b") == "a~b"
    assert slugify("a---b") == "a~b"
    assert slugify("a___b") == "a~b"
    assert slugify("a ,.!? b") == "a~b"


def test_separator_is_tilde():
    assert slugify("hello world") == "hello~world"
    assert "~" in slugify("hello world")
    assert "-" not in slugify("hello world")


def test_separators_removed_at_start_and_end():
    assert slugify("  hello  ") == "hello"
    assert slugify("---hello---") == "hello"
    assert slugify("~~hello~~") == "hello"
    assert slugify("~") == EMPTY_SLUG


def test_empty_input_returns_empty_slug():
    assert slugify("") == EMPTY_SLUG


def test_only_non_alnum_returns_empty_slug():
    assert slugify("!!!") == EMPTY_SLUG
    assert slugify(" ~~~ ") == EMPTY_SLUG


def test_short_slug_is_untouched():
    assert slugify("hello world") == "hello~world"
    assert len(slugify("hello world")) <= SLUG_MAX


def test_long_slug_is_cut_to_max():
    # 40 letters -> cut to 37 letters.
    slug = slugify("a" * 40)
    assert slug == "a" * SLUG_MAX
    assert len(slug) == SLUG_MAX


def test_cut_removes_trailing_separator():
    # 36 letters + separator + 1 letter = 38 chars; cutting to 37 leaves a
    # trailing separator that must be removed.
    slug = slugify(("a" * 36) + " " + "b")
    assert slug == "a" * 36
    assert not slug.endswith(SEPARATOR)


def test_result_never_exceeds_max():
    assert len(slugify("x" * 1000)) <= SLUG_MAX
