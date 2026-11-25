"""Spec 001: slugify."""

import re

SEPARATOR = "~"
SLUG_MAX = 37
EMPTY_SLUG = "n~a"

_NON_ALNUM = re.compile(r"[^a-zA-Z0-9]+")


def slugify(text: str) -> str:
    """Return a slug for *text*.

    Lowercases the input, replaces every run of characters that are not ASCII
    letters or digits with a single separator, and strips separators from the
    start and end.
    """
    slug = _NON_ALNUM.sub(SEPARATOR, text.lower()).strip(SEPARATOR)
    if len(slug) > SLUG_MAX:
        slug = slug[:SLUG_MAX].rstrip(SEPARATOR)
    if not slug:
        slug = EMPTY_SLUG
    return slug
