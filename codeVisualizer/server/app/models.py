from typing import Any

from pydantic import BaseModel, Field


class ProblemRequest(BaseModel):
    url: str


class TraceRequest(BaseModel):
    code: str = Field(min_length=1)
    reference_code: str | None = None
    entrypoint: str | None = None
    args: list[Any] = Field(default_factory=list)


class ProblemResponse(BaseModel):
    title: str
    title_slug: str
    difficulty: str
    question_id: str
    content_text: str
    entrypoint: str | None
    starter_code: str | None
    sample_args: list[list[Any]]
    source_url: str
