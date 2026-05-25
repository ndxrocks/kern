"""
Kern — Agent framework for small models.

Small Models. Big Impact.

Template-based structured output, JSON repair, LaTeX protection,
and workflow visualization — so 1-7B models produce reliable results.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("kern-ai")
except PackageNotFoundError:
    __version__ = "0.1.1"

__all__ = ["__version__"]
