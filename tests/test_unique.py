import pytest
from slugkit import unique_slug, SEPARATOR, SLUG_MAX, EMPTY_SLUG


def test_base_not_taken_returns_base():
    assert unique_slug("hello world", set()) == "hello~world"


def test_base_not_taken_in_non_empty_existing():
    assert unique_slug("hello", {"world", "foo"}) == "hello"


def test_base_taken_returns_suffix_2():
    assert unique_slug("hello", {"hello"}) == "hello~2"


def test_base_and_2_taken_returns_suffix_3():
    assert unique_slug("hello", {"hello", "hello~2"}) == "hello~3"


def test_multiple_suffixes_taken():
    existing = {"hello", "hello~2", "hello~3", "hello~4"}
    assert unique_slug("hello", existing) == "hello~5"


def test_existing_not_modified():
    existing = {"abc"}
    unique_slug("abc", existing)
    assert existing == {"abc"}


def test_empty_slug_base_not_taken():
    assert unique_slug("", set()) == EMPTY_SLUG


def test_empty_slug_base_taken_returns_suffix():
    result = unique_slug("", {EMPTY_SLUG})
    assert result == EMPTY_SLUG + "~2"


def test_empty_slug_base_and_2_taken():
    result = unique_slug("", {EMPTY_SLUG, EMPTY_SLUG + "~2"})
    assert result == EMPTY_SLUG + "~3"


def test_result_at_most_slug_max():
    # base of exactly SLUG_MAX chars; with suffix it must still be <= SLUG_MAX
    long_text = "a" * 50
    base = "a" * SLUG_MAX  # slugify truncates to this
    existing = {base}
    result = unique_slug(long_text, existing)
    assert len(result) <= SLUG_MAX


def test_truncated_base_no_trailing_separator():
    # Build a text whose slug is exactly SLUG_MAX chars; force suffix path
    long_text = "a" * 50
    base = "a" * SLUG_MAX
    existing = {base}
    result = unique_slug(long_text, existing)
    # The part before the suffix must not end with SEPARATOR
    suffix = "~2"
    assert result.endswith(suffix)
    trimmed_base = result[: -len(suffix)]
    assert not trimmed_base.endswith(SEPARATOR)


def test_base_with_separator_at_cut_point():
    # Craft a base that ends with SEPARATOR right at the cut point
    # base = 'a' * 35 + '~' + 'b'  -> len 37 (SLUG_MAX)
    # suffix '~2' len=2 -> max_base_len = 35 -> base[:35] = 'a'*35 -> rstrip('~') = 'a'*35
    base_text = "a" * 35 + " b"  # slugify -> 'a'*35 + '~b', len=37
    from slugkit import slugify
    base = slugify(base_text)
    assert len(base) == SLUG_MAX
    existing = {base}
    result = unique_slug(base_text, existing)
    assert len(result) <= SLUG_MAX
    assert not result[: result.rfind("~2")].endswith(SEPARATOR) if "~2" in result else True


def test_suffix_separator_matches_constant():
    result = unique_slug("abc", {"abc"})
    assert result == "abc" + SEPARATOR + "2"


def test_does_not_reimplement_slugify():
    # unique_slug must produce the same base as slugify
    from slugkit import slugify
    text = "Hello, World!"
    base = slugify(text)
    result = unique_slug(text, set())
    assert result == base


def test_large_n_suffix():
    existing = {"abc"} | {f"abc{SEPARATOR}{n}" for n in range(2, 102)}
    result = unique_slug("abc", existing)
    assert result == f"abc{SEPARATOR}102"
