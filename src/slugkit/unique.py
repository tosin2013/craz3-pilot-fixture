"""Unique slug generation."""

from slugkit.slug import slugify, SEPARATOR, SLUG_MAX


def unique_slug(text: str, existing: set[str]) -> str:
    """Return a slug derived from *text* that is not in *existing*.

    1. Compute base = slugify(text).
    2. If base is not in existing, return it.
    3. Otherwise, try suffixes SEPARATOR + str(n) for n = 2, 3, 4, …
       The full slug (base + suffix) must be at most SLUG_MAX characters:
       the base is cut so that len(base) + len(suffix) <= SLUG_MAX, and
       any trailing SEPARATOR on the cut base is removed before appending.
    4. existing is never modified.
    """
    base = slugify(text)
    if base not in existing:
        return base

    n = 2
    while True:
        suffix = SEPARATOR + str(n)
        max_base_len = SLUG_MAX - len(suffix)
        trimmed_base = base[:max_base_len].rstrip(SEPARATOR)
        candidate = trimmed_base + suffix
        if candidate not in existing:
            return candidate
        n += 1
