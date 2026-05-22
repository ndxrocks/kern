from typing import Dict

from httpx import AsyncClient as HttpxAsyncClient
from httpx import Client as HttpxClient
from httpx import Response

from kern.api.settings import kern_api_settings


class Api:
    def __init__(self):
        self.headers: Dict[str, str] = {
            "user-agent": f"{kern_api_settings.app_name}/{kern_api_settings.app_version}",
            "Content-Type": "application/json",
        }

    def Client(self) -> HttpxClient:
        return HttpxClient(
            base_url=kern_api_settings.api_url,
            headers=self.headers,
            timeout=60,
            http2=True,
        )

    def AsyncClient(self) -> HttpxAsyncClient:
        return HttpxAsyncClient(
            base_url=kern_api_settings.api_url,
            headers=self.headers,
            timeout=60,
            http2=True,
        )


api = Api()


def invalid_response(r: Response) -> bool:
    """Returns true if the response is invalid"""

    if r.status_code >= 400:
        return True
    return False
