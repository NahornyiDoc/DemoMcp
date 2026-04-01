import os
import uuid
import pytest
from fastmcp import Client

deepeval = pytest.importorskip("deepeval")
from deepeval import evaluate
from deepeval.metrics import MCPUseMetric
from deepeval.test_case import LLMTestCase, MCPServer, MCPToolCall
from deepeval.evaluate.configs import AsyncConfig

pytestmark = pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY is required for DeepEval MCP metrics",
)


@pytest.mark.asyncio
async def test_deepeval_get_issue_single_turn(mcp_server):
    async with Client(mcp_server) as client:
        tools = await client.list_tools()
        result = await client.call_tool_mcp("get_issue", {"issue_key": "DEV-1"})

    test_case = LLMTestCase(
        input="Get details for issue DEV-1",
        actual_output=str(result.structuredContent),
        mcp_servers=[
            MCPServer(server_name="JiraMCP", transport="stdio", available_tools=tools)
        ],
        mcp_tools_called=[
            MCPToolCall(name="get_issue", args={"issue_key": "DEV-1"}, result=result)
        ],
    )

    metric = MCPUseMetric(model="gpt-4o", threshold=0.5, async_mode=False)
    eval_result = evaluate([test_case], [metric], async_config=AsyncConfig(run_async=False))
    assert eval_result.test_results[0].success is True


@pytest.mark.asyncio
async def test_deepeval_create_and_delete_issue(mcp_server):
    summary = f"DeepEval issue {uuid.uuid4().hex[:8]}"
    async with Client(mcp_server) as client:
        tools = await client.list_tools()
        created = await client.call_tool_mcp(
            "create_issue",
            {"summary": summary, "description": "Created by DeepEval test", "issue_type": "Task"},
        )
        created_key = created.structuredContent["key"]
        deleted = await client.call_tool_mcp("delete_issue", {"issue_key": created_key})

    test_case = LLMTestCase(
        input="Create a Task issue and then delete it",
        actual_output=f"create={created.structuredContent}; delete={deleted.structuredContent}",
        mcp_servers=[
            MCPServer(server_name="JiraMCP", transport="stdio", available_tools=tools)
        ],
        mcp_tools_called=[
            MCPToolCall(
                name="create_issue",
                args={"summary": summary, "description": "Created by DeepEval test", "issue_type": "Task"},
                result=created,
            ),
            MCPToolCall(
                name="delete_issue",
                args={"issue_key": created_key},
                result=deleted,
            ),
        ],
    )

    metric = MCPUseMetric(model="gpt-4o", threshold=0.5, async_mode=False)
    eval_result = evaluate([test_case], [metric], async_config=AsyncConfig(run_async=False))
    assert eval_result.test_results[0].success is True