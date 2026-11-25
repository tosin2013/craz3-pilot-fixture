"""Unique slug generation for the slugkit package.

Reuses ``slugify`` and the constants from ``slugkit.slug`` rather than
re-implementing them.
"""

from slugkit.slug import SEPARATOR, SLUG_MAX, slugify


def unique_slug(text: str, existing: set[str]) -> str:
    """Return a slug for ``text`` that is not already in ``existing``.

    If ``slugify(text)`` is free, it is returned unchanged. Otherwise numeric
    suffixes (``~2``, ``~3``, …) are appended until a free slug is found. The
    base is shortened as needed so the full result fits within ``SLUG_MAX``.
    ``existing`` is never modified.
    """
    base = slugify(text)
    if base not in existing:
        return base

    n = 2
    while True:
        suffix = SEPARATOR + str(n)
        max_base_len = SLUG_MAX - len(suffix)
        cut_base = base[:max_base_len].rstrip(SEPARATOR)
        candidate = cut_base + suffix
        if candidate not in existing:
            return candidate
        n += 1
