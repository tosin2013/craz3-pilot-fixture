import pytest
from slugkit import unique_slug, SEPARATOR, SLUG_MAX, EMPTY_SLUG


def test_base_not_in_existing_returns_base():
    assert unique_slug("Hello World", set()) == "hello~world"


def test_base_in_existing_returns_suffix_2():
    assert unique_slug("hello", {"hello"}) == "hello~2"


def test_base_and_suffix_2_taken_returns_suffix_3():
    assert unique_slug("hello", {"hello", "hello~2"}) == "hello~3"


def test_multiple_suffixes_taken():
    existing = {"hello", "hello~2", "hello~3", "hello~4"}
    assert unique_slug("hello", existing) == "hello~5"


def test_does_not_modify_existing():
    existing = {"hello"}
    original = set(existing)
    unique_slug("hello", existing)
    assert existing == original


def test_empty_slug_not_taken():
    assert unique_slug("!!!", set()) == EMPTY_SLUG


def test_empty_slug_taken_gets_suffix():
    result = unique_slug("!!!", {EMPTY_SLUG})
    assert result == EMPTY_SLUG + "~2"


def test_empty_slug_multiple_suffixes_taken():
    existing = {EMPTY_SLUG, EMPTY_SLUG + "~2", EMPTY_SLUG + "~3"}
    assert unique_slug("!!!", existing) == EMPTY_SLUG + "~4"


def test_result_at_most_slug_max_chars():
    # Base that fills SLUG_MAX exactly
    long_text = "a" * SLUG_MAX
    base = "a" * SLUG_MAX
    existing = {base}
    result = unique_slug(long_text, existing)
    assert len(result) <= SLUG_MAX


def test_long_base_trimmed_before_suffix():
    # Create a text whose slug is exactly SLUG_MAX chars
    long_text = "a" * SLUG_MAX
    base = "a" * SLUG_MAX
    existing = {base}
    result = unique_slug(long_text, existing)
    suffix = SEPARATOR + "2"
    expected_base = base[: SLUG_MAX - len(suffix)].rstrip(SEPARATOR)
    assert result == expected_base + suffix


def test_trailing_separator_stripped_from_cut_base():
    # Build a base that when cut ends with SEPARATOR
    # SLUG_MAX = 37, suffix "~2" len = 2, so we need base[:35] to end with "~"
    # Construct: 34 'a's + '~' + something to make it longer than 37
    text_base = "a" * 34 + "~" + "b" * 10  # slug: 34a + ~ + 10b = 45 chars, cut at 37 -> "aaa...a~" (35 chars), strip -> 34 'a's
    # The slug of this will be: lowercase, non-alnum replaced by ~
    # "a"*34 + "~" + "b"*10 is already valid slug chars
    # slugify truncates to 37 chars, rstrips ~
    from slugkit import slugify
    base = slugify(text_base)
    existing = {base}
    result = unique_slug(text_base, existing)
    assert len(result) <= SLUG_MAX
    # suffix is ~2
    suffix = SEPARATOR + "2"
    assert result.endswith(suffix)
    # the part before suffix should not end with SEPARATOR
    prefix = result[: -len(suffix)]
    assert not prefix.endswith(SEPARATOR)


def test_suffix_separator_format():
    # Suffix must be SEPARATOR + str(n)
    result = unique_slug("test", {"test"})
    assert result == "test" + SEPARATOR + "2"


def test_no_collision_returns_immediately():
    # If slug is free, return it without checking for suffixes
    result = unique_slug("free-slug", set())
    assert result == "free~slug"
