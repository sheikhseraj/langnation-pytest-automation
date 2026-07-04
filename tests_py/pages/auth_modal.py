from __future__ import annotations

from playwright.sync_api import expect

from tests_py.pages.base_page import BasePage


class AuthModal(BasePage):
    def open_sign_in(self) -> None:
        self.page.evaluate("window.lnOpenAuth && window.lnOpenAuth('signin')")
        expect(self.page.locator(".ln-modal")).to_be_visible()

    def expect_sign_in_fields(self) -> None:
        expect(self.page.locator(".ln-modal input[type='email']")).to_be_visible()
        expect(self.page.locator(".ln-modal input[type='password']")).to_be_visible()

    def sign_in(self, email: str, password: str) -> None:
        self.page.locator(".ln-modal input[type='email']").fill(email)
        self.page.locator(".ln-modal input[type='password']").fill(password)
        self.page.locator(".ln-modal button[type='submit'], .ln-modal .ln-btn").first.click()
