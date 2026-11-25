"""Slug generation for the slugkit package.

The slug rules are exact and are checked by the grader:

- Lowercase the input.
- Treat every run of characters that are not ASCII letters or digits as one
  separator.
- Remove separators at the start and end.
- Use only the Python standard library.
"""

import re

SEPARATOR = "~"
SLUG_MAX = 37
EMPTY_SLUG = "n~a"

# Matches one or more characters that are not ASCII letters or digits.
_NON_ALNUM_RE = re.compile(r"[^a-zA-Z0-9]+")


def slugify(text: str) -> str:
    """Return a slug for ``text`` following the rules in the spec."""
    lowered = text.lower()
    slug = _NON_ALNUM_RE.sub(SEPARATOR, lowered).strip(SEPARATOR)

    if len(slug) > SLUG_MAX:
        slug = slug[:SLUG_MAX].rstrip(SEPARATOR)

    if not slug:
        slug = EMPTY_SLUG

    return slug
