from __future__ import annotations

from playwright.sync_api import Page, expect

from tests_py.pages.base_page import BasePage


class DictionaryPage(BasePage):
    @property
    def search_input(self):
        return self.page.locator(".dc-input")

    @property
    def desktop_search_button(self):
        return self.page.locator(".dc-inputrow .dc-go")

    @property
    def mode_buttons(self):
        return self.page.locator(".dc-seg button")

    @property
    def result_meta(self):
        return self.page.locator(".dc-meta")

    def open(self) -> None:
        self.goto("/")
        self.expect_loaded()
        expect(self.search_input).to_be_visible()

    def search(self, word: str) -> None:
        self.search_input.fill(word)
        expect(self.desktop_search_button).to_be_enabled()
        self.desktop_search_button.click()

    def expect_empty_search_disabled(self) -> None:
        expect(self.desktop_search_button).to_be_disabled()

    def expect_result_for(self, source: str, target: str) -> None:
        expect(self.result_meta).to_contain_text(source)
        expect(self.page.get_by_text(target, exact=False).first).to_be_visible()

    def choose_manual_direction(self) -> None:
        self.mode_buttons.nth(1).click()

    def open_study_menu(self) -> None:
        self.page.get_by_role("button", name="Menu").click()

    def toggle_dark_mode(self) -> None:
        self.page.get_by_label("Toggle theme").click()

    def select_regional_language(self, language_name: str) -> None:
        self.page.locator(".dc-regional-trigger").click()
        self.page.locator(".dc-regional-opt").filter(has_text=language_name).first.click()


def mock_lookup_success(page: Page) -> None:
    page.route(
        "**/api/lookup",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body="""{
              "query": "Haus",
              "from": "de",
              "to": "en",
              "_source": "pytest-mock",
              "entries": [{
                "source": "Haus",
                "target": "house",
                "pos": "noun",
                "gender": "n",
                "article": "das",
                "plural": "Haeuser",
                "example_source": "Das Haus ist gross.",
                "example_target": "The house is big.",
                "examples": []
              }]
            }""",
        ),
    )


def mock_word_of_day(page: Page, word: str = "Haus") -> None:
    page.route(
        "**/api/word-of-day",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=f'{{"date":"2026-07-04","word":"{word}"}}',
        ),
    )


def mock_examples(page: Page) -> None:
    page.route(
        "**/api/examples",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"words":["Haus","gehen","schnell"]}',
        ),
    )


def mock_regional_lookup(page: Page, translation: str = "घर") -> None:
    page.route(
        "**/api/lookup-regional",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=f'{{"translation":"{translation}","transliteration":"ghar","language_name":"Hindi"}}',
        ),
    )


def mock_lookup_with_verb_forms(page: Page) -> None:
    page.route(
        "**/api/lookup",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body="""{
              "query": "gehen",
              "from": "de",
              "to": "en",
              "_source": "pytest-mock",
              "entries": [{
                "source": "gehen",
                "target": "to go",
                "pos": "verb",
                "praeteritum": "ging",
                "perfekt": "ist gegangen",
                "example_source": "Ich gehe nach Hause.",
                "example_target": "I go home.",
                "from_vocabulary": true,
                "verb_forms": {
                  "infinitive_de": "gehen",
                  "praeteritum": "[\\"ich ging\\",\\"du gingst\\",\\"er ging\\"]",
                  "perfekt": "[\\"ich bin gegangen\\",\\"du bist gegangen\\",\\"er ist gegangen\\"]",
                  "partizip2": "gegangen",
                  "auxiliary": "sein"
                },
                "examples": []
              }]
            }""",
        ),
    )


def mock_lookup_with_noun_forms(page: Page) -> None:
    page.route(
        "**/api/lookup",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body="""{
              "query": "Haus",
              "from": "de",
              "to": "en",
              "_source": "pytest-mock",
              "entries": [{
                "source": "Haus",
                "target": "house",
                "pos": "noun",
                "gender": "n",
                "article": "das",
                "plural": "Haeuser",
                "example_source": "Das Haus ist gross.",
                "example_target": "The house is big.",
                "from_vocabulary": true,
                "noun_forms": {
                  "gender": "n",
                  "article": "das",
                  "plural_de": "Haeuser",
                  "singular_forms": "[\\"das Haus\\",\\"des Hauses\\",\\"dem Haus\\",\\"das Haus\\"]",
                  "plural_forms": "[\\"die Haeuser\\",\\"der Haeuser\\",\\"den Haeusern\\",\\"die Haeuser\\"]",
                  "plural_en": "houses"
                },
                "examples": []
              }]
            }""",
        ),
    )
