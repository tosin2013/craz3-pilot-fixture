"""Slug generation for the slugkit package."""

import re

SEPARATOR = "~"
SLUG_MAX = 37
EMPTY_SLUG = "n~a"


def slugify(text: str) -> str:
    """Return a normalized slug for ``text``.

    The input is lowercased, every run of characters that are not ASCII
    letters or digits becomes a single ``SEPARATOR``, and separators at the
    start and end are removed. Long slugs are truncated to ``SLUG_MAX``
    characters (dropping any trailing separator), and an empty result falls
    back to ``EMPTY_SLUG``.
    """
    slug = re.sub(r"[^a-zA-Z0-9]+", SEPARATOR, text.lower())
    slug = slug.strip(SEPARATOR)

    if len(slug) > SLUG_MAX:
        slug = slug[:SLUG_MAX].rstrip(SEPARATOR)

    if not slug:
        slug = EMPTY_SLUG

    return slug
