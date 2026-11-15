import pytest
from slugkit import slugify
from slugkit.slug import SEPARATOR, SLUG_MAX, EMPTY_SLUG


def test_separator_constant():
    assert SEPARATOR == "~"


def test_slug_max_constant():
    assert SLUG_MAX == 37


def test_empty_slug_constant():
    assert EMPTY_SLUG == "n~a"


def test_basic_lowercase():
    assert slugify("Hello World") == "hello~world"


def test_already_lowercase():
    assert slugify("hello world") == "hello~world"


def test_uppercase_input():
    assert slugify("HELLO WORLD") == "hello~world"


def test_uses_tilde_separator():
    assert "~" in slugify("hello world")
    assert "-" not in slugify("hello world")


def test_non_alphanumeric_replaced_by_tilde():
    assert slugify("foo!bar") == "foo~bar"
    assert slugify("foo...bar") == "foo~bar"


def test_run_of_separators_becomes_one():
    assert slugify("foo   bar") == "foo~bar"
    assert slugify("foo---bar") == "foo~bar"
    assert slugify("foo!@#bar") == "foo~bar"


def test_leading_separator_removed():
    assert slugify("  hello") == "hello"
    assert slugify("!!!hello") == "hello"


def test_trailing_separator_removed():
    assert slugify("hello  ") == "hello"
    assert slugify("hello!!!") == "hello"


def test_leading_and_trailing_removed():
    assert slugify("  hello world  ") == "hello~world"


def test_digits_preserved():
    assert slugify("foo 42 bar") == "foo~42~bar"


def test_mixed_alphanumeric():
    assert slugify("foo2bar") == "foo2bar"


def test_empty_string_returns_empty_slug():
    assert slugify("") == EMPTY_SLUG


def test_only_separators_returns_empty_slug():
    assert slugify("   ") == EMPTY_SLUG
    assert slugify("!!!") == EMPTY_SLUG


def test_max_length_not_exceeded():
    result = slugify("a" * 100)
    assert len(result) <= SLUG_MAX


def test_long_slug_truncated_to_slug_max():
    long_input = "a" * 50
    result = slugify(long_input)
    assert len(result) == SLUG_MAX


def test_truncated_slug_no_trailing_tilde():
    # Build input so the cut falls on a tilde
    # 37 chars: 18 a's + ~ + rest -> cut at 37 would land on tilde
    part = "a" * 18 + " " + "b" * 20
    result = slugify(part)
    assert len(result) <= SLUG_MAX
    assert not result.endswith("~")


def test_truncation_removes_trailing_tilde():
    # Construct a string where the 37th character would be a tilde
    # "a" * 18 + "~" + "b" * 19 -> length 38, cut at 37 gives "a"*18 + "~" + "b"*18
    # Actually let's force a tilde at position 37 (index 36)
    # 36 a's + space + lots more -> slug = "a"*36 + "~" + ...
    # cut at 37 = "a"*36 + "~" -> trailing tilde removed -> "a"*36
    text = "a" * 36 + " " + "b" * 10
    result = slugify(text)
    assert len(result) <= SLUG_MAX
    assert not result.endswith("~")


def test_exactly_slug_max_length():
    text = "a" * SLUG_MAX
    result = slugify(text)
    assert result == "a" * SLUG_MAX
    assert len(result) == SLUG_MAX


def test_special_characters_only_with_letters():
    assert slugify("hello-world") == "hello~world"
    assert slugify("hello_world") == "hello~world"


def test_numbers_only():
    assert slugify("12345") == "12345"


def test_unicode_non_ascii_treated_as_separator():
    result = slugify("café")
    assert result == "caf~e" or result == "cafe" or "~" not in result.replace("caf", "")
    # The key rule: non-ASCII chars are not ASCII letters/digits, so treated as separator
    assert not result.endswith("~")
    assert not result.startswith("~")


def test_unicode_separator_behavior():
    # 'é' is not an ASCII letter, so it's a separator
    result = slugify("caf\u00e9 bar")
    assert result == "caf~bar"


def test_newline_treated_as_separator():
    assert slugify("foo\nbar") == "foo~bar"


def test_tab_treated_as_separator():
    assert slugify("foo\tbar") == "foo~bar"


def test_import_from_slugkit():
    from slugkit import slugify as sf
    assert sf("Hello World") == "hello~world"
