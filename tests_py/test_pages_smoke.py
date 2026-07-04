from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect


PUBLIC_PAGES = [
    pytest.param("/", "Where language", id="dictionary-home"),
    pytest.param("/grammar.html", "German Grammar", id="grammar"),
    pytest.param("/amtsdeutsch.html", "Amtsdeutsch Decoder", id="amtsdeutsch"),
    pytest.param("/reset-password.html?token=dummy", "Choose a new password", id="reset-password"),
    pytest.param("/user-portal.html", "My Account", id="user-portal"),
    pytest.param("/dashboard.html", "Dashboard", id="dashboard"),
    pytest.param("/admin.html", "Admin", id="admin-home"),
    pytest.param("/admin-vocab.html", "Admin", id="admin-vocab"),
    pytest.param("/admin-users.html", "Admin", id="admin-users"),
    pytest.param("/admin-feedback.html", "Admin", id="admin-feedback"),
    pytest.param("/admin-ai-analytics.html", "Admin", id="admin-ai-analytics"),
    pytest.param("/admin-amtsdeutsch.html", "Admin", id="admin-amtsdeutsch"),
    pytest.param("/admin-batches.html", "Admin", id="admin-batches"),
    pytest.param("/admin-batch-progress.html", "Admin", id="admin-batch-progress"),
    pytest.param("/admin-student-search.html", "Admin", id="admin-student-search"),
    pytest.param("/admin-lookup-sources.html", "Admin", id="admin-lookup-sources"),
]


@pytest.mark.ui
@pytest.mark.pages
@pytest.mark.smoke
@pytest.mark.parametrize(("path", "expected_text"), PUBLIC_PAGES)
def test_public_pages_render(page: Page, app_base_url: str, path: str, expected_text: str) -> None:
    page.goto(f"{app_base_url}{path}")

    expect(page.locator("body")).to_contain_text(expected_text, timeout=10_000)
    expect(page.locator("body")).not_to_contain_text("Cannot GET")

