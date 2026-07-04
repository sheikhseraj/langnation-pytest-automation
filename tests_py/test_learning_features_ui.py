from __future__ import annotations

import re

import pytest
from playwright.sync_api import Page, expect

from tests_py.pages.dictionary_page import DictionaryPage, mock_examples, mock_word_of_day


def _mock_signed_in_user(page: Page) -> None:
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


@pytest.mark.ui
def test_quiz_button_opens_quiz_panel(page: Page, app_base_url: str) -> None:
    mock_examples(page)
    dictionary = DictionaryPage(page, app_base_url)
    dictionary.open()

    page.get_by_role("button", name="Quiz").click()

    expect(page.locator(".dc-studytitle")).to_contain_text("Vocabulary quiz")


@pytest.mark.ui
def test_flashcards_button_opens_flashcard_panel(page: Page, app_base_url: str) -> None:
    mock_examples(page)
    dictionary = DictionaryPage(page, app_base_url)
    dictionary.open()

    page.get_by_role("button", name="Flashcards").click()

    expect(page.locator(".dc-studytitle")).to_contain_text("Flashcards")


@pytest.mark.ui
def test_study_menu_lists_main_learning_features(page: Page, app_base_url: str) -> None:
    dictionary = DictionaryPage(page, app_base_url)
    dictionary.open()

    dictionary.open_study_menu()

    for label in ["Progress", "Quiz", "Flashcards", "Grammar", "Vocab by Topic", "Expressions", "Amtsdeutsch"]:
        expect(page.locator(".study-menu")).to_contain_text(label)


@pytest.mark.ui
def test_topics_menu_opens_topic_view_for_signed_in_user(page: Page, app_base_url: str) -> None:
    _mock_signed_in_user(page)
    dictionary = DictionaryPage(page, app_base_url)
    dictionary.open()

    dictionary.open_study_menu()
    page.locator(".study-menu-item").filter(has_text="Vocab by Topic").click()

    expect(page.locator(".topics-view")).to_be_visible()
    expect(page.locator(".topics-view")).to_contain_text("vocabulary", timeout=10_000)


@pytest.mark.ui
def test_expressions_menu_opens_expressions_view_for_signed_in_user(page: Page, app_base_url: str) -> None:
    _mock_signed_in_user(page)
    dictionary = DictionaryPage(page, app_base_url)
    dictionary.open()

    dictionary.open_study_menu()
    page.locator(".study-menu-item").filter(has_text="Expressions").click()

    expect(page.locator(".expressions-view").first).to_be_visible()


@pytest.mark.ui
def test_grammar_menu_routes_to_grammar_page_for_signed_in_user(page: Page, app_base_url: str) -> None:
    _mock_signed_in_user(page)
    dictionary = DictionaryPage(page, app_base_url)
    dictionary.open()

    dictionary.open_study_menu()
    page.locator(".study-menu-item").filter(has_text="Grammar").click()

    expect(page).to_have_url(re.compile(r"/grammar\.html$"))


@pytest.mark.ui
def test_word_of_day_button_appears_and_runs_lookup(page: Page, app_base_url: str) -> None:
    mock_word_of_day(page, "Haus")
    mock_examples(page)
    dictionary = DictionaryPage(page, app_base_url)
    dictionary.open()

    expect(page.get_by_text("Word of the day")).to_be_visible(timeout=10_000)
    expect(page.get_by_role("button", name=re.compile(r"Word of the day.*Haus"))).to_be_visible()
