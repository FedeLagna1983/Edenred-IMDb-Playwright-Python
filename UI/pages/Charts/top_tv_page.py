from __future__ import annotations

import re

from playwright.sync_api import expect

from pages.base_page import BasePage


class TopTvPage(BasePage):
    BREAKING_BAD_TITLE_ID = "tt0903747"

    def open_breaking_bad(self) -> None:
        title_path = f"title/{self.BREAKING_BAD_TITLE_ID}/"
        link = self.page.locator(f'a.ipc-title-link-wrapper[href*="/{title_path}"]').first
        href = link.get_attribute("href") if link.count() > 0 else None
        self.open_url(href or title_path)
        expect(self.page).to_have_url(re.compile(rf"/title/{self.BREAKING_BAD_TITLE_ID}/"))
