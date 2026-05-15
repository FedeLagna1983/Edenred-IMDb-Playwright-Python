from __future__ import annotations

import re

from playwright.sync_api import Locator, expect

from pages.base_page import BasePage


class MediaGalleryPage(BasePage):
    BREAKING_BAD_TITLE_ID = "tt0903747"
    DANNY_TREJO_NAME_ID = "nm0001803"

    def open_from_current_title(self) -> None:
        self.page.evaluate("window.stop()")

    def filter_by_danny_trejo(self) -> None:
        self._goto_mediaindex(cast_filter=self.DANNY_TREJO_NAME_ID)

    def open_second_photo(self) -> None:
        link = self.media_links.nth(1)
        expect(link).to_be_visible(timeout=20_000)
        self.open_url(self.href_or_fail(link, "Second media link does not have an href."))
        expect(self.page).to_have_url(re.compile(r"/title/.*/mediaviewer/|/media/"))

    @property
    def media_links(self) -> Locator:
        return self.page.locator('a[href*="/mediaviewer/"], a[href*="/media/"]').filter(
            has_text=re.compile(r"\S|^$")
        )

    def _goto_mediaindex(self, cast_filter: str | None = None) -> None:
        query = f"?cast={cast_filter}" if cast_filter else ""
        self.open_url_resilient(f"title/{self.BREAKING_BAD_TITLE_ID}/mediaindex/{query}")
