import argparse
import base64

def _parse_args():
    parser = argparse.ArgumentParser(description="Jira MCP Server")
    parser.add_argument("--email",       required=True, help="Jira account email")
    parser.add_argument("--token",       required=True, help="Jira API token")
    parser.add_argument("--url",         required=True, help="Jira base URL, e.g. https://mycompany.atlassian.net")
    parser.add_argument("--project-key", required=True, help="Jira project key, e.g. AT")
    return parser.parse_args()


def _build_headers(email: str, token: str) -> dict[str, str]:
    creds = base64.b64encode(f"{email}:{token}".encode()).decode()
    return {
        "Authorization": f"Basic {creds}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

_args = _parse_args()

JIRA_BASE_URL = _args.url.rstrip("/")
PROJECT_KEY   = _args.project_key
HEADERS       = _build_headers(_args.email, _args.token)

VALID_ISSUE_TYPES = ["Bug", "Task", "Epic"]