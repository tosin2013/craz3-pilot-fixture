"""Unique slug generation."""

from slugkit.slug import slugify, SEPARATOR, SLUG_MAX


def unique_slug(text: str, existing: set[str]) -> str:
    """Return a slug for *text* that is not in *existing*.

    Uses ``slugify`` to compute the base slug, then appends ``SEPARATOR + str(n)``
    for n = 2, 3, 4, … until a free slug is found. The full result is at most
    ``SLUG_MAX`` characters; the base is trimmed (and any trailing ``SEPARATOR``
    removed) to make room for the suffix.
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
