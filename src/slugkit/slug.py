"""Slug generation (spec 001)."""

import re

SEPARATOR = "~"
SLUG_MAX = 37
EMPTY_SLUG = "n~a"

_SEPARATOR_RE = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    """Return a URL-safe slug for ``text``.

    Rules:
    1. Lowercase the input.
    2. Every run of characters that are not ASCII letters or digits becomes one
       ``SEPARATOR``.
    3. Separators at the start and end are removed.
    4. Slugs longer than ``SLUG_MAX`` are cut to ``SLUG_MAX`` and any trailing
       ``SEPARATOR`` is removed.
    5. An empty result is replaced with ``EMPTY_SLUG``.
    """
    slug = _SEPARATOR_RE.sub(SEPARATOR, text.lower()).strip(SEPARATOR)
    if len(slug) > SLUG_MAX:
        slug = slug[:SLUG_MAX].rstrip(SEPARATOR)
    return slug or EMPTY_SLUG
