from __future__ import annotations

import re

from playwright.sync_api import expect

from pages.base_page import BasePage


class PersonPage(BasePage):
    def open_first_completed_upcoming_credit(self) -> None:
        self.click_if_available(self.page.get_by_role("button", name=re.compile(r"upcoming|proxim", re.I)))
        self.click_if_available(self.page.get_by_role("link", name=re.compile(r"upcoming|proxim", re.I)))

        completed_item = self.page.locator("li, .ipc-metadata-list-summary-item, .filmo-row").filter(
            has_text=re.compile(r"completed|completada", re.I)
        )
        title_link = completed_item.locator('a[href*="/title/"]').first
        self.click_or_open_href(title_link)
        expect(self.page).to_have_url(re.compile(r"/title/"))

