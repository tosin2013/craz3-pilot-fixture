"""Unique slug generation for the slugkit package."""

from .slug import SEPARATOR, SLUG_MAX, slugify


def unique_slug(text: str, existing: set[str]) -> str:
    """Return a slug for ``text`` that is not in ``existing``.

    Reuses :func:`slugkit.slug.slugify` and the spec 001 constants. When the
    base slug is already taken, append ``SEPARATOR + str(n)`` suffixes for
    n = 2, 3, 4, ... until a free slug is found. The full result, including the
    suffix, is capped at ``SLUG_MAX`` characters. ``existing`` is never modified.
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
