from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


DEFAULT_PROJECT_ROOT = Path(
    r"C:\Users\sheik\My_Porject\LangNation Dictionary\Web\langnation-dictionary-v19"
)


@dataclass(frozen=True)
class TestConfig:
    base_url: str
    project_root: Path
    timeout_ms: int = 10_000


def read_base_url(pytest_base_url: str | None = None) -> str | None:
    return (
        pytest_base_url
        or os.getenv("LANGNATION_BASE_URL")
        or os.getenv("BASE_URL")
    )


def read_project_root() -> Path:
    return Path(os.getenv("LANGNATION_PROJECT_ROOT") or DEFAULT_PROJECT_ROOT)

