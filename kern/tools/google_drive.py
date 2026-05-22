"""Backward-compatibility stub. Use kern.tools.google.drive instead."""

import warnings

warnings.warn(
    "Importing from 'kern.tools.google_drive' is deprecated. "
    "Use 'from kern.tools.google.drive import GoogleDriveTools' instead.",
    DeprecationWarning,
    stacklevel=2,
)

from kern.tools.google.drive import *  # noqa: F401, F403, E402
from kern.tools.google.drive import GoogleDriveTools  # noqa: F811, E402

__all__ = ["GoogleDriveTools"]
