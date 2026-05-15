from __future__ import annotations

import re
from urllib.parse import urlparse

from playwright.sync_api import Locator, expect

from pages.base_page import BasePage


class BoxOfficePage(BasePage):
    def open_second_movie(self) -> None:
        self.open_movie_by_index(1)
        expect(self.page).to_have_url(re.compile(r"/title/"))

    def open_movie_by_index(self, index: int) -> None:
        href = self.movie_links.nth(index).get_attribute("href")
        if not href:
            raise AssertionError(f"Movie link at index {index} does not have an href.")
        path = urlparse(href).path
        self.page.goto(f"{self.BASE_URL}{path}", wait_until="domcontentloaded")

    @property
    def movie_links(self) -> Locator:
        return self.page.locator('a.ipc-title-link-wrapper[href*="/title/"]').filter(has_text=re.compile(r"\S"))
