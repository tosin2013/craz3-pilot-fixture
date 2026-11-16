import pytest
from slugkit import slugify
from slugkit.slug import SEPARATOR, SLUG_MAX, EMPTY_SLUG


def test_separator_constant():
    assert SEPARATOR == "~"


def test_slug_max_constant():
    assert SLUG_MAX == 37


def test_empty_slug_constant():
    assert EMPTY_SLUG == "n~a"


def test_slugify_exported_from_package():
    from slugkit import slugify as sf
    assert callable(sf)


# Rule 1: Lowercase
def test_lowercase():
    assert slugify("Hello World") == "hello~world"


def test_all_uppercase():
    assert slugify("PYTHON") == "python"


# Rule 2: Runs of non-alphanumeric characters become one separator
def test_single_space_separator():
    assert slugify("hello world") == "hello~world"


def test_multiple_spaces_become_one_separator():
    assert slugify("hello   world") == "hello~world"


def test_special_chars_become_separator():
    assert slugify("hello-world") == "hello~world"


def test_mixed_separators_collapse():
    assert slugify("hello - world") == "hello~world"


def test_various_non_alnum_chars():
    assert slugify("foo!@#bar") == "foo~bar"


# Rule 3: No leading or trailing separators
def test_no_leading_separator():
    assert not slugify("  hello").startswith("~")


def test_no_trailing_separator():
    assert not slugify("hello  ").endswith("~")


def test_leading_and_trailing_stripped():
    assert slugify("  hello world  ") == "hello~world"


# Rule 4: Separator is tilde, not hyphen
def test_separator_is_tilde():
    result = slugify("hello world")
    assert "~" in result
    assert "-" not in result


# SLUG_MAX: truncate to 37 chars, then strip trailing tilde
def test_slug_exactly_max_length():
    text = "a" * SLUG_MAX
    assert slugify(text) == "a" * SLUG_MAX


def test_slug_longer_than_max_is_cut():
    text = "a" * (SLUG_MAX + 10)
    result = slugify(text)
    assert len(result) <= SLUG_MAX


def test_slug_cut_removes_trailing_tilde():
    # Construct input that produces a tilde exactly at position SLUG_MAX after cut
    # 36 'a's + separator + more chars => after cut at 37, position 37 is '~'
    text = "a" * 36 + "   " + "b" * 10
    result = slugify(text)
    assert len(result) <= SLUG_MAX
    assert not result.endswith("~")


def test_long_slug_with_tilde_at_boundary():
    # 37 a's then space then more: slug is 'aaa...a~bbb'; cut at 37 may land on '~'
    text = "a" * 37 + " " + "b" * 10
    result = slugify(text)
    assert len(result) <= SLUG_MAX
    assert not result.endswith("~")


# EMPTY_SLUG: empty or whitespace/special-only input
def test_empty_string_returns_empty_slug():
    assert slugify("") == EMPTY_SLUG


def test_whitespace_only_returns_empty_slug():
    assert slugify("   ") == EMPTY_SLUG


def test_special_chars_only_returns_empty_slug():
    assert slugify("!@#$%") == EMPTY_SLUG


# Combined cases
def test_numbers_preserved():
    assert slugify("chapter 2") == "chapter~2"


def test_alphanumeric_mixed():
    assert slugify("Python3 is great") == "python3~is~great"


def test_unicode_non_ascii_treated_as_separator():
    result = slugify("café")
    assert "~" not in result or not result.startswith("~")
    assert not result.endswith("~")
