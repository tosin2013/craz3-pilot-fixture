"""slugkit: throwaway fixture package for the specfoundry M1 pilot."""

from .slug import EMPTY_SLUG, SEPARATOR, SLUG_MAX, slugify

__all__ = ["slugify", "SEPARATOR", "SLUG_MAX", "EMPTY_SLUG"]
