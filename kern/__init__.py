"""
Kern — Agno fork optimized for small models.

Replaces complex JSON Schema with simple fill-in-the-blanks templates
that small models (2-4B parameters) can reliably follow.

Key differences from Agno:
  - Template-based structured output (not JSON Schema)
  - json_repair + LaTeX protection for malformed responses
  - Targeted retry on validation failures
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("kern")
except PackageNotFoundError:
    __version__ = "0.1.0"

__all__ = ["__version__"]
