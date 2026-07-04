from __future__ import annotations

import re

from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")

    def goto(self, path: str = "/") -> None:
        self.page.goto(f"{self.base_url}{path}")

    def expect_loaded(self) -> None:
        expect(self.page.locator("#root")).to_be_visible()

    def expect_title_contains(self, text: str) -> None:
        expect(self.page).to_have_title(re.compile(re.escape(text), re.IGNORECASE))


class StaticPage(BasePage):
    def open(self, path: str) -> None:
        self.goto(path)

    def expect_heading(self, name: str) -> None:
        expect(self.page.get_by_role("heading", name=name).first).to_be_visible()
