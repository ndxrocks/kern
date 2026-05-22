"""Backward-compatibility stub. Use kern.tools.google.gmail instead."""

import warnings

warnings.warn(
    "Importing from 'kern.tools.gmail' is deprecated. Use 'from kern.tools.google.gmail import GmailTools' instead.",
    DeprecationWarning,
    stacklevel=2,
)

from kern.tools.google.gmail import *  # noqa: F401, F403, E402
from kern.tools.google.gmail import GmailTools  # noqa: F811, E402

__all__ = ["GmailTools"]
