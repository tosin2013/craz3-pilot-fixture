import pytest
from slugkit import slugify, SEPARATOR, SLUG_MAX, EMPTY_SLUG
from slugkit.slug import slugify as slug_direct


# --- constant values ---

def test_separator_value():
    assert SEPARATOR == "~"

def test_slug_max_value():
    assert SLUG_MAX == 37

def test_empty_slug_value():
    assert EMPTY_SLUG == "n~a"


# --- rule 1: lowercase ---

def test_lowercases_input():
    assert slugify("Hello World") == "hello~world"

def test_all_uppercase():
    assert slugify("PYTHON") == "python"


# --- rule 2: non-alphanum runs become one separator ---

def test_spaces_become_separator():
    assert slugify("foo bar") == "foo~bar"

def test_multiple_spaces_become_one_separator():
    assert slugify("foo   bar") == "foo~bar"

def test_punctuation_becomes_separator():
    assert slugify("foo!@#bar") == "foo~bar"

def test_mixed_separators_collapse():
    assert slugify("foo - bar") == "foo~bar"

def test_tilde_in_input_treated_as_separator():
    assert slugify("foo~bar") == "foo~bar"


# --- rule 3: strip leading/trailing separators ---

def test_leading_separator_stripped():
    assert slugify("  hello") == "hello"

def test_trailing_separator_stripped():
    assert slugify("hello  ") == "hello"

def test_both_ends_stripped():
    assert slugify("  hello world  ") == "hello~world"

def test_leading_punctuation_stripped():
    assert slugify("---hello") == "hello"


# --- rule 4: empty result returns EMPTY_SLUG ---

def test_empty_string_returns_empty_slug():
    assert slugify("") == EMPTY_SLUG

def test_only_separators_returns_empty_slug():
    assert slugify("   ") == EMPTY_SLUG

def test_only_punctuation_returns_empty_slug():
    assert slugify("!@#$%") == EMPTY_SLUG


# --- rule 5: truncation at SLUG_MAX ---

def test_slug_within_max_not_truncated():
    text = "a" * SLUG_MAX
    assert slugify(text) == text

def test_slug_truncated_at_max():
    text = "a" * (SLUG_MAX + 10)
    result = slugify(text)
    assert len(result) <= SLUG_MAX

def test_truncation_removes_trailing_tilde():
    # Construct a string that after slugify produces a tilde at position SLUG_MAX
    # e.g. 36 'a's then a space then more letters → slug is "aaa...a~bbb..."
    # cutting at 37 chars lands on '~' which must be stripped
    part1 = "a" * (SLUG_MAX - 1)   # 36 chars
    part2 = "b" * 10
    text = part1 + " " + part2     # slug before cut: "aaa...a~bbb..." (37th char is '~')
    result = slugify(text)
    assert not result.endswith(SEPARATOR)
    assert len(result) <= SLUG_MAX

def test_truncation_result_no_trailing_tilde():
    long_text = "hello world " * 10
    result = slugify(long_text)
    assert len(result) <= SLUG_MAX
    assert not result.endswith(SEPARATOR)


# --- export from package ---

def test_importable_from_package():
    from slugkit import slugify as sf
    assert callable(sf)

def test_slugify_basic_integration():
    assert slugify("The Quick Brown Fox") == "the~quick~brown~fox"
