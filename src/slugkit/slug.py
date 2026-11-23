"""Slugification for the slugkit package."""

import re

SEPARATOR = "~"
SLUG_MAX = 37
EMPTY_SLUG = "n~a"


def slugify(text: str) -> str:
    """Turn ``text`` into a slug.

    Rules (see spec 001):
      1. Lowercase the input.
      2. Collapse every run of characters that are not ASCII letters or digits
         into a single ``SEPARATOR``.
      3. Remove separators at the start and end.
      4. Truncate to ``SLUG_MAX`` characters, then strip any trailing separator.
      5. Return ``EMPTY_SLUG`` when the result would be empty.
    """
    slug = re.sub(r"[^a-z0-9]+", SEPARATOR, text.lower())
    slug = slug.strip(SEPARATOR)

    if len(slug) > SLUG_MAX:
        slug = slug[:SLUG_MAX].rstrip(SEPARATOR)

    return slug if slug else EMPTY_SLUG
