import pytest
from slugkit import unique_slug
from slugkit.slug import SEPARATOR, SLUG_MAX, EMPTY_SLUG


def test_base_not_in_existing_returns_base():
    assert unique_slug("Hello World", set()) == "hello~world"


def test_base_not_in_existing_no_suffix():
    result = unique_slug("foo", {"bar", "baz"})
    assert result == "foo"


def test_base_taken_returns_suffix_2():
    result = unique_slug("abc", {"abc"})
    assert result == "abc~2"


def test_base_and_2_taken_returns_suffix_3():
    result = unique_slug("abc", {"abc", "abc~2"})
    assert result == "abc~3"


def test_multiple_suffixes_skipped():
    existing = {"abc", "abc~2", "abc~3", "abc~4"}
    result = unique_slug("abc", existing)
    assert result == "abc~5"


def test_does_not_modify_existing():
    existing = {"abc"}
    original = set(existing)
    unique_slug("abc", existing)
    assert existing == original


def test_suffix_format_uses_separator_and_number():
    result = unique_slug("abc", {"abc"})
    assert result == "abc" + SEPARATOR + "2"


def test_result_at_most_slug_max():
    # long base that fills SLUG_MAX, then taken
    long_text = "a" * 50
    base = "a" * SLUG_MAX  # slugify truncates to SLUG_MAX
    existing = {base}
    result = unique_slug(long_text, existing)
    assert len(result) <= SLUG_MAX


def test_long_base_trimmed_for_suffix():
    # base is exactly SLUG_MAX chars; adding suffix requires trimming
    long_text = "a" * 50
    base = "a" * SLUG_MAX
    existing = {base}
    result = unique_slug(long_text, existing)
    suffix = SEPARATOR + "2"
    assert result.endswith(suffix)
    assert len(result) <= SLUG_MAX


def test_no_trailing_separator_before_suffix():
    # Construct a base where trimming would leave a trailing SEPARATOR
    # base = "a" * 35 + "~b" (len=38 -> truncated to 37 = "a"*35+"~b" -> rstrip gives "a"*35+"~b"[0:2])
    # We want trimming to cut mid-separator; let's build a specific case.
    # base of length 37, suffix "~2" (len 2), so max_base_len = 35
    # If base[35] == "~", trimming to 35 gives trailing "~", which must be stripped.
    base_chars = "a" * 34 + SEPARATOR + "b" * 2  # len=37
    # Create text that slugifies to this:
    text = "a" * 34 + " " + "b" * 2 + " " + "x" * 20  # slugify truncates to 37
    from slugkit.slug import slugify
    actual_base = slugify(text)
    existing = {actual_base}
    result = unique_slug(text, existing)
    assert len(result) <= SLUG_MAX
    assert not result[: result.rfind(SEPARATOR + "2")].endswith(SEPARATOR)


def test_empty_slug_base_not_taken():
    result = unique_slug("", set())
    assert result == EMPTY_SLUG


def test_empty_slug_base_taken_uses_suffix():
    result = unique_slug("", {EMPTY_SLUG})
    assert result == EMPTY_SLUG + SEPARATOR + "2"


def test_empty_slug_base_multiple_taken():
    existing = {EMPTY_SLUG, EMPTY_SLUG + SEPARATOR + "2"}
    result = unique_slug("", existing)
    assert result == EMPTY_SLUG + SEPARATOR + "3"


def test_import_from_slugkit():
    from slugkit import unique_slug as us
    assert us("hello", set()) == "hello"


def test_uses_slugify_internally():
    # unique_slug should apply the same transformations as slugify
    assert unique_slug("Hello World!", set()) == "hello~world"


def test_suffix_starts_at_2_not_1():
    result = unique_slug("abc", {"abc"})
    assert result == "abc~2"
    assert result != "abc~1"


def test_result_length_with_suffix_exactly_slug_max():
    # suffix "~2" is 2 chars; base can be SLUG_MAX - 2 = 35 chars max when trimmed
    suffix = SEPARATOR + "2"
    max_base = SLUG_MAX - len(suffix)  # 35
    text = "a" * 50
    base = "a" * SLUG_MAX
    existing = {base}
    result = unique_slug(text, existing)
    assert len(result) <= SLUG_MAX
    expected_trimmed_base = ("a" * SLUG_MAX)[:max_base].rstrip(SEPARATOR)
    assert result == expected_trimmed_base + suffix
