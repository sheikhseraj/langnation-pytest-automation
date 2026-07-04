from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from tests_py.pages.dictionary_page import (
    DictionaryPage,
    mock_examples,
    mock_lookup_success,
    mock_lookup_with_noun_forms,
    mock_lookup_with_verb_forms,
    mock_regional_lookup,
)


@pytest.mark.ui
def test_dark_mode_toggle_changes_theme(page: Page, app_base_url: str) -> None:
    dictionary = DictionaryPage(page, app_base_url)
    dictionary.open()

    dictionary.toggle_dark_mode()

    expect(page.locator(".dc-root")).to_have_attribute("data-theme", "dark")
    assert page.evaluate("localStorage.getItem('ln_theme')") == "dark"


@pytest.mark.ui
def test_regional_language_lookup_updates_result(page: Page, app_base_url: str) -> None:
    mock_lookup_success(page)
    mock_regional_lookup(page)
    dictionary = DictionaryPage(page, app_base_url)
    dictionary.open()
    dictionary.search("Haus")

    dictionary.select_regional_language("Hindi")

    expect(page.locator("body")).to_contain_text("घर", timeout=10_000)


@pytest.mark.ui
def test_verb_lookup_can_show_conjugation_table(page: Page, app_base_url: str) -> None:
    mock_lookup_with_verb_forms(page)
    dictionary = DictionaryPage(page, app_base_url)
    dictionary.open()

    dictionary.search("gehen")
    page.locator("button").filter(has_text="Conjugation").first.click()

    expect(page.locator("body")).to_contain_text("aux", timeout=10_000)
    expect(page.locator("body")).to_contain_text("gegangen")


@pytest.mark.ui
def test_noun_lookup_can_show_declension_table(page: Page, app_base_url: str) -> None:
    mock_lookup_with_noun_forms(page)
    dictionary = DictionaryPage(page, app_base_url)
    dictionary.open()

    dictionary.search("Haus")
    page.locator("button").filter(has_text="Declension").first.click()

    expect(page.locator("body")).to_contain_text("declension", timeout=10_000)
    expect(page.locator("body")).to_contain_text("Haeuser")
