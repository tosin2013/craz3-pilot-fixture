"""Unique slug generation."""

from slugkit.slug import slugify, SEPARATOR, SLUG_MAX


def unique_slug(text: str, existing: set[str]) -> str:
    """Return a slug derived from *text* that is not in *existing*.

    1. Compute base = slugify(text).
    2. If base is not taken, return it.
    3. Otherwise try base + SEPARATOR + str(n) for n = 2, 3, 4, ...
       The full slug (including suffix) must not exceed SLUG_MAX characters:
       the base is trimmed and any trailing SEPARATOR is stripped before the
       suffix is appended.
    """
    base = slugify(text)

    if base not in existing:
        return base

    n = 2
    while True:
        suffix = SEPARATOR + str(n)
        # Trim base so that len(trimmed_base) + len(suffix) <= SLUG_MAX
        max_base_len = SLUG_MAX - len(suffix)
        trimmed_base = base[:max_base_len].rstrip(SEPARATOR)
        candidate = trimmed_base + suffix
        if candidate not in existing:
            return candidate
        n += 1
