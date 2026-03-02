#!/usr/bin/env python3
"""Bloom GraphQL MCP Server.

This server connects to Bloom Growth's GraphQL API and exposes it through
the Model Context Protocol (MCP).

Transport modes (set via MCP_TRANSPORT env var):
  - "stdio" (default): Local MCP client via stdin/stdout
  - "streamable-http": HTTP server for Copilot Studio / remote MCP clients

When using streamable-http, set MCP_API_KEY to require authentication.
"""

import os

from mcp.server.fastmcp import FastMCP

from bloomy_mcp.introspection import (
    get_available_queries,
    get_available_mutations,
)
from bloomy_mcp.operations import (
    get_query_details,
    get_mutation_details,
    execute_query,
    get_authenticated_user_id,
)


# Initialize FastMCP server
dependencies = [
    "gql",
    "httpx",
    "pyyaml",
]
mcp = FastMCP("bloom-graphql", dependencies=dependencies)


# Register resources
mcp.resource("bloom://queries")(get_available_queries)
mcp.resource("bloom://mutations")(get_available_mutations)


# Register tools
mcp.tool()(get_query_details)
mcp.tool()(get_mutation_details)
mcp.tool()(execute_query)
mcp.tool()(get_authenticated_user_id)


def main() -> None:
    """Entry point for the server.

    Set MCP_TRANSPORT=streamable-http for Copilot Studio / HTTP access.
    Defaults to stdio for local MCP client usage.
    """
    transport = os.getenv("MCP_TRANSPORT", "stdio")

    if transport == "streamable-http":
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", "8000"))
        api_key = os.getenv("MCP_API_KEY")

        if api_key:
            # Run with API key middleware via custom ASGI app
            import uvicorn
            from bloomy_mcp.middleware import APIKeyMiddleware

            app = mcp.streamable_http_app()
            app.add_middleware(APIKeyMiddleware, api_key=api_key)
            uvicorn.run(app, host=host, port=port)
        else:
            mcp.run(transport="streamable-http", host=host, port=port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
