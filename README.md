# Jira MCP Server

A local MCP server for managing Jira issues. Supports 7 tools: get, create, update, delete, search issues, add and get comments.

---

## Prerequisites

- Python 3.11+
- Jira Cloud account
- Jira API token → [Generate here](https://id.atlassian.com/manage-api-tokens)

---

## Installation

### Clone the repository

```bash
git clone https://github.com/your-repo/jira-mcp.git
cd jira-mcp
```

### Create virtual environment and install dependencies

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Configuration

### macOS / Linux — `mcp.json`

```json
{
  "servers": {
    "JiraMCP": {
      "type": "stdio",
      "command": "/absolute/path/to/project/.venv/bin/python",
      "args": [
        "/absolute/path/to/project/server.py",
        "--email",       "your@email.com",
        "--token",       "YOUR_API_TOKEN",
        "--url",         "https://your-domain.atlassian.net",
        "--project-key", "DEV"
      ]
    }
  }
}
```

---

### Windows — `mcp.json`

```json
{
  "servers": {
    "JiraMCP": {
      "type": "stdio",
      "command": "C:\\absolute\\path\\to\\project\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\absolute\\path\\to\\project\\server.py",
        "--email",       "your@email.com",
        "--token",       "YOUR_API_TOKEN",
        "--url",         "https://your-domain.atlassian.net",
        "--project-key", "DEV"
      ]
    }
  }
}
```

---

## Client Setup

### GitHub Copilot (VS Code)

1. Open VS Code
2. Create `.vscode/mcp.json` in your project root
3. Paste the configuration above (macOS or Windows)
4. Open GitHub Copilot Chat → Agent mode
5. Type `#JiraMCP` to attach the server context
6. Verify: you should see `5 tools` (or `7 tools`) discovered in the output log

**Quick check in VS Code Output:**
```
[info] Discovered 7 tools
```

---

### Claude Code (CLI)

Add the server to your Claude Code config:

**macOS / Linux**
```bash
claude mcp add jira-mcp \
  /absolute/path/to/.venv/bin/python \
  /absolute/path/to/server.py \
  --email your@email.com \
  --token YOUR_API_TOKEN \
  --url https://your-domain.atlassian.net \
  --project-key DEV
```

**Windows**
```bash
claude mcp add jira-mcp ^
  C:\path\to\.venv\Scripts\python.exe ^
  C:\path\to\server.py ^
  --email your@email.com ^
  --token YOUR_API_TOKEN ^
  --url https://your-domain.atlassian.net ^
  --project-key DEV
```

Or manually edit `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "jira-mcp": {
      "command": "/absolute/path/to/.venv/bin/python",
      "args": [
        "/absolute/path/to/server.py",
        "--email",       "your@email.com",
        "--token",       "YOUR_API_TOKEN",
        "--url",         "https://your-domain.atlassian.net",
        "--project-key", "DEV"
      ]
    }
  }
}
```

Verify connection:
```bash
claude mcp list
```

---

## Available Tools

| Tool | Description | Read Only | Destructive |
|------|-------------|-----------|-------------|
| `get_issue` | Get issue details by key | ✅ | ❌ |
| `create_issue` | Create a new issue | ❌ | ❌ |
| `update_issue` | Update summary or description | ❌ | ❌ |
| `delete_issue` | Permanently delete an issue | ❌ | ✅ |
| `search_issues` | Search using JQL | ✅ | ❌ |
| `add_comment` | Add a comment to an issue | ❌ | ❌ |
| `get_comments` | Get all comments for an issue | ✅ | ❌ |

---

## Usage Examples

```
get issue DEV-1

create issue with summary "Login button broken" type Bug

update issue DEV-1 summary "Login button broken on mobile"

search issues in project DEV where status is Open order by created DESC

add comment to DEV-1 "Reproduced on iOS 17, cannot reproduce on Android"

get all comments for DEV-1

delete issue DEV-5
```

---