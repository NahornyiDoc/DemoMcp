import uuid
import pytest
from fastmcp import Client


@pytest.mark.asyncio
async def test_get_issue_valid(mcp_server):
    async with Client(mcp_server) as client:
        result = await client.call_tool_mcp("get_issue", {"issue_key": "DEV-1"})
    assert result.isError is False
    assert result.structuredContent["key"] == "DEV-1"


@pytest.mark.asyncio
async def test_get_issue_invalid_format(mcp_server):
    async with Client(mcp_server) as client:
        result = await client.call_tool_mcp("get_issue", {"issue_key": "DEV1"})
    assert result.isError is True


@pytest.mark.asyncio
async def test_create_issue_empty_summary(mcp_server):
    async with Client(mcp_server) as client:
        result = await client.call_tool_mcp("create_issue", {"summary": "   "})
    assert result.isError is True


@pytest.mark.asyncio
async def test_add_comment_response_fields_are_correct(mcp_server):
    marker = f"autotest-{uuid.uuid4().hex[:8]}"
    async with Client(mcp_server) as client:
        result = await client.call_tool_mcp(
            "add_comment",
            {"issue_key": "DEV-1", "comment": marker},
        )
    assert result.isError is False
    content = result.structuredContent
    assert content["issue_key"] == "DEV-1"
    assert content["comment_id"] != "unknown"
    assert isinstance(content["author"], str)
    assert content["author"] not in ("unknown", "")
    assert content["author"] != content["comment_id"]


@pytest.mark.asyncio
async def test_get_comments_trailing_space(mcp_server):
    async with Client(mcp_server) as client:
        result = await client.call_tool_mcp("get_comments", {"issue_key": "DEV-1 "})
    assert result.isError is True


@pytest.mark.asyncio
async def test_get_comments_leading_space(mcp_server):
    async with Client(mcp_server) as client:
        result = await client.call_tool_mcp("get_comments", {"issue_key": " DEV-1"})
    assert result.isError is True
