"""Spec 002: unique slugs."""

from itertools import count

from slugkit.slug import SEPARATOR, SLUG_MAX, slugify


def unique_slug(text: str, existing: set[str]) -> str:
    """Return a slug for *text* that is not in *existing*.

    Reuses :func:`slugkit.slug.slugify` to compute the base slug. If the base is
    already taken, appends ``SEPARATOR + str(n)`` for ``n = 2, 3, 4, ...`` until a
    free slug is found. The base is cut so the full result (including the suffix)
    never exceeds ``SLUG_MAX`` characters, and any trailing separator left by the
    cut is removed before the suffix is added. *existing* is never modified.
    """
    base = slugify(text)
    if base not in existing:
        return base

    for n in count(2):
        suffix = SEPARATOR + str(n)
        cut = SLUG_MAX - len(suffix)
        if cut < 0:
            cut = 0
        trimmed = base[:cut].rstrip(SEPARATOR)
        candidate = trimmed + suffix
        if candidate not in existing:
            return candidate
