"""GraphQL client for Bloom API.

Provides a client for connecting to and executing operations against the Bloom GraphQL API.
"""

from os import getenv
from typing import Any, Dict, Optional

from gql import Client as GQLClient, gql
from gql.transport.httpx import HTTPXTransport


class Client:
    """Client for interacting with the Bloom GraphQL API."""

    def __init__(self) -> None:
        """Initialize the GraphQL client with authentication.

        Uses environment variables BLOOM_API_URL and BLOOM_API_TOKEN for configuration.
        Raises ValueError if required environment variables are not set.
        """
        api_url = getenv("BLOOM_API_URL")
        api_token = getenv("BLOOM_API_TOKEN")

        if not api_url or not api_token:
            raise ValueError("BLOOM_API_URL and BLOOM_API_TOKEN environment variables must be set")

        headers = {"Authorization": f"Bearer {api_token}"}
        transport = HTTPXTransport(url=api_url, headers=headers)
        self.gql_client = GQLClient(transport=transport, fetch_schema_from_transport=True)

    def execute(self, query: Any, variable_values: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a GraphQL query or mutation.

        Args:
            query: The GraphQL query object (created using gql())
            variable_values: Optional dictionary of variables to include with the query

        Returns:
            Dict containing the query results
        """
        return self.gql_client.execute(query, variable_values=variable_values)


_default_client: Optional[Client] = None


def get_client() -> Client:
    """Get or create the default client instance.

    Lazily initializes the client on first use to avoid import-time failures
    when environment variables are not yet available.
    """
    global _default_client
    if _default_client is None:
        _default_client = Client()
    return _default_client
