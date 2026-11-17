"""Unique slug generation."""

from slugkit.slug import slugify, SEPARATOR, SLUG_MAX


def unique_slug(text: str, existing: set[str]) -> str:
    """Return a slug derived from *text* that is not in *existing*.

    If the base slug is already taken, suffixes ``~2``, ``~3``, … are appended.
    The full slug (including suffix) never exceeds ``SLUG_MAX`` characters; the
    base is trimmed (and any trailing ``~`` removed) to make room for the suffix.
    ``existing`` is never modified.
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
