from __future__ import annotations

from urllib.parse import quote_plus

from pages.base_page import BasePage


class HomePage(BasePage):
    def open(self) -> None:
        self.open_url("")

    def search_person(self, person_name: str) -> None:
        self.open_url(f"find/?q={quote_plus(person_name)}&s=nm")
        self.page.wait_for_load_state("domcontentloaded")
