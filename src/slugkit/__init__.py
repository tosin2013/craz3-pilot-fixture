"""slugkit: throwaway fixture package for the specfoundry M1 pilot."""

from .slug import slugify
from .unique import unique_slug

__all__ = ["slugify", "unique_slug"]
