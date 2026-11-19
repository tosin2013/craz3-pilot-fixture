"""Unique slug generation for the slugkit package."""

from .slug import EMPTY_SLUG, SEPARATOR, SLUG_MAX, slugify

__all__ = ["unique_slug"]


def unique_slug(text: str, existing: set[str]) -> str:
    """Return a slug for ``text`` that is not present in ``existing``.

    The slug is computed with :func:`slugkit.slugify`. When the base slug is
    already taken, numeric suffixes (``SEPARATOR + str(n)`` for n = 2, 3, ...)
    are appended until a free slug is found. The resulting slug, including its
    suffix, is never longer than ``SLUG_MAX`` characters. ``existing`` is not
    modified.
    """
    base = slugify(text)

    if base not in existing:
        return base

    n = 2
    while True:
        suffix = SEPARATOR + str(n)

        if len(base) + len(suffix) > SLUG_MAX:
            cut = base[: SLUG_MAX - len(suffix)].rstrip(SEPARATOR)
        else:
            cut = base

        candidate = cut + suffix
        if candidate not in existing:
            return candidate

        n += 1
