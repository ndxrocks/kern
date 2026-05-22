"""Backward-compatibility stub. Use kern.tools.google.calendar instead."""

import warnings

warnings.warn(
    "Importing from 'kern.tools.googlecalendar' is deprecated. "
    "Use 'from kern.tools.google.calendar import GoogleCalendarTools' instead.",
    DeprecationWarning,
    stacklevel=2,
)

from kern.tools.google.calendar import *  # noqa: F401, F403, E402
from kern.tools.google.calendar import GoogleCalendarTools  # noqa: F811, E402

__all__ = ["GoogleCalendarTools"]
