"""REST client for Bloom Growth API v1.

Provides an async HTTP client for the Bloom Growth REST API.
"""

from os import getenv
from typing import Any, Optional

import httpx


class Client:
    """Async client for the Bloom Growth REST API v1."""

    def __init__(self) -> None:
        base_url = getenv("BLOOM_API_URL", "")
        api_token = getenv("BLOOM_API_TOKEN", "")

        if not base_url or not api_token:
            raise ValueError("BLOOM_API_URL and BLOOM_API_TOKEN environment variables must be set")

        # Normalize: strip trailing slash, remove /graphql suffix for backward compat
        base_url = base_url.rstrip("/")
        if base_url.endswith("/graphql"):
            base_url = base_url[: -len("/graphql")]

        # Append /api/v1 if not already present
        if not base_url.endswith("/api/v1"):
            base_url = f"{base_url}/api/v1"

        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

    async def get(self, path: str, params: Optional[dict] = None) -> Any:
        """GET request. Returns parsed JSON."""
        response = await self._client.get(path, params=params)
        response.raise_for_status()
        return response.json()

    async def post(self, path: str, json: Optional[dict] = None) -> Any:
        """POST request. Returns parsed JSON."""
        response = await self._client.post(path, json=json)
        response.raise_for_status()
        return response.json()

    async def put(self, path: str, json: Optional[dict] = None) -> Any:
        """PUT request. Returns parsed JSON."""
        response = await self._client.put(path, json=json)
        response.raise_for_status()
        return response.json()

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._client.aclose()


_default_client: Optional[Client] = None


def get_client() -> Client:
    """Get or create the default client instance."""
    global _default_client
    if _default_client is None:
        _default_client = Client()
    return _default_client
