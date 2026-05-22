"""Backward-compatibility stub. Use kern.tools.google.maps instead."""

import warnings

warnings.warn(
    "Importing from 'kern.tools.google_maps' is deprecated. "
    "Use 'from kern.tools.google.maps import GoogleMapTools' instead.",
    DeprecationWarning,
    stacklevel=2,
)

from kern.tools.google.maps import *  # noqa: F401, F403, E402
from kern.tools.google.maps import GoogleMapTools  # noqa: F811, E402

__all__ = ["GoogleMapTools"]
