"""Tests for the slugify function and its constants (spec 001)."""

from slugkit import EMPTY_SLUG, SEPARATOR, SLUG_MAX, slugify
from slugkit.slug import EMPTY_SLUG as _EMPTY_SLUG
from slugkit.slug import SEPARATOR as _SEPARATOR
from slugkit.slug import SLUG_MAX as _SLUG_MAX


def test_constants_have_expected_values():
    assert SEPARATOR == "~"
    assert SLUG_MAX == 37
    assert EMPTY_SLUG == "n~a"


def test_constants_are_defined_on_slug_module():
    assert _SEPARATOR == "~"
    assert _SLUG_MAX == 37
    assert _EMPTY_SLUG == "n~a"


def test_lowercases_input():
    assert slugify("Hello World") == "hello~world"
    assert slugify("HELLO") == "hello"


def test_runs_of_non_alnum_become_single_separator():
    assert slugify("hello   world") == "hello~world"
    assert slugify("hello, world") == "hello~world"
    assert slugify("hello---world") == "hello~world"
    assert slugify("a@@@###b") == "a~b"


def test_uses_tilde_separator_not_dash():
    assert "~" in slugify("hello world")
    assert "-" not in slugify("hello-world")


def test_removes_leading_and_trailing_separators():
    assert slugify("  hello world  ") == "hello~world"
    assert slugify("---hello---") == "hello"
    assert slugify("!!!hello!!!") == "hello"


def test_empty_input_returns_empty_slug():
    assert slugify("") == EMPTY_SLUG
    assert slugify("   ") == EMPTY_SLUG
    assert slugify("!!!") == EMPTY_SLUG


def test_truncates_to_slug_max():
    long_word = "a" * 100
    result = slugify(long_word)
    assert len(result) == SLUG_MAX


def test_truncation_removes_trailing_separator():
    # 40 letters with a separator in the middle, so the cut lands on a "~".
    text = "a" * 40 + " " + "b" * 40
    result = slugify(text)
    assert len(result) <= SLUG_MAX
    assert not result.endswith("~")
    assert result.endswith("a")


def test_truncated_result_starts_correctly():
    text = "a" * 50
    result = slugify(text)
    assert result == "a" * SLUG_MAX


def test_short_slug_is_unchanged():
    assert slugify("abc") == "abc"
    assert slugify("abc def") == "abc~def"
