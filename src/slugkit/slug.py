"""Slug function (spec 001)."""

import re

SEPARATOR = "~"
SLUG_MAX = 37
EMPTY_SLUG = "n~a"

_NON_ALNUM_RE = re.compile(r"[^a-zA-Z0-9]+")


def slugify(text: str) -> str:
    """Return a URL-safe slug for ``text``.

    Rules:
    1. Lowercase the input.
    2. Treat every run of non-ASCII-letter/digit characters as one separator.
    3. Remove separators at the start and end.
    4. Truncate to ``SLUG_MAX``, then remove any trailing separator.
    5. Return ``EMPTY_SLUG`` when the result would be empty.
    """
    slug = _NON_ALNUM_RE.sub(SEPARATOR, text.lower()).strip(SEPARATOR)
    if len(slug) > SLUG_MAX:
        slug = slug[:SLUG_MAX].rstrip(SEPARATOR)
    if not slug:
        return EMPTY_SLUG
    return slug
