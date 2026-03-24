from fastmcp import FastMCP
from tools import get_issue
from tools import create_issue
from tools import update_issue
from tools import delete_issue
from tools import search_issues
from tools import add_comment
from tools import get_comments

mcp = FastMCP(
    name="JiraMCP",
    instructions="""
        Jira MCP server for managing issues.
        Use project key from your configuration for all operations.
        
        Available operations:
        - get_issue:      get issue details by key
        - create_issue:   create a new issue
        - update_issue:   update summary or description
        - delete_issue:   permanently delete an issue
        - search_issues:  search using JQL
        
        JQL examples:
          project=AT ORDER BY created DESC
          project=AT AND status=Open
          project=AT AND issuetype=Bug AND assignee=currentUser()
    """,
)

get_issue.register(mcp)
create_issue.register(mcp)
update_issue.register(mcp)
delete_issue.register(mcp)
search_issues.register(mcp)
add_comment.register(mcp)
get_comments.register(mcp)

if __name__ == "__main__":
    mcp.run(transport="stdio", show_banner=False)