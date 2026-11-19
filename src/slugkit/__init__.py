"""slugkit: throwaway fixture package for the specfoundry M1 pilot."""

from .slug import EMPTY_SLUG, SEPARATOR, SLUG_MAX, slugify
from .unique import unique_slug

__all__ = ["slugify", "unique_slug", "SEPARATOR", "SLUG_MAX", "EMPTY_SLUG"]
