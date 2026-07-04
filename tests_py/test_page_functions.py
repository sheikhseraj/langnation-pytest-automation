from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.ui
def test_reset_password_mismatch_validation(page: Page, app_base_url: str) -> None:
    page.goto(f"{app_base_url}/reset-password.html?token=dummy-token")

    page.locator("#pw1").fill("Password123!")
    page.locator("#pw2").fill("Different123!")
    page.locator("#btn").click()

    expect(page.locator("#msg")).to_contain_text("Passwords do not match")


@pytest.mark.ui
def test_reset_password_eye_toggle(page: Page, app_base_url: str) -> None:
    page.goto(f"{app_base_url}/reset-password.html?token=dummy-token")

    expect(page.locator("#pw1")).to_have_attribute("type", "password")
    page.locator("[data-eye='pw1']").click()

    expect(page.locator("#pw1")).to_have_attribute("type", "text")


@pytest.mark.ui
def test_amtsdeutsch_consent_unlocks_tool(page: Page, app_base_url: str) -> None:
    page.add_init_script(
        """
        localStorage.setItem('ln_token', 'mock-token');
        localStorage.removeItem('ln_amts_consent_v1');
        """
    )
    page.route(
        "**/api/amtsdeutsch/access-status",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"allowed":true,"status":"approved"}',
        ),
    )
    page.goto(f"{app_base_url}/amtsdeutsch.html")

    expect(page.locator("#amt-consent")).to_be_visible()
    expect(page.locator("#amt-consent-btn")).to_be_disabled()
    page.locator("#amt-consent-cb").check()
    expect(page.locator("#amt-consent-btn")).to_be_enabled()
    page.locator("#amt-consent-btn").click()

    expect(page.locator("#amt-tool")).to_be_visible()


@pytest.mark.ui
def test_amtsdeutsch_decode_button_requires_text(page: Page, app_base_url: str) -> None:
    page.add_init_script(
        """
        localStorage.setItem('ln_token', 'mock-token');
        localStorage.setItem('ln_amts_consent_v1', '1');
        """
    )
    page.route(
        "**/api/amtsdeutsch/access-status",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"allowed":true,"status":"approved"}',
        ),
    )
    page.goto(f"{app_base_url}/amtsdeutsch.html")

    expect(page.locator("#amt-decode-btn")).to_be_disabled()
    page.locator("#amt-text").fill("Bitte reichen Sie die Unterlagen bis morgen ein.")

    expect(page.locator("#amt-decode-btn")).to_be_enabled()

