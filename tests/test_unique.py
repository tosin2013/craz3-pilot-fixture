"""Tests for unique_slug (spec 002)."""

import pytest
from slugkit import unique_slug, SEPARATOR, SLUG_MAX, EMPTY_SLUG


class TestBasicBehaviour:
    def test_free_base_returned_as_is(self):
        assert unique_slug("hello world", set()) == "hello~world"

    def test_existing_set_not_modified(self):
        existing = {"hello~world"}
        original = set(existing)
        unique_slug("hello world", existing)
        assert existing == original

    def test_first_collision_gets_suffix_2(self):
        base = "hello~world"
        assert unique_slug("hello world", {base}) == f"{base}{SEPARATOR}2"

    def test_second_collision_gets_suffix_3(self):
        base = "hello~world"
        existing = {base, f"{base}{SEPARATOR}2"}
        assert unique_slug("hello world", existing) == f"{base}{SEPARATOR}3"

    def test_multiple_collisions(self):
        base = "abc"
        existing = {base, f"{base}{SEPARATOR}2", f"{base}{SEPARATOR}3"}
        assert unique_slug("abc", existing) == f"{base}{SEPARATOR}4"


class TestSuffixFormat:
    def test_suffix_separator_is_tilde(self):
        base = "x"
        result = unique_slug("x", {base})
        assert result == "x~2"

    def test_suffix_starts_at_2(self):
        result = unique_slug("test", {"test"})
        assert result.endswith(f"{SEPARATOR}2")


class TestMaxLength:
    def test_result_never_exceeds_slug_max(self):
        # Build a long base slug (SLUG_MAX chars) and make it collide
        long_text = "a" * SLUG_MAX
        base = "a" * SLUG_MAX  # slugify keeps it at SLUG_MAX
        existing = {base}
        result = unique_slug(long_text, existing)
        assert len(result) <= SLUG_MAX

    def test_base_trimmed_to_fit_suffix(self):
        # Base is exactly SLUG_MAX; with suffix "~2" (2 chars) base must be trimmed
        long_text = "a" * SLUG_MAX
        base = "a" * SLUG_MAX
        existing = {base}
        result = unique_slug(long_text, existing)
        suffix = f"{SEPARATOR}2"
        # The result should end with the suffix
        assert result.endswith(suffix)
        assert len(result) <= SLUG_MAX

    def test_trailing_separator_stripped_from_trimmed_base(self):
        # Craft a slug whose trim point lands on a SEPARATOR character
        # Base: "a" * (SLUG_MAX - 1) + "~"  — but slugify strips trailing ~,
        # so we need a base where the character at the trim index is "~".
        # Use a base like "aaa...a~bbb" so trimming exposes a trailing "~".
        # SLUG_MAX=37, suffix "~2" is 2 chars, so trimmed base length = 35.
        # Build text so slugify gives: "a"*34 + "~" + "b"*2  (len=37)
        # After trim to 35: "a"*34 + "~"  -> rstrip("~") -> "a"*34
        inner = "a" * 34 + " " + "b" * 2  # slugify -> "a"*34 + "~" + "b"*2
        from slugkit import slugify
        base = slugify(inner)
        assert len(base) == SLUG_MAX
        assert base[34] == SEPARATOR  # trim point for suffix "~2"

        existing = {base}
        result = unique_slug(inner, existing)
        assert len(result) <= SLUG_MAX
        assert not result[: SLUG_MAX - 2].endswith(SEPARATOR + SEPARATOR)
        assert result.endswith(f"{SEPARATOR}2")


class TestEmptySlug:
    def test_empty_slug_free(self):
        assert unique_slug("!!!!", set()) == EMPTY_SLUG

    def test_empty_slug_taken_gets_suffix(self):
        existing = {EMPTY_SLUG}
        result = unique_slug("!!!!", existing)
        assert result == f"{EMPTY_SLUG}{SEPARATOR}2"

    def test_empty_slug_multiple_collisions(self):
        existing = {EMPTY_SLUG, f"{EMPTY_SLUG}{SEPARATOR}2"}
        result = unique_slug("!!!!", existing)
        assert result == f"{EMPTY_SLUG}{SEPARATOR}3"


class TestReusesSlugify:
    def test_uses_slugify_normalisation(self):
        # unique_slug should apply the same normalisation as slugify
        from slugkit import slugify
        result = unique_slug("Hello World!", set())
        assert result == slugify("Hello World!")

    def test_case_insensitive(self):
        result = unique_slug("HELLO", set())
        assert result == "hello"
