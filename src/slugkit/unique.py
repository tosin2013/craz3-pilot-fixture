"""Unique slug generation."""
from slugkit.slug import slugify, SEPARATOR, SLUG_MAX


def unique_slug(text: str, existing: set[str]) -> str:
    """Return a slug derived from *text* that is not in *existing*."""
    base = slugify(text)
    if base not in existing:
        return base

    n = 2
    while True:
        suffix = SEPARATOR + str(n)
        # Trim base so the full slug fits within SLUG_MAX
        max_base_len = SLUG_MAX - len(suffix)
        trimmed = base[:max_base_len].rstrip(SEPARATOR)
        candidate = trimmed + suffix
        if candidate not in existing:
            return candidate
        n += 1
