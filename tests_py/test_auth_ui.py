from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from tests_py.pages.auth_modal import AuthModal
from tests_py.pages.dictionary_page import DictionaryPage


@pytest.mark.ui
@pytest.mark.auth
@pytest.mark.data
def test_sign_in_form_submits_with_test_data(page: Page, app_base_url: str, login_test_data: dict) -> None:
    user = login_test_data["valid_user"]
    page.route(
        "**/api/auth/signin",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=f"""{{"token":"mock-token","user":{{"email":"{user['email']}","name":"{user['name']}"}}}}""",
        ),
    )
    dictionary = DictionaryPage(page, app_base_url)
    dictionary.open()
    auth = AuthModal(page, app_base_url)
    auth.open_sign_in()

    auth.sign_in(user["email"], user["password"])

    expect(page.locator(".ln-toast")).to_contain_text("Welcome", timeout=10_000)


@pytest.mark.ui
@pytest.mark.auth
def test_sign_in_shows_error_for_invalid_user(page: Page, app_base_url: str, login_test_data: dict) -> None:
    user = login_test_data["invalid_user"]
    page.route(
        "**/api/auth/signin",
        lambda route: route.fulfill(
            status=401,
            content_type="application/json",
            body='{"error":"Incorrect password. Please try again."}',
        ),
    )
    dictionary = DictionaryPage(page, app_base_url)
    dictionary.open()
    auth = AuthModal(page, app_base_url)
    auth.open_sign_in()

    auth.sign_in(user["email"], user["password"])

    expect(page.locator(".ln-err")).to_contain_text("Incorrect password", timeout=10_000)


@pytest.mark.ui
@pytest.mark.auth
def test_google_login_callback_saves_session(page: Page, app_base_url: str) -> None:
    page.route(
        "**/api/auth/google",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"token":"mock-google-token","user":{"email":"google.qa@example.com","name":"Google QA"}}',
        ),
    )
    dictionary = DictionaryPage(page, app_base_url)
    dictionary.open()

    page.evaluate("window.lnGoogleAuth('mock-google-credential')")

    expect(page.locator(".ln-toast")).to_contain_text("Welcome", timeout=10_000)
    assert page.evaluate("localStorage.getItem('ln_token')") == "mock-google-token"


@pytest.mark.ui
@pytest.mark.auth
def test_logout_clears_saved_session(page: Page, app_base_url: str) -> None:
    page.add_init_script(
        """
        localStorage.setItem('ln_token', 'mock-token');
        localStorage.setItem('ln_user', JSON.stringify({email:'qa.user@example.com', name:'QA User'}));
        """
    )
    page.route(
        "**/api/auth/me",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"user":{"email":"qa.user@example.com","name":"QA User"}}',
        ),
    )
    page.route(
        "**/api/auth/signout",
        lambda route: route.fulfill(status=200, content_type="application/json", body='{"ok":true}'),
    )
    dictionary = DictionaryPage(page, app_base_url)
    dictionary.open()

    page.evaluate("window.lnSignOut()")

    expect(page.locator(".ln-toast")).to_contain_text("Signed out", timeout=10_000)
    assert page.evaluate("localStorage.getItem('ln_token')") is None
