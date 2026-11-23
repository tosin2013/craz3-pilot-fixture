"""Slug generation for the slugkit package.

Implements the single public helper ``slugify`` and the constants it relies on:

- ``SEPARATOR``  -- the character used to separate word runs (``"~"``).
- ``SLUG_MAX``   -- the maximum length of a slug (``37``).
- ``EMPTY_SLUG`` -- the value returned when a slug would otherwise be empty
  (``"n~a"``).
"""

import re

SEPARATOR = "~"
SLUG_MAX = 37
EMPTY_SLUG = "n~a"

_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    """Return a URL-safe slug for ``text``.

    1. Lowercase the input.
    2. Collapse every run of characters that are not ASCII letters or digits
       into a single ``SEPARATOR``.
    3. Remove separators at the start and end.
    4. Truncate to ``SLUG_MAX`` characters, dropping any trailing separator
       left by the cut.
    5. Return ``EMPTY_SLUG`` when the result would be empty.
    """
    slug = _NON_ALNUM.sub(SEPARATOR, text.lower())
    slug = slug.strip(SEPARATOR)

    if len(slug) > SLUG_MAX:
        slug = slug[:SLUG_MAX].rstrip(SEPARATOR)

    return slug if slug else EMPTY_SLUG
