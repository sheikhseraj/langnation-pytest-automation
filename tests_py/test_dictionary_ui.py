from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from tests_py.pages.auth_modal import AuthModal
from tests_py.pages.dictionary_page import DictionaryPage, mock_lookup_success


@pytest.mark.ui
@pytest.mark.smoke
def test_homepage_loads_dictionary_search(page: Page, app_base_url: str) -> None:
    dictionary = DictionaryPage(page, app_base_url)

    dictionary.open()

    expect(page.get_by_role("heading", name="Where language, connects nations.")).to_be_visible()
    dictionary.expect_empty_search_disabled()


@pytest.mark.ui
@pytest.mark.smoke
def test_dictionary_search_renders_result_from_api(page: Page, app_base_url: str) -> None:
    mock_lookup_success(page)
    dictionary = DictionaryPage(page, app_base_url)
    dictionary.open()

    dictionary.search("Haus")

    dictionary.expect_result_for("Haus", "house")
    expect(page.get_by_text("1 result")).to_be_visible()
    expect(page.get_by_role("button", name="Clear")).to_be_visible()


@pytest.mark.ui
def test_direction_toggle_keeps_search_usable(page: Page, app_base_url: str) -> None:
    dictionary = DictionaryPage(page, app_base_url)
    dictionary.open()

    dictionary.choose_manual_direction()
    dictionary.search_input.fill("house")

    expect(dictionary.desktop_search_button).to_be_enabled()


@pytest.mark.ui
@pytest.mark.auth
def test_auth_modal_can_open_sign_in_form(page: Page, app_base_url: str) -> None:
    dictionary = DictionaryPage(page, app_base_url)
    dictionary.open()
    auth = AuthModal(page, app_base_url)

    auth.open_sign_in()

    auth.expect_sign_in_fields()


