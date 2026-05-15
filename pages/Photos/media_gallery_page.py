from __future__ import annotations

import re
from urllib.parse import urlparse

from playwright.sync_api import Error, Locator, expect

from pages.base_page import BasePage


class MediaGalleryPage(BasePage):
    BREAKING_BAD_TITLE_ID = "tt0903747"
    DANNY_TREJO_NAME_ID = "nm0001803"

    def open_from_current_title(self) -> None:
        self.page.evaluate("window.stop()")

    def filter_by_danny_trejo(self) -> None:
        self._goto_mediaindex(cast_filter=self.DANNY_TREJO_NAME_ID)

    def open_second_photo(self) -> None:
        expect(self.media_links.nth(1)).to_be_visible(timeout=20_000)
        href = self.media_links.nth(1).get_attribute("href")
        if not href:
            raise AssertionError("Second media link does not have an href.")
        path = urlparse(href).path
        self.page.goto(f"{self.BASE_URL}{path}", wait_until="domcontentloaded")
        expect(self.page).to_have_url(re.compile(r"/title/.*/mediaviewer/|/media/"))

    @property
    def media_links(self) -> Locator:
        return self.page.locator('a[href*="/mediaviewer/"], a[href*="/media/"]').filter(
            has_text=re.compile(r"\S|^$")
        )

    def _goto_mediaindex(self, cast_filter: str | None = None) -> None:
        query = f"?cast={cast_filter}" if cast_filter else ""
        url = f"{self.BASE_URL}/title/{self.BREAKING_BAD_TITLE_ID}/mediaindex/{query}"
        for _ in range(2):
            try:
                self.page.goto(url, wait_until="commit")
                self.page.wait_for_load_state("domcontentloaded")
                return
            except Error:
                self.page.evaluate("window.stop()")
                self.page.wait_for_timeout(500)
        self.page.goto(url, wait_until="domcontentloaded")
