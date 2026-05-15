from __future__ import annotations

import re

from playwright.sync_api import expect

from pages.base_page import BasePage


class TopTvPage(BasePage):
    BREAKING_BAD_TITLE_ID = "tt0903747"

    def open_breaking_bad(self) -> None:
        link = self.page.locator(f'a.ipc-title-link-wrapper[href*="/title/{self.BREAKING_BAD_TITLE_ID}/"]').first
        if link.count() > 0:
            href = link.get_attribute("href")
            if href:
                self.page.goto(f"{self.BASE_URL}{href}" if href.startswith("/") else href, wait_until="domcontentloaded")
            else:
                self.page.goto(f"{self.BASE_URL}/title/{self.BREAKING_BAD_TITLE_ID}/", wait_until="domcontentloaded")
        else:
            self.page.goto(f"{self.BASE_URL}/title/{self.BREAKING_BAD_TITLE_ID}/", wait_until="domcontentloaded")
        expect(self.page).to_have_url(re.compile(rf"/title/{self.BREAKING_BAD_TITLE_ID}/"))
