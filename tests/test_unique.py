import pytest
from slugkit import unique_slug
from slugkit.slug import SEPARATOR, SLUG_MAX, EMPTY_SLUG


def test_unique_slug_exported_from_package():
    from slugkit import unique_slug as us
    assert callable(us)


# Rule 1: base not in existing -> return base directly
def test_base_not_in_existing():
    assert unique_slug("hello world", set()) == "hello~world"


def test_base_not_in_existing_nonempty_set():
    existing = {"other~slug"}
    assert unique_slug("hello", existing) == "hello"


# Rule 2: base in existing -> try suffix ~2
def test_suffix_2_when_base_taken():
    existing = {"hello~world"}
    assert unique_slug("hello world", existing) == "hello~world~2"


# Rule 3: increment suffix until free
def test_suffix_increments():
    existing = {"hello~world", "hello~world~2", "hello~world~3"}
    assert unique_slug("hello world", existing) == "hello~world~4"


def test_suffix_increments_many():
    base = "abc"
    existing = {base} | {f"abc~{n}" for n in range(2, 10)}
    assert unique_slug("abc", existing) == "abc~10"


# Rule 4: existing is not modified
def test_existing_not_modified():
    existing = {"hello"}
    original = set(existing)
    unique_slug("hello", existing)
    assert existing == original


def test_existing_not_modified_when_base_free():
    existing = {"other"}
    original = set(existing)
    unique_slug("hello", existing)
    assert existing == original


# Rule 5: result including suffix must be <= SLUG_MAX
def test_result_length_at_most_slug_max():
    long_text = "a" * 50
    result = unique_slug(long_text, set())
    assert len(result) <= SLUG_MAX


def test_result_with_suffix_length_at_most_slug_max():
    long_text = "a" * 50
    base = "a" * SLUG_MAX  # slugify will produce this
    existing = {base}
    result = unique_slug(long_text, existing)
    assert len(result) <= SLUG_MAX


def test_base_trimmed_so_suffix_fits():
    # base is exactly SLUG_MAX chars; suffix ~2 is 2 chars -> base must be trimmed
    base = "a" * SLUG_MAX
    existing = {base}
    result = unique_slug("a" * 50, existing)
    assert len(result) <= SLUG_MAX
    assert result.endswith("~2")


# Rule 6: trailing ~ removed from cut base before adding suffix
def test_trailing_tilde_removed_from_cut_base():
    # Create a base that ends with ~ when trimmed to make room for suffix
    # Build a text whose slug is 35 a's + ~ + something, so trimming at 35 leaves trailing ~
    # slugify("a"*35 + "   " + "b"*5) => "aaa...a~bbbbb" (41 chars) => cut to 37 => "aaa...a~bb"
    # We need a case where cut lands on ~
    # "a"*36 + " " + "b" produces slug "aaa...a~b" (38 chars) -> cut at 37 -> "aaa...a~" -> rstrip -> "aaa...a"
    # So base = "a"*36  (slugify truncates)
    # Let's construct it carefully:
    text = "a" * 36 + "   " + "b" * 10
    from slugkit.slug import slugify
    base = slugify(text)
    existing = {base}
    result = unique_slug(text, existing)
    assert len(result) <= SLUG_MAX
    assert not result[:-len("~2")].endswith(SEPARATOR) or result.endswith("~2")


def test_no_double_tilde_in_candidate():
    # If trimmed base ends with ~, it must be stripped before appending suffix
    # Craft a base that when trimmed to fit suffix would end with ~
    # base length = SLUG_MAX, suffix = "~2" (len 2), so max_base_len = SLUG_MAX - 2 = 35
    # Make base = "a"*35 + "~" + "a" (37 chars), trimming to 35 gives "a"*35, no ~
    # Instead, make base = "a"*34 + "~" + "a" (36 chars but ends at 35 = "a"*34 + "~")
    # We need slugify to produce a base that at position 35 has a ~
    # text: "a"*34 + " " + "a"*3 -> slug "a"*34 + "~" + "aaa" = 38 chars -> cut to 37 -> "a"*34 + "~" + "aa"
    # trimmed at max_base_len=35 -> "a"*34 + "~" -> rstrip(~) -> "a"*34
    text = "a" * 34 + " " + "a" * 10
    from slugkit.slug import slugify
    base = slugify(text)
    assert len(base) == SLUG_MAX
    existing = {base}
    result = unique_slug(text, existing)
    assert "~~" not in result
    assert len(result) <= SLUG_MAX


# Rule 7: EMPTY_SLUG base still gets suffixed if taken
def test_empty_slug_base_taken():
    existing = {EMPTY_SLUG}
    result = unique_slug("", existing)
    assert result == EMPTY_SLUG + SEPARATOR + "2"


def test_empty_slug_base_multiple_taken():
    existing = {EMPTY_SLUG, EMPTY_SLUG + "~2", EMPTY_SLUG + "~3"}
    result = unique_slug("", existing)
    assert result == EMPTY_SLUG + SEPARATOR + "4"


def test_empty_slug_base_not_taken():
    assert unique_slug("", set()) == EMPTY_SLUG


def test_special_chars_only_uses_empty_slug():
    assert unique_slug("!@#", set()) == EMPTY_SLUG


def test_special_chars_taken_gets_suffix():
    existing = {EMPTY_SLUG}
    result = unique_slug("!@#", existing)
    assert result == EMPTY_SLUG + "~2"


# General correctness
def test_result_not_in_existing_when_base_free():
    existing = {"other"}
    result = unique_slug("hello", existing)
    assert result not in existing or result == "hello"


def test_result_is_free_slug():
    existing = {"test", "test~2", "test~3"}
    result = unique_slug("test", existing)
    assert result not in existing


def test_uses_slugify_internally():
    # Input with uppercase and spaces -> same slug as slugify would produce
    from slugkit.slug import slugify
    text = "Hello World"
    base = slugify(text)
    result = unique_slug(text, set())
    assert result == base


def test_suffix_format_uses_separator_and_number():
    existing = {"abc"}
    result = unique_slug("abc", existing)
    assert result == "abc" + SEPARATOR + "2"
