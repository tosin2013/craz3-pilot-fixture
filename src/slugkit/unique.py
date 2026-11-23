"""Unique slug generation for the slugkit package.

Implements the single public helper ``unique_slug``, which reuses ``slugify``
and the constants from :mod:`slugkit.slug` to produce a slug that is not
already present in a caller-supplied set.
"""

from .slug import SEPARATOR, SLUG_MAX, slugify


def unique_slug(text: str, existing: set[str]) -> str:
    """Return a slug for ``text`` that is not in ``existing``.

    1. Compute ``base = slugify(text)`` and return it if it is free.
    2. Otherwise append ``SEPARATOR + str(n)`` for ``n = 2, 3, 4, ...`` until a
       free slug is found.
    3. The full result, suffix included, never exceeds ``SLUG_MAX`` characters:
       the base is cut so that ``len(base) + len(suffix) <= SLUG_MAX`` and any
       trailing ``SEPARATOR`` left by the cut is removed first.
    4. ``existing`` is never modified.
    """
    base = slugify(text)

    if base not in existing:
        return base

    n = 2
    while True:
        suffix = SEPARATOR + str(n)
        cut_base = base[: SLUG_MAX - len(suffix)].rstrip(SEPARATOR)
        candidate = cut_base + suffix
        if candidate not in existing:
            return candidate
        n += 1
