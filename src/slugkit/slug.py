"""Slug generation utilities."""

import re

SEPARATOR = "~"
SLUG_MAX = 37
EMPTY_SLUG = "n~a"


def slugify(text: str) -> str:
    """Convert text to a slug using tilde as separator."""
    lowered = text.lower()
    # Replace runs of non-alphanumeric characters with the separator
    slug = re.sub(r"[^a-z0-9]+", SEPARATOR, lowered)
    # Strip leading/trailing separators
    slug = slug.strip(SEPARATOR)
    # Truncate to SLUG_MAX and remove trailing separator
    if len(slug) > SLUG_MAX:
        slug = slug[:SLUG_MAX].rstrip(SEPARATOR)
    # Return fallback when result is empty
    return slug if slug else EMPTY_SLUG
