"""Unique slug generation (Spec 002)."""

from .slug import SEPARATOR, SLUG_MAX, slugify


def unique_slug(text: str, existing: set[str]) -> str:
    """Return a slug for ``text`` that is not in ``existing``.

    Reuses :func:`slugkit.slugify` and the Spec 001 constants. The base slug is
    returned unchanged when it is free; otherwise ``SEPARATOR + str(n)``
    suffixes are tried for n = 2, 3, 4, ... until a free slug is found.

    The full result, including the suffix, is kept at most ``SLUG_MAX``
    characters long: the base is cut so that ``len(base) + len(suffix)`` fits,
    any trailing separator on the cut base is removed, and then the suffix is
    appended. ``existing`` is never modified.
    """
    base = slugify(text)
    if base not in existing:
        return base

    n = 2
    while True:
        suffix = SEPARATOR + str(n)
        max_base = max(0, SLUG_MAX - len(suffix))
        cut = base[:max_base].rstrip(SEPARATOR)
        candidate = cut + suffix
        if candidate not in existing:
            return candidate
        n += 1
