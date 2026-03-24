import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from config import VALID_ISSUE_TYPES


class IssueKeySchema(BaseModel):
    issue_key: str = Field(min_length=2, max_length=20)

    @field_validator("issue_key")
    @classmethod
    def validate_format(cls, v: str) -> str:
        cleaned = v.strip().upper()
        if not re.match(r"^[A-Z]+-\d+$", cleaned):
            raise ValueError(
                f"Invalid issue key format: '{v}'. Expected format like 'AT-42'"
            )
        return cleaned


class CreateIssueSchema(BaseModel):
    summary: str = Field(min_length=1, max_length=255)
    description: str = Field(default="", max_length=10_000)
    issue_type: str = Field(default="Story")

    @field_validator("issue_type")
    @classmethod
    def validate_issue_type(cls, v: str) -> str:
        if v not in VALID_ISSUE_TYPES:
            raise ValueError(
                f"Invalid issue_type: '{v}'. Must be one of: {VALID_ISSUE_TYPES}"
            )
        return v

    @field_validator("summary")
    @classmethod
    def validate_summary(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("summary cannot be empty or whitespace only")
        return v.strip()


class UpdateIssueSchema(BaseModel):
    issue_key: str = Field(min_length=2, max_length=20)
    summary: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None, max_length=10_000)

    @field_validator("issue_key")
    @classmethod
    def validate_key(cls, v: str) -> str:
        cleaned = v.strip().upper()
        if not re.match(r"^[A-Z]+-\d+$", cleaned):
            raise ValueError(
                f"Invalid issue key format: '{v}'. Expected format like 'AT-42'"
            )
        return cleaned

    @field_validator("summary")
    @classmethod
    def validate_summary(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError("summary cannot be empty or whitespace only")
            return v.strip()
        return v


class SearchIssuesSchema(BaseModel):
    jql: str = Field(min_length=1, max_length=500)
    max_results: int = Field(default=20, ge=1, le=50)