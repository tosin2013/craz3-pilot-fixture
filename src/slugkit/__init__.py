"""slugkit: throwaway fixture package for the specfoundry M1 pilot."""

from slugkit.slug import slugify, SEPARATOR, SLUG_MAX, EMPTY_SLUG
from slugkit.unique import unique_slug

__all__ = ["slugify", "SEPARATOR", "SLUG_MAX", "EMPTY_SLUG", "unique_slug"]
