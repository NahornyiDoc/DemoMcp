import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.argv = [
    "pytest",
    "--email",       os.environ.get("JIRA_EMAIL", ""),
    "--token",       os.environ.get("JIRA_TOKEN", ""),
    "--url",         os.environ.get("JIRA_URL", "https://test-automation-accelerators.atlassian.net"),
    "--project-key", os.environ.get("JIRA_PROJECT_KEY", "DEV"),
]