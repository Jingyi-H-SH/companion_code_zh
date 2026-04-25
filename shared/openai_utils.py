"""供初学者演示代码复用的 OpenAI 工具函数。"""

from __future__ import annotations

import getpass
import json
import os
import sys
from typing import Any

try:
    from openai import OpenAI
except ImportError as exc:  # pragma: no cover
    raise RuntimeError("请先执行 `pip install -r requirements.txt` 安装依赖。") from exc


DEFAULT_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")


def ensure_openai_credentials(locale: str = "zh") -> dict[str, str]:
    """Read OpenAI credentials from the environment or prompt the reader once."""
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    model = os.environ.get("OPENAI_MODEL", "").strip() or DEFAULT_MODEL
    if not key:
        if not sys.stdin.isatty():
            raise RuntimeError("请先设置 OPENAI_API_KEY，或在交互式终端中运行本脚本。")
        key = getpass.getpass("请输入你的 OpenAI API key（输入不可见）：").strip()
        if not key:
            raise RuntimeError("请先设置 OPENAI_API_KEY，或在交互式终端中运行本脚本。")
        model_input = input("请输入要使用的模型名 [gpt-4.1-mini]：").strip()
        if model_input:
            model = model_input
    os.environ["OPENAI_API_KEY"] = key
    os.environ["OPENAI_MODEL"] = model
    return {"OPENAI_API_KEY": key, "OPENAI_MODEL": model}


def get_model() -> str:
    return os.environ.get("OPENAI_MODEL", DEFAULT_MODEL)


def create_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("请先设置 OPENAI_API_KEY，或在交互式终端中运行本脚本。")
    return OpenAI(api_key=api_key)


def json_completion(system_prompt: str, user_prompt: str, schema_name: str, schema: dict[str, Any], max_output_tokens: int = 900) -> dict[str, Any]:
    response = create_client().responses.create(
        model=get_model(),
        input=[
            {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
            {"role": "user", "content": [{"type": "input_text", "text": user_prompt}]},
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": schema_name,
                "schema": schema,
                "strict": True,
            }
        },
        max_output_tokens=max_output_tokens,
    )
    return json.loads(response.output_text)


def text_completion(system_prompt: str, user_prompt: str, max_output_tokens: int = 700) -> str:
    response = create_client().responses.create(
        model=get_model(),
        input=[
            {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
            {"role": "user", "content": [{"type": "input_text", "text": user_prompt}]},
        ],
        max_output_tokens=max_output_tokens,
    )
    return response.output_text.strip()


def clamp_score(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))
