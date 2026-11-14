"""Unique slug generation."""
from slugkit.slug import EMPTY_SLUG, SEPARATOR, SLUG_MAX, slugify


def unique_slug(text: str, existing: set[str]) -> str:
    """Return a slug derived from *text* that is not in *existing*.

    If the base slug is already taken, suffixes ``~2``, ``~3``, … are tried.
    The full slug (base + suffix) is always at most ``SLUG_MAX`` characters.
    *existing* is never modified.
    """
    base = slugify(text)
    if base not in existing:
        return base

    n = 2
    while True:
        suffix = SEPARATOR + str(n)
        # Trim base so that base + suffix fits within SLUG_MAX
        max_base_len = SLUG_MAX - len(suffix)
        trimmed = base[:max_base_len].rstrip(SEPARATOR)
        candidate = trimmed + suffix
        if candidate not in existing:
            return candidate
        n += 1
