from __future__ import annotations

from urllib.parse import quote_plus

from pages.base_page import BasePage


class HomePage(BasePage):
    def open(self) -> None:
        self.page.goto(self.BASE_URL, wait_until="domcontentloaded")
        self.accept_cookies_if_present()

    def search_person(self, person_name: str) -> None:
        self.open()
        self.page.goto(
            f"{self.BASE_URL}/find/?q={quote_plus(person_name)}&s=nm",
            wait_until="domcontentloaded",
        )
        self.page.wait_for_load_state("domcontentloaded")

