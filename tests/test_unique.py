"""Tests for unique_slug (spec 002)."""

import pytest
from slugkit import unique_slug
from slugkit.slug import SEPARATOR, SLUG_MAX, EMPTY_SLUG


class TestBasicBehaviour:
    def test_free_slug_returned_as_is(self):
        assert unique_slug("hello world", set()) == "hello~world"

    def test_free_slug_not_in_existing(self):
        existing = {"other~slug"}
        assert unique_slug("hello", existing) == "hello"

    def test_taken_slug_gets_suffix_2(self):
        existing = {"hello~world"}
        assert unique_slug("hello world", existing) == "hello~world~2"

    def test_taken_slug_suffix_increments(self):
        existing = {"hello~world", "hello~world~2", "hello~world~3"}
        assert unique_slug("hello world", existing) == "hello~world~4"

    def test_existing_not_modified(self):
        existing = {"abc"}
        original = set(existing)
        unique_slug("abc", existing)
        assert existing == original


class TestSuffixFormat:
    def test_suffix_uses_separator(self):
        base = "abc"
        existing = {base}
        result = unique_slug("abc", existing)
        assert result == f"abc{SEPARATOR}2"

    def test_suffix_increments_from_2(self):
        base = "abc"
        existing = {base, f"abc{SEPARATOR}2"}
        assert unique_slug("abc", existing) == f"abc{SEPARATOR}3"

    def test_suffix_continues_incrementing(self):
        base = "z"
        existing = {base} | {f"z{SEPARATOR}{n}" for n in range(2, 10)}
        assert unique_slug("z", existing) == f"z{SEPARATOR}10"


class TestLengthConstraint:
    def test_result_at_most_slug_max(self):
        # Base slug that is exactly SLUG_MAX characters
        long_text = "a" * SLUG_MAX
        existing = {unique_slug(long_text, set())}
        result = unique_slug(long_text, existing)
        assert len(result) <= SLUG_MAX

    def test_base_trimmed_to_fit_suffix(self):
        # Craft a base that is exactly SLUG_MAX chars; with suffix ~2 it would overflow
        base = "a" * SLUG_MAX
        # slugify will truncate to SLUG_MAX
        from slugkit.slug import slugify
        base_slug = slugify(base)
        assert len(base_slug) == SLUG_MAX

        existing = {base_slug}
        result = unique_slug(base, existing)
        assert len(result) <= SLUG_MAX
        assert result.endswith(f"{SEPARATOR}2")

    def test_no_trailing_separator_before_suffix(self):
        # Build a base that when trimmed ends with SEPARATOR; ensure it's stripped
        # Use a slug whose trimmed form would end with ~
        # "a" * (SLUG_MAX - 2) + "~x" -> after slugify: "a"*(SLUG_MAX-2)~x truncated
        # Easier: craft text so trimmed base ends with SEPARATOR
        # slug of "a~b~c~d..." repeated to fill SLUG_MAX
        # Let's construct directly: a base that is SLUG_MAX chars with last char ~
        from slugkit.slug import slugify

        # We need a slug where, when we cut to (SLUG_MAX - len("~2")), the last char is ~
        suffix = f"{SEPARATOR}2"
        cut_len = SLUG_MAX - len(suffix)  # 35

        # Build text so that slugify gives a slug where char at index cut_len-1 is ~
        # e.g. "a"*(cut_len-1) + " " + "b" + extra chars to reach SLUG_MAX
        text = "a" * (cut_len - 1) + " b" + "c" * (SLUG_MAX - cut_len)
        slug = slugify(text)
        # The slug should be exactly SLUG_MAX chars
        assert len(slug) == SLUG_MAX
        # The char at position cut_len-1 (0-indexed cut_len-1) should be ~
        assert slug[cut_len - 1] == SEPARATOR, f"Expected ~ at index {cut_len-1}, got: {slug!r}"

        existing = {slug}
        result = unique_slug(text, existing)
        assert len(result) <= SLUG_MAX
        # Result should not contain ~~ (trailing ~ from trimmed base + separator)
        assert "~~" not in result
        assert result.endswith(suffix)


class TestEmptySlugFallback:
    def test_empty_slug_free(self):
        assert unique_slug("", set()) == EMPTY_SLUG

    def test_empty_slug_taken_gets_suffix(self):
        existing = {EMPTY_SLUG}
        result = unique_slug("", existing)
        assert result == f"{EMPTY_SLUG}{SEPARATOR}2"

    def test_empty_slug_multiple_taken(self):
        existing = {EMPTY_SLUG, f"{EMPTY_SLUG}{SEPARATOR}2"}
        result = unique_slug("", existing)
        assert result == f"{EMPTY_SLUG}{SEPARATOR}3"


class TestReusesSlugify:
    def test_uses_slugify_normalisation(self):
        # unique_slug should apply the same normalisation as slugify
        from slugkit.slug import slugify
        result = unique_slug("Hello, World!", set())
        assert result == slugify("Hello, World!")

    def test_unicode_handled_via_slugify(self):
        from slugkit.slug import slugify
        text = "Ünïcödé"
        result = unique_slug(text, set())
        assert result == slugify(text)
