import httpx
from fastmcp.exceptions import ToolError
from config import JIRA_BASE_URL, HEADERS


def jira_request(method: str, path: str, **kwargs) -> dict:
    url = f"{JIRA_BASE_URL}{path}"

    try:
        with httpx.Client(timeout=15) as client:
            response = client.request(method, url, headers=HEADERS, **kwargs)
            response.raise_for_status()
            return response.json() if response.content else {}

    except httpx.HTTPStatusError as e:
        raise ToolError(
            f"Jira API error {e.response.status_code}: {e.response.text}"
        ) from e

    except httpx.TimeoutException:
        raise ToolError("Jira request timed out") from None

    except httpx.ConnectError:
        raise ToolError(
            f"Cannot connect to Jira at {JIRA_BASE_URL}"
        ) from None