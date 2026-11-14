"""Unique slug generation."""

from .slug import slugify, SEPARATOR, SLUG_MAX


def unique_slug(text: str, existing: set[str]) -> str:
    """Return a slug derived from *text* that is not in *existing*.

    1. Compute base = slugify(text).
    2. If base is not taken, return it.
    3. Otherwise try base + SEPARATOR + str(n) for n = 2, 3, 4, ...
       truncating base so the full result fits within SLUG_MAX characters,
       removing any trailing SEPARATOR from the cut base before appending.
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
