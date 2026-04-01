import os
import sys
from dotenv import load_dotenv
import pytest
from fastmcp import FastMCP

load_dotenv()

sys.argv = [
    "pytest",
    "--email",       os.environ.get("JIRA_EMAIL", ""),
    "--token",       os.environ.get("JIRA_TOKEN", ""),
    "--url",         os.environ.get("JIRA_URL", "https://test-automation-accelerators.atlassian.net"),
    "--project-key", os.environ.get("JIRA_PROJECT_KEY", "DEV"),
]

from tools import get_issue, create_issue, update_issue, delete_issue, search_issues, add_comment, get_comments


@pytest.fixture(scope="session")
def mcp_server():
    server = FastMCP("JiraMCP-Test")
    get_issue.register(server)
    create_issue.register(server)
    update_issue.register(server)
    delete_issue.register(server)
    search_issues.register(server)
    add_comment.register(server)
    get_comments.register(server)
    return server