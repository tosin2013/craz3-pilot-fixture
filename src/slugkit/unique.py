"""Unique slug generation utilities."""

from .slug import slugify, SEPARATOR, SLUG_MAX


def unique_slug(text: str, existing: set[str]) -> str:
    """Return a slug derived from text that is not in existing.

    Appends SEPARATOR + str(n) for n = 2, 3, 4, … until a free slug is found.
    The full result is always at most SLUG_MAX characters.
    """
    base = slugify(text)
    if base not in existing:
        return base

    n = 2
    while True:
        suffix = SEPARATOR + str(n)
        max_base_len = SLUG_MAX - len(suffix)
        trimmed = base[:max_base_len].rstrip(SEPARATOR)
        candidate = trimmed + suffix
        if candidate not in existing:
            return candidate
        n += 1
