#!/usr/bin/env python3
"""Bloom Growth REST API MCP Server.

This server connects to Bloom Growth's REST API v1 and exposes it through
the Model Context Protocol (MCP).

Transport modes (set via MCP_TRANSPORT env var):
  - "stdio" (default): Local MCP client via stdin/stdout
  - "streamable-http": HTTP server for Copilot Studio / remote MCP clients

When using streamable-http, set MCP_API_KEY to require authentication.
"""

import os

from mcp.server.fastmcp import FastMCP

from bloomy_mcp.tools import (
    get_capabilities,
    get_my_rocks,
    get_my_scorecard,
    get_my_measurables,
    get_my_issues,
    list_meetings,
    get_meeting_details,
    get_meeting_todos,
    get_meeting_issues,
)


# Initialize FastMCP server
dependencies = ["httpx"]
mcp = FastMCP("bloomy", dependencies=dependencies)


# Register resources
mcp.resource("bloom://capabilities")(get_capabilities)


# Register tools
mcp.tool()(get_my_rocks)
mcp.tool()(get_my_scorecard)
mcp.tool()(get_my_measurables)
mcp.tool()(get_my_issues)
mcp.tool()(list_meetings)
mcp.tool()(get_meeting_details)
mcp.tool()(get_meeting_todos)
mcp.tool()(get_meeting_issues)


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
        allowed_host = os.getenv("MCP_ALLOWED_HOST", "")

        import uvicorn
        from mcp.server.transport_security import TransportSecuritySettings

        if allowed_host:
            mcp.settings.transport_security = TransportSecuritySettings(
                enable_dns_rebinding_protection=True,
                allowed_hosts=[f"{allowed_host}", "localhost:*", "127.0.0.1:*"],
                allowed_origins=[f"https://{allowed_host}", "http://localhost:*", "http://127.0.0.1:*"],
            )
        else:
            mcp.settings.transport_security = TransportSecuritySettings(
                enable_dns_rebinding_protection=False,
            )

        app = mcp.streamable_http_app()

        if api_key:
            from bloomy_mcp.middleware import APIKeyMiddleware
            app.add_middleware(APIKeyMiddleware, api_key=api_key)

        uvicorn.run(app, host=host, port=port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
