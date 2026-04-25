from __future__ import annotations

import json
import re
from pathlib import Path


TOKEN_RE = re.compile(r"[a-zA-Z0-9_]+")


def load_json_items(path: str | Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text or "")]


def _flatten(value) -> str:
    if isinstance(value, list):
        return " ".join(str(item) for item in value)
    return str(value)


def retrieve_chunks(query: str, items: list[dict], top_k: int = 2, fields: tuple[str, ...] = ("title", "content", "topic", "barrier", "section", "tags", "moderator_hint")) -> list[dict]:
    query_tokens = tokenize(query)
    scored = []
    for index, item in enumerate(items):
        haystack = " ".join(_flatten(item.get(field, "")) for field in fields)
        item_tokens = tokenize(haystack)
        score = sum(1 for token in query_tokens if token in item_tokens)
        scored.append((score, -index, item))
    scored.sort(reverse=True)
    selected = [item for score, _, item in scored[:top_k] if score > 0]
    if not selected:
        selected = [item for _, _, item in scored[:top_k]]
    return selected


def format_chunks(chunks: list[dict]) -> str:
    lines = []
    for chunk in chunks:
        title = chunk.get("title", chunk.get("id", "Reference"))
        content = chunk.get("content", "")
        lines.append(f"[{chunk.get('id', 'REF')}] {title}: {content}")
    return "\n".join(lines)
