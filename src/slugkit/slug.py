"""Slug generation for the slugkit package (spec 001)."""

import re

# Separator placed between runs of non-alphanumeric characters.
SEPARATOR = "~"

# Maximum length of a generated slug, in characters.
SLUG_MAX = 37

# Literal value returned when the slug would otherwise be empty.
EMPTY_SLUG = "n~a"

# Matches one or more characters that are not ASCII letters or digits.
_NON_ALNUM = re.compile(r"[^a-zA-Z0-9]+")


def slugify(text: str) -> str:
    """Return a URL-friendly slug for ``text``.

    Rules:
    1. Lowercase the input.
    2. Replace every run of non-ASCII-letter/digit characters with ``SEPARATOR``.
    3. Remove separators at the start and end.
    4. Truncate to ``SLUG_MAX`` characters, then drop any trailing separator.
    5. Return ``EMPTY_SLUG`` when the result would be empty.
    """
    lowered = text.lower()
    slug = SEPARATOR.join(_NON_ALNUM.split(lowered))
    slug = slug.strip(SEPARATOR)

    if not slug:
        return EMPTY_SLUG

    if len(slug) > SLUG_MAX:
        slug = slug[:SLUG_MAX].rstrip(SEPARATOR)

    return slug
