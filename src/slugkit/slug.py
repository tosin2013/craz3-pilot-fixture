"""Slug generation (Spec 001)."""

import re

SEPARATOR = "~"
SLUG_MAX = 37
EMPTY_SLUG = "n~a"


def slugify(text: str) -> str:
    """Return a URL-friendly slug for ``text``.

    Rules (see spec 001):
    - lowercase the input;
    - collapse every run of non-ASCII-letter/digit characters into one ``SEPARATOR``;
    - strip separators from the start and end;
    - truncate to ``SLUG_MAX`` characters, then strip any trailing separator;
    - return ``EMPTY_SLUG`` when the result would be empty.
    """
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9]+", SEPARATOR, slug)
    slug = slug.strip(SEPARATOR)
    if len(slug) > SLUG_MAX:
        slug = slug[:SLUG_MAX].rstrip(SEPARATOR)
    return slug if slug else EMPTY_SLUG
