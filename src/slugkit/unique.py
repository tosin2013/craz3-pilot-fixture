"""Unique slug generation (spec 002)."""

from .slug import EMPTY_SLUG, SEPARATOR, SLUG_MAX, slugify


def unique_slug(text: str, existing: set[str]) -> str:
    """Return a slug for ``text`` that is not in ``existing``.

    Reuses ``slugify`` and the spec 001 constants. ``existing`` is never
    modified.
    """
    base = slugify(text)
    if base not in existing:
        return base

    n = 2
    while True:
        suffix = SEPARATOR + str(n)
        # Keep the full result, including the suffix, within SLUG_MAX.
        cut = base[: SLUG_MAX - len(suffix)].rstrip(SEPARATOR)
        candidate = cut + suffix
        if candidate not in existing:
            return candidate
        n += 1
