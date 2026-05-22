"""Backward-compatibility stub. Use kern.tools.google.sheets instead."""

import warnings

warnings.warn(
    "Importing from 'kern.tools.googlesheets' is deprecated. "
    "Use 'from kern.tools.google.sheets import GoogleSheetsTools' instead.",
    DeprecationWarning,
    stacklevel=2,
)

from kern.tools.google.sheets import *  # noqa: F401, F403, E402
from kern.tools.google.sheets import GoogleSheetsTools  # noqa: F811, E402

__all__ = ["GoogleSheetsTools"]
