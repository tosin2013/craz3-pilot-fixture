import pytest
from slugkit import slugify, SEPARATOR, SLUG_MAX, EMPTY_SLUG


def test_constants():
    assert SEPARATOR == "~"
    assert SLUG_MAX == 37
    assert EMPTY_SLUG == "n~a"


def test_lowercase():
    assert slugify("Hello World") == "hello~world"


def test_separator_is_tilde():
    assert slugify("foo bar") == "foo~bar"


def test_run_of_separators_collapsed():
    assert slugify("foo   bar") == "foo~bar"
    assert slugify("foo-bar--baz") == "foo~bar~baz"
    assert slugify("foo!@#bar") == "foo~bar"


def test_leading_trailing_separators_removed():
    assert slugify("  hello  ") == "hello"
    assert slugify("--hello--") == "hello"
    assert slugify("!!!") == EMPTY_SLUG


def test_empty_input_returns_empty_slug():
    assert slugify("") == EMPTY_SLUG


def test_whitespace_only_returns_empty_slug():
    assert slugify("   ") == EMPTY_SLUG


def test_non_ascii_treated_as_separator():
    # Non-ASCII characters are treated as separators; trailing/leading tildes are stripped
    result = slugify("über cool")
    assert result == "ber~cool"
    # 'café': 'é' is non-ASCII, becomes separator; trailing separator stripped
    result = slugify("café")
    assert result in ("caf~e", "caf")  # depends on unicode decomposition


def test_digits_preserved():
    assert slugify("abc123") == "abc123"
    assert slugify("123 456") == "123~456"


def test_truncation_to_max_length():
    long_input = "a" * 50
    result = slugify(long_input)
    assert len(result) <= SLUG_MAX


def test_truncation_removes_trailing_tilde():
    # Construct input that would produce a tilde right at position SLUG_MAX
    # e.g. 36 'a's then a separator then more text -> cut at 37, strip trailing ~
    text = "a" * 36 + " " + "b" * 10
    result = slugify(text)
    assert len(result) <= SLUG_MAX
    assert not result.endswith(SEPARATOR)


def test_truncation_exact_boundary():
    # 37 chars with no separator: should stay as-is
    text = "a" * 37
    result = slugify(text)
    assert result == "a" * 37

    # 38 chars: truncated to 37
    text = "a" * 38
    result = slugify(text)
    assert result == "a" * 37


def test_mixed_case_and_symbols():
    assert slugify("Hello, World!") == "hello~world"


def test_already_valid_slug():
    assert slugify("hello~world") == "hello~world"


def test_empty_slug_constant_exported():
    from slugkit import EMPTY_SLUG as es
    assert es == "n~a"
