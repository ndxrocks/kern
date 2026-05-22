__all__ = [
    "GoogleAuth",
    "GoogleSlidesTools",
    "GoogleBigQueryTools",
    "GoogleCalendarTools",
    "GoogleDriveTools",
    "GmailTools",
    "GoogleMapTools",
    "GoogleSheetsTools",
]


def __getattr__(name: str):
    if name == "GoogleAuth":
        from kern.tools.google.auth import GoogleAuth

        return GoogleAuth
    if name == "GoogleSlidesTools":
        from kern.tools.google.slides import GoogleSlidesTools

        return GoogleSlidesTools
    if name == "GoogleBigQueryTools":
        from kern.tools.google.bigquery import GoogleBigQueryTools

        return GoogleBigQueryTools
    if name == "GoogleCalendarTools":
        from kern.tools.google.calendar import GoogleCalendarTools

        return GoogleCalendarTools
    if name == "GoogleDriveTools":
        from kern.tools.google.drive import GoogleDriveTools

        return GoogleDriveTools
    if name == "GmailTools":
        from kern.tools.google.gmail import GmailTools

        return GmailTools
    if name == "GoogleMapTools":
        from kern.tools.google.maps import GoogleMapTools

        return GoogleMapTools
    if name == "GoogleSheetsTools":
        from kern.tools.google.sheets import GoogleSheetsTools

        return GoogleSheetsTools
    raise AttributeError(f"module 'kern.tools.google' has no attribute {name!r}")
