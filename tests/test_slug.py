"""Tests for slugkit.slug covering every rule in spec 001."""

import string

from slugkit import EMPTY_SLUG, SEPARATOR, SLUG_MAX, slugify
from slugkit import slug as slug_module


def test_constants_are_exposed():
    assert SEPARATOR == "~"
    assert SLUG_MAX == 37
    assert EMPTY_SLUG == "n~a"
    assert slug_module.SEPARATOR == "~"
    assert slug_module.SLUG_MAX == 37
    assert slug_module.EMPTY_SLUG == "n~a"


def test_lowercases_input():
    assert slugify("Hello") == "hello"
    assert slugify("HELLO WORLD") == "hello~world"


def test_runs_of_non_alphanumeric_become_single_separator():
    assert slugify("a--b") == "a~b"
    assert slugify("a   b") == "a~b"
    assert slugify("a___b") == "a~b"
    assert slugify("a!@#$%^&*b") == "a~b"


def test_uses_tilde_separator_not_dash():
    assert slugify("hello world") == "hello~world"
    assert SEPARATOR == "~"


def test_removes_separators_at_start_and_end():
    assert slugify("  hello  ") == "hello"
    assert slugify("!!! hello !!!") == "hello"
    assert slugify("~~~abc~~~") == "abc"


def test_only_ascii_letters_and_digits_kept():
    assert slugify("café au lait") == "caf~au~lait"
    assert slugify("naïve") == "na~ve"


def test_empty_result_returns_empty_slug():
    assert slugify("") == EMPTY_SLUG
    assert slugify("   ") == EMPTY_SLUG
    assert slugify("!!!") == EMPTY_SLUG
    assert slugify("...") == EMPTY_SLUG


def test_max_length_is_respected_and_trailing_separator_trimmed():
    # Exactly SLUG_MAX characters are kept as-is.
    exact = "a" * SLUG_MAX
    assert slugify(exact) == exact
    assert len(slugify(exact)) == SLUG_MAX

    # Longer slugs are cut to SLUG_MAX and a trailing separator removed.
    long_text = "a" * (SLUG_MAX + 5)
    assert slugify(long_text) == "a" * SLUG_MAX

    # When the cut lands on a separator, the trailing separator is removed.
    prefix = "a" * (SLUG_MAX - 1)
    text = prefix + "~" + "b" * 10
    result = slugify(text)
    assert result == prefix
    assert len(result) == SLUG_MAX - 1


def test_separator_only_appears_between_word_runs():
    slug = slugify("one two three")
    assert slug == "one~two~three"
    assert not slug.startswith("~")
    assert not slug.endswith("~")
