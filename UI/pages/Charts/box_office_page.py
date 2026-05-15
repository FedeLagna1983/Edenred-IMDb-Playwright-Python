from __future__ import annotations

import re

from playwright.sync_api import Locator, expect

from pages.base_page import BasePage


class BoxOfficePage(BasePage):
    def open_second_movie(self) -> None:
        self.open_movie_by_index(1)
        expect(self.page).to_have_url(re.compile(r"/title/"))

    def open_movie_by_index(self, index: int) -> None:
        link = self.movie_links.nth(index)
        self.open_url(self.href_or_fail(link, f"Movie link at index {index} does not have an href."))

    @property
    def movie_links(self) -> Locator:
        return self.page.locator('a.ipc-title-link-wrapper[href*="/title/"]').filter(has_text=re.compile(r"\S"))
