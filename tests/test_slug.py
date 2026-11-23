"""Tests for ``slugkit.slug.slugify`` and its constants."""

from slugkit import EMPTY_SLUG, SEPARATOR, SLUG_MAX, slugify
from slugkit import slug as slug_module


def test_constants_have_expected_values():
    assert SEPARATOR == "~"
    assert SLUG_MAX == 37
    assert EMPTY_SLUG == "n~a"


def test_constants_live_on_slug_module():
    assert slug_module.SEPARATOR == "~"
    assert slug_module.SLUG_MAX == 37
    assert slug_module.EMPTY_SLUG == "n~a"


def test_lowercases_input():
    assert slugify("Hello World") == slugify("hello world")
    assert slugify("ABC") == "abc"


def test_replaces_non_alnum_runs_with_separator():
    assert slugify("hello world") == "hello~world"
    assert slugify("hello  world") == "hello~world"
    assert slugify("hello---world") == "hello~world"
    assert slugify("a.b,c!d") == "a~b~c~d"


def test_separator_is_tilde_not_hyphen():
    assert slugify("hello world") == "hello~world"
    assert "-" not in slugify("hello world")


def test_strips_leading_and_trailing_separators():
    assert slugify("  hello  ") == "hello"
    assert slugify("---hello world---") == "hello~world"
    assert slugify("..abc..") == "abc"


def test_keeps_ascii_letters_and_digits():
    assert slugify("abc123") == "abc123"
    assert slugify("123 abc") == "123~abc"


def test_truncates_long_slug_to_slug_max():
    long_text = "a" * 50
    result = slugify(long_text)
    assert len(result) == SLUG_MAX
    assert result == "a" * SLUG_MAX


def test_truncation_removes_trailing_separator():
    # 36 letters, a separator, then more letters: cutting at 37 leaves a
    # trailing "~" which must be removed.
    text = ("a" * 36) + "-" + "b"
    result = slugify(text)
    assert result == "a" * 36
    assert not result.endswith(SEPARATOR)


def test_empty_result_returns_empty_slug():
    assert slugify("") == EMPTY_SLUG
    assert slugify("!!!") == EMPTY_SLUG
    assert slugify("   ") == EMPTY_SLUG


def test_result_is_always_ascii_alnum_or_separator():
    samples = ["Hello, World!", "  spaced  out  ", "foo_bar-baz.qux", "MiXeD 123"]
    for s in samples:
        out = slugify(s)
        assert all(c.isascii() and (c.isalnum() or c == SEPARATOR) for c in out)
        assert out == out.lower()
        assert not out.startswith(SEPARATOR)
        assert not out.endswith(SEPARATOR)
