"""slugkit: throwaway fixture package for the specfoundry M1 pilot."""

from slugkit.slug import slugify
from slugkit.unique import unique_slug

__all__ = ["slugify", "unique_slug"]
