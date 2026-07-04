from __future__ import annotations

import pytest


@pytest.mark.api
@pytest.mark.smoke
def test_health_endpoint_reports_core_status(api_client) -> None:
    response = api_client.get(f"{api_client.base_url}/api/health", timeout=5)

    assert response.status_code == 200
    payload = response.json()
    assert payload["ok"] is True
    assert "auth" in payload
    assert "aiProviderMain" in payload


@pytest.mark.api
@pytest.mark.smoke
def test_config_endpoint_is_safe_for_browser(api_client) -> None:
    response = api_client.get(f"{api_client.base_url}/api/config", timeout=5)

    assert response.status_code == 200
    payload = response.json()
    assert {"authEnabled", "googleEnabled", "captchaEnabled"}.issubset(payload)
    assert "ANTHROPIC_API_KEY" not in response.text
    assert "OPENAI_API_KEY" not in response.text


@pytest.mark.api
@pytest.mark.smoke
def test_lookup_requires_a_query(api_client) -> None:
    response = api_client.post(
        f"{api_client.base_url}/api/lookup",
        json={"q": "", "mode": "auto"},
        timeout=5,
    )

    assert response.status_code == 400
    assert "word" in response.json()["error"].lower()

