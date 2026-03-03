"""MCP tool implementations for Bloom Growth REST API.

Each function is registered as an MCP tool in server.py.
"""

import json

from bloomy_mcp.client import get_client


def _format(data) -> str:
    """Convert API response to readable JSON string."""
    return json.dumps(data, indent=2, default=str)


def get_capabilities() -> str:
    """List all available Bloom Growth tools and what they can do.

    Returns a description of each tool, its parameters, and example
    use cases to help choose the right tool.
    """
    return """Available Bloom Growth Tools:

## My Data (no parameters needed)
- get_my_rocks: Get your quarterly rocks/goals
- get_my_scorecard: Get your scorecard with measurables
- get_my_measurables: Get your KPIs/metrics
- get_my_issues: Get issues assigned to you

## Meetings
- list_meetings: List all your L10 meetings (returns meeting IDs)
- get_meeting_details(meeting_id): Get meeting info and attendees
- get_meeting_todos(meeting_id): Get todos from a meeting
- get_meeting_issues(meeting_id): Get issues from a meeting

## Common Workflows
- To see your todos: first call list_meetings, then call get_meeting_todos for each meeting
- To check your L10 issues: first call list_meetings, then call get_meeting_issues
"""


async def get_my_rocks() -> str:
    """Get all rocks (quarterly goals) for the authenticated user.

    Returns a list of rocks with their title, status, completion percentage,
    due date, and owner information.
    """
    try:
        data = await get_client().get("/rocks/user/mine")
        return _format(data)
    except Exception as e:
        return f"Error fetching rocks: {e}"


async def get_my_scorecard() -> str:
    """Get the scorecard for the authenticated user.

    Returns measurables (KPIs/metrics) assigned to the user, including
    current values, goals, and whether they are on track.
    """
    try:
        data = await get_client().get("/scorecard/user/mine")
        return _format(data)
    except Exception as e:
        return f"Error fetching scorecard: {e}"


async def get_my_measurables() -> str:
    """Get all measurables (KPIs/metrics) assigned to the authenticated user.

    Returns measurable details including name, target, current value,
    and scoring direction.
    """
    try:
        data = await get_client().get("/measurables/user/mine")
        return _format(data)
    except Exception as e:
        return f"Error fetching measurables: {e}"


async def get_my_issues() -> str:
    """Get all issues assigned to the authenticated user.

    Returns open issues with their title, priority, creation date,
    and which meeting they belong to.
    """
    try:
        data = await get_client().get("/issues/users/mine")
        return _format(data)
    except Exception as e:
        return f"Error fetching issues: {e}"


async def list_meetings() -> str:
    """List all L10 meetings the authenticated user has access to.

    Returns meeting names and IDs. Use the meeting ID with other tools
    like get_meeting_todos or get_meeting_issues to get meeting-specific data.
    """
    try:
        data = await get_client().get("/L10/list")
        return _format(data)
    except Exception as e:
        return f"Error listing meetings: {e}"


async def get_meeting_details(meeting_id: int) -> str:
    """Get full details about a specific L10 meeting.

    Args:
        meeting_id: The numeric ID of the L10 meeting. Use list_meetings to find IDs.

    Returns meeting name, attendees, and configuration details.
    """
    try:
        data = await get_client().get(f"/L10/{meeting_id}")
        return _format(data)
    except Exception as e:
        return f"Error fetching meeting {meeting_id}: {e}"


async def get_meeting_todos(meeting_id: int) -> str:
    """Get all todos from a specific L10 meeting.

    Args:
        meeting_id: The numeric ID of the L10 meeting. Use list_meetings to find IDs.

    Returns todo items with their title, assignee, due date, and completion status.
    """
    try:
        data = await get_client().get(f"/l10/{meeting_id}/todos")
        return _format(data)
    except Exception as e:
        return f"Error fetching todos for meeting {meeting_id}: {e}"


async def get_meeting_issues(meeting_id: int) -> str:
    """Get all issues from a specific L10 meeting's issues list.

    Args:
        meeting_id: The numeric ID of the L10 meeting. Use list_meetings to find IDs.

    Returns issues with their title, owner, priority, and status.
    """
    try:
        data = await get_client().get(f"/l10/{meeting_id}/issues")
        return _format(data)
    except Exception as e:
        return f"Error fetching issues for meeting {meeting_id}: {e}"
