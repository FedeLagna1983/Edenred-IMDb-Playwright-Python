from __future__ import annotations

import re
from pathlib import Path

from playwright.sync_api import Error, Locator, expect

from pages.base_page import BasePage
from utils.dates import get_birth_date_filters


class NameSearchPage(BasePage):
    def open_person_result(self, person_name: str) -> None:
        self.person_result_links.filter(has_text=re.compile(person_name, re.I)).first.click()
        expect(self.page).to_have_url(re.compile(r"/name/"))

    def open_people_born_yesterday(self) -> None:
        filters = get_birth_date_filters()
        self._goto_name_search(f"birth_monthday={filters.yesterday_month_day}")
        self.accept_cookies_if_present()

    def open_people_born_exactly_40_years_ago(self) -> None:
        filters = get_birth_date_filters()
        self._goto_name_search(f"birth_date={filters.forty_years_ago},{filters.forty_years_ago}")
        self.accept_cookies_if_present()

    def open_third_person_result_and_capture(self, screenshot_path: Path) -> None:
        self.person_result_links.nth(2).click()
        expect(self.page).to_have_url(re.compile(r"/name/"))
        self.page.screenshot(path=str(screenshot_path), full_page=True)

    def open_first_description_link_or_capture_results(self, screenshot_path: Path) -> None:
        first_result = self.result_items.filter(has=self.page.locator('a[href*="/name/"]')).first
        description_link = first_result.locator('a:not([href*="/name/"])').first

        if description_link.count() == 0:
            self.page.screenshot(path=str(screenshot_path), full_page=True)
            return

        description_link.click()
        self.page.wait_for_load_state("domcontentloaded")
        self.page.screenshot(path=str(screenshot_path), full_page=True)

    @property
    def person_result_links(self) -> Locator:
        return self.page.locator('a[href*="/name/"]').filter(has_text=re.compile(r"\S"))

    @property
    def result_items(self) -> Locator:
        return self.page.locator("li, .ipc-metadata-list-summary-item")
    def _goto_name_search(self, query: str) -> None:
        url = f"{self.BASE_URL}/search/name/?{query}"
        for _ in range(2):
            try:
                self.page.goto(url, wait_until="domcontentloaded")
                return
            except Error:
                self.page.evaluate("window.stop()")
                self.page.wait_for_timeout(500)
        self.page.goto(url, wait_until="commit")
        self.page.wait_for_load_state("domcontentloaded")
