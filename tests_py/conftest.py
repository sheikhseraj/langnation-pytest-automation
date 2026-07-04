from __future__ import annotations

import os
import json
import socket
import subprocess
import time
from pathlib import Path
from typing import Iterator

import pytest
import requests

from tests_py.config import TestConfig, read_base_url, read_project_root


TEST_DATA_DIR = Path(__file__).resolve().parent / "test_data"



def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _wait_for_health(base_url: str, timeout_s: int = 25) -> None:
    deadline = time.time() + timeout_s
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            response = requests.get(f"{base_url}/api/health", timeout=2)
            if response.status_code == 200:
                return
        except requests.RequestException as exc:
            last_error = exc
        time.sleep(0.5)
    raise RuntimeError(f"LangNation server did not become healthy at {base_url}") from last_error


@pytest.fixture(scope="session")
def test_config(pytestconfig: pytest.Config) -> Iterator[TestConfig]:
    project_root = read_project_root()
    configured_url = read_base_url(pytestconfig.getoption("base_url", default=None))
    if configured_url:
        yield TestConfig(base_url=configured_url.rstrip("/"), project_root=project_root)
        return

    if os.getenv("LANGNATION_SKIP_SERVER") == "1":
        raise pytest.UsageError("Set --base-url or BASE_URL when LANGNATION_SKIP_SERVER=1.")
    if not (project_root / "server.js").exists():
        raise pytest.UsageError(f"LangNation project root not found: {project_root}")

    port = _free_port()
    base_url = f"http://127.0.0.1:{port}"
    env = os.environ.copy()
    env.update(
        {
            "PORT": str(port),
            "NODE_ENV": "test",
            "JWT_SECRET": env.get("JWT_SECRET", "pytest-local-secret"),
        }
    )

    process = subprocess.Popen(
        ["node", "server.js"],
        cwd=project_root,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        _wait_for_health(base_url)
        yield TestConfig(base_url=base_url, project_root=project_root)
    finally:
        process.terminate()
        try:
            process.wait(timeout=8)
        except subprocess.TimeoutExpired:
            process.kill()


@pytest.fixture()
def app_base_url(test_config: TestConfig) -> str:
    return test_config.base_url


@pytest.fixture()
def api_client(test_config: TestConfig) -> requests.Session:
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    session.base_url = test_config.base_url  # type: ignore[attr-defined]
    return session


@pytest.fixture(scope="session")
def login_test_data() -> dict:
    data_file = Path(os.getenv("LANGNATION_LOGIN_DATA", TEST_DATA_DIR / "login_users.example.json"))
    with data_file.open(encoding="utf-8") as file:
        return json.load(file)



