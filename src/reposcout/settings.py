"""Local configuration with explicit credential handling."""

import os
from pathlib import Path
from typing import Literal

from pydantic import Field, model_validator

from reposcout.domain import Record, ResearchError

PRICE_SOURCE = "https://api-docs.deepseek.com/zh-cn/quick_start/pricing/"
PRICE_DATE = "2026-11-12"


class Settings(Record):
    home: Path = Field(default_factory=lambda: Path(os.getenv("REPOSCOUT_HOME", ".reposcout")))
    max_model_calls: int = Field(default=20, ge=1, le=100)
    max_github_requests: int = Field(default=60, ge=1, le=500)
    timeout_seconds: int = Field(default=600, ge=1, le=3600)
    search_limit: int = Field(default=10, ge=1, le=30)
    analyze_limit: int = Field(default=3, ge=1, le=10)
    max_cost_cny: float = Field(default=20, gt=0, le=20)
    max_output_tokens: int = Field(default=4096, ge=256, le=8192)
    # Peak, uncached rates in micro-CNY per token. Cached input is conservatively charged.
    input_micro_cny: Literal[2] = 2
    output_micro_cny: Literal[8] = 8
    model: Literal["deepseek-flash"] = "deepseek-flash"
    review_model: Literal["deepseek-v4-pro"] = "deepseek-v4-pro"
    base_url: Literal["https://api.deepseek.com/anthropic"] = "https://api.deepseek.com/anthropic"

    @model_validator(mode="after")
    def validate_limits(self):
        if self.analyze_limit > self.search_limit:
            raise ValueError("analyze_limit 必须小于等于 search_limit")
        return self

    def api_key(self) -> str:
        value = os.getenv("DEEPSEEK_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        value = value or os.getenv("ANTHROPIC_AUTH_TOKEN")
        if not value:
            raise ResearchError("configuration", "请通过环境变量配置 DEEPSEEK_API_KEY")
        return value
