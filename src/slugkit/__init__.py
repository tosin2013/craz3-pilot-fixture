"""slugkit: throwaway fixture package for the specfoundry M1 pilot."""

from .slug import slugify, SEPARATOR, SLUG_MAX, EMPTY_SLUG
from .unique import unique_slug

__all__ = ["slugify", "SEPARATOR", "SLUG_MAX", "EMPTY_SLUG", "unique_slug"]
