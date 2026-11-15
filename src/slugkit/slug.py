"""Slug generation utilities."""

import re

SEPARATOR = "~"
SLUG_MAX = 37
EMPTY_SLUG = "n~a"


def slugify(text: str) -> str:
    """Convert *text* to a URL-safe slug.

    Rules:
    - Lowercased.
    - Runs of non-ASCII-alphanumeric characters become a single SEPARATOR (~).
    - Leading/trailing separators are stripped.
    - Truncated to SLUG_MAX characters; trailing separator removed after cut.
    - Empty result returns EMPTY_SLUG.
    """
    lowered = text.lower()
    slug = re.sub(r"[^a-z0-9]+", SEPARATOR, lowered).strip(SEPARATOR)

    if len(slug) > SLUG_MAX:
        slug = slug[:SLUG_MAX].rstrip(SEPARATOR)

    return slug if slug else EMPTY_SLUG
