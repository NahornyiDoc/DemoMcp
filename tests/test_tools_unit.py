import pytest
from pydantic import ValidationError

from schemas import IssueKeySchema, CreateIssueSchema, SearchIssuesSchema


def test_valid_key():
    data = IssueKeySchema(issue_key="DEV-1")
    assert data.issue_key == "DEV-1"


def test_lowercase_converted():
    data = IssueKeySchema(issue_key="dev-1")
    assert data.issue_key == "DEV-1"


def test_empty_key_raises():
    with pytest.raises(ValidationError):
        IssueKeySchema(issue_key="")


def test_invalid_format_raises():
    with pytest.raises(ValidationError):
        IssueKeySchema(issue_key="DEV1")


def test_empty_summary_raises():
    with pytest.raises(ValidationError):
        CreateIssueSchema(summary="")


def test_whitespace_summary_raises():
    with pytest.raises(ValidationError):
        CreateIssueSchema(summary="   ")


def test_summary_too_long_raises():
    with pytest.raises(ValidationError):
        CreateIssueSchema(summary="x" * 256)


def test_invalid_issue_type_raises():
    with pytest.raises(ValidationError):
        CreateIssueSchema(summary="Valid summary", issue_type="Story")


def test_max_results_out_of_range_raises():
    with pytest.raises(ValidationError):
        SearchIssuesSchema(jql="project=DEV", max_results=51)
