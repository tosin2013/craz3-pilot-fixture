"""Slug generation utilities."""

import re

SEPARATOR = "~"
SLUG_MAX = 37
EMPTY_SLUG = "n~a"


def slugify(text: str) -> str:
    """Convert *text* to a URL-friendly slug.

    - Lowercases the input.
    - Replaces every run of non-ASCII-alphanumeric characters with SEPARATOR.
    - Strips leading/trailing separators.
    - Truncates to SLUG_MAX characters, then strips any trailing separator.
    - Returns EMPTY_SLUG when the result would otherwise be empty.
    """
    lowered = text.lower()
    slug = re.sub(r"[^a-z0-9]+", SEPARATOR, lowered)
    slug = slug.strip(SEPARATOR)
    if len(slug) > SLUG_MAX:
        slug = slug[:SLUG_MAX].rstrip(SEPARATOR)
    return slug if slug else EMPTY_SLUG
