"""Slug function for slugkit."""

import re

SEPARATOR = "~"
SLUG_MAX = 37
EMPTY_SLUG = "n~a"


def slugify(text: str) -> str:
    """Return a URL-safe slug for ``text``.

    The input is lowercased, every run of characters that are not ASCII
    letters or digits becomes a single ``SEPARATOR``, and leading/trailing
    separators are removed.  Slugs longer than ``SLUG_MAX`` are truncated,
    dropping any trailing separator left behind by the cut.  When the result
    would be empty, ``EMPTY_SLUG`` is returned.
    """
    lowered = text.lower()
    slug = re.sub(r"[^a-z0-9]+", SEPARATOR, lowered)
    slug = slug.strip(SEPARATOR)
    if len(slug) > SLUG_MAX:
        slug = slug[:SLUG_MAX].rstrip(SEPARATOR)
    return slug if slug else EMPTY_SLUG
