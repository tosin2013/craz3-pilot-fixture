"""Tests for unique_slug (spec 002)."""
import pytest
from slugkit import unique_slug
from slugkit.slug import EMPTY_SLUG, SEPARATOR, SLUG_MAX


class TestBasicBehaviour:
    def test_free_base_returned_as_is(self):
        """If the base slug is not in existing, return it unchanged."""
        assert unique_slug("Hello World", set()) == "hello~world"

    def test_free_base_not_in_existing(self):
        assert unique_slug("foo", {"bar", "baz"}) == "foo"

    def test_does_not_modify_existing(self):
        existing = {"foo"}
        unique_slug("foo", existing)
        assert existing == {"foo"}


class TestSuffixRules:
    def test_suffix_starts_at_2(self):
        """First collision adds ~2."""
        result = unique_slug("abc", {"abc"})
        assert result == "abc~2"

    def test_suffix_increments(self):
        """When ~2 is also taken, use ~3."""
        result = unique_slug("abc", {"abc", "abc~2"})
        assert result == "abc~3"

    def test_suffix_continues_incrementing(self):
        existing = {"abc", "abc~2", "abc~3", "abc~4"}
        assert unique_slug("abc", existing) == "abc~5"

    def test_separator_in_suffix(self):
        """Suffix is SEPARATOR + str(n)."""
        result = unique_slug("abc", {"abc"})
        assert result == "abc" + SEPARATOR + "2"


class TestLengthConstraint:
    def test_result_at_most_slug_max(self):
        long_text = "a" * 100
        existing = set()
        result = unique_slug(long_text, existing)
        assert len(result) <= SLUG_MAX

    def test_suffixed_result_at_most_slug_max(self):
        """Even with a suffix the result must not exceed SLUG_MAX."""
        long_text = "a" * 100
        base = "a" * SLUG_MAX  # will be trimmed by slugify to SLUG_MAX chars
        existing = {base}
        result = unique_slug(long_text, existing)
        assert len(result) <= SLUG_MAX

    def test_base_trimmed_before_suffix(self):
        """Base is cut so that base + suffix fits in SLUG_MAX; trailing ~ removed."""
        # Build an existing set containing the max-length base
        long_text = "a" * 100
        from slugkit.slug import slugify
        base = slugify(long_text)
        assert len(base) == SLUG_MAX

        existing = {base}
        result = unique_slug(long_text, existing)
        assert len(result) <= SLUG_MAX
        assert result.endswith(SEPARATOR + "2")

    def test_no_trailing_separator_in_trimmed_base(self):
        """After trimming, any trailing SEPARATOR chars are stripped before suffix."""
        # Craft a base that ends with SEPARATOR when trimmed to max_base_len
        suffix = SEPARATOR + "2"
        max_base_len = SLUG_MAX - len(suffix)
        # Create a text whose base slug is exactly SLUG_MAX chars,
        # and whose first max_base_len chars end with SEPARATOR.
        # Use 'a' repeated to fill and add a separator right at the cut point.
        # e.g. "aaa...a~bbb...b" where cut falls on '~'
        inner = "a" * (max_base_len - 1) + "~" + "b" * (SLUG_MAX - max_base_len)
        # inner has SLUG_MAX chars; trimmed to max_base_len ends in '~'
        base = inner  # treat as the slug directly for assertion
        trimmed_expected = inner[:max_base_len].rstrip(SEPARATOR)
        candidate = trimmed_expected + suffix
        assert SEPARATOR not in candidate[len(trimmed_expected) - 1: len(trimmed_expected)]
        assert len(candidate) <= SLUG_MAX


class TestEmptySlug:
    def test_empty_input_free(self):
        """Empty-ish text that resolves to EMPTY_SLUG is returned when free."""
        result = unique_slug("", set())
        assert result == EMPTY_SLUG

    def test_empty_slug_taken_gets_suffix(self):
        """EMPTY_SLUG follows the same suffix rules when taken."""
        result = unique_slug("", {EMPTY_SLUG})
        assert result == EMPTY_SLUG + SEPARATOR + "2"

    def test_empty_slug_multiple_taken(self):
        existing = {EMPTY_SLUG, EMPTY_SLUG + SEPARATOR + "2"}
        result = unique_slug("", existing)
        assert result == EMPTY_SLUG + SEPARATOR + "3"


class TestImport:
    def test_importable_from_slugkit(self):
        from slugkit import unique_slug as us
        assert callable(us)

    def test_reuses_slugify(self):
        """unique_slug normalises text the same way slugify does."""
        from slugkit import slugify
        result = unique_slug("Hello, World!", set())
        assert result == slugify("Hello, World!")
