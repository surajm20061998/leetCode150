from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from typing import Any
from urllib.parse import urlparse

import httpx

from .models import ProblemResponse


LEETCODE_GRAPHQL = "https://leetcode.com/graphql"
QUESTION_QUERY = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId
    title
    titleSlug
    content
    difficulty
    exampleTestcases
    metaData
    codeSnippets { lang langSlug code }
  }
}
"""


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"p", "pre", "br", "li", "h1", "h2", "h3"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"p", "pre", "li"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        raw = "".join(self.parts)
        return re.sub(r"\n{3,}", "\n\n", raw).strip()


def extract_slug(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc not in {"leetcode.com", "www.leetcode.com"}:
        raise ValueError("Please use a leetcode.com problem URL")
    match = re.search(r"/problems/([^/?#]+)/?", parsed.path)
    if not match:
        raise ValueError("Could not find a problem slug in that URL")
    return match.group(1)


def _parse_value(line: str) -> Any:
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        # Some older questions use Python-like literals in examples.
        replacements = {"True": "true", "False": "false", "None": "null"}
        normalized = line
        for source, target in replacements.items():
            normalized = normalized.replace(source, target)
        return json.loads(normalized)


def parse_sample_args(example_testcases: str, parameter_count: int) -> list[list[Any]]:
    if parameter_count <= 0:
        return [[]]
    lines = [line.strip() for line in example_testcases.splitlines() if line.strip()]
    cases: list[list[Any]] = []
    for index in range(0, len(lines), parameter_count):
        group = lines[index : index + parameter_count]
        if len(group) != parameter_count:
            continue
        try:
            cases.append([_parse_value(line) for line in group])
        except (json.JSONDecodeError, ValueError):
            continue
    return cases


async def fetch_problem(url: str) -> ProblemResponse:
    slug = extract_slug(url)
    headers = {
        "User-Agent": "Mozilla/5.0 CodeVisualizer/0.1",
        "Referer": f"https://leetcode.com/problems/{slug}/",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        response = await client.post(
            LEETCODE_GRAPHQL,
            headers=headers,
            json={"query": QUESTION_QUERY, "variables": {"titleSlug": slug}},
        )
        response.raise_for_status()
        data = response.json().get("data", {}).get("question")
    if not data:
        raise ValueError("LeetCode did not return a public problem for that URL")

    try:
        metadata = json.loads(data.get("metaData") or "{}")
    except json.JSONDecodeError:
        metadata = {}
    method_name = metadata.get("name")
    params = metadata.get("params") or []
    snippets = data.get("codeSnippets") or []
    python_snippet = next(
        (item.get("code") for item in snippets if item.get("langSlug") in {"python3", "python"}),
        None,
    )
    extractor = TextExtractor()
    extractor.feed(data.get("content") or "")
    return ProblemResponse(
        title=data["title"],
        title_slug=data["titleSlug"],
        difficulty=data["difficulty"],
        question_id=data["questionId"],
        content_text=extractor.text(),
        entrypoint=f"Solution.{method_name}" if method_name else None,
        starter_code=python_snippet,
        sample_args=parse_sample_args(data.get("exampleTestcases") or "", len(params)),
        source_url=f"https://leetcode.com/problems/{slug}/",
    )
