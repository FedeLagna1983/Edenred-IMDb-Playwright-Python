from __future__ import annotations

import re

from playwright.sync_api import Locator, Page


class BasePage:
    BASE_URL = "https://www.imdb.com"

    def __init__(self, page: Page) -> None:
        self.page = page

    def accept_cookies_if_present(self) -> None:
        cookie_buttons = [
            re.compile(r"accept", re.I),
            re.compile(r"aceptar", re.I),
            re.compile(r"agree", re.I),
        ]
        for name in cookie_buttons:
            button = self.page.get_by_role("button", name=name)
            if button.count() > 0:
                try:
                    button.first.click(timeout=2_000)
                    return
                except Exception:
                    continue

    def click_if_available(self, locator: Locator) -> bool:
        if locator.count() == 0:
            return False
        try:
            locator.first.click(timeout=3_000)
            self.page.wait_for_load_state("domcontentloaded")
            return True
        except Exception:
            return False

    def click_or_open_href(self, locator: Locator) -> None:
        try:
            locator.click(timeout=5_000)
            return
        except Exception:
            href = locator.get_attribute("href")
            if not href:
                raise
            if href.startswith("/"):
                href = f"{self.BASE_URL}{href}"
            self.page.goto(href, wait_until="domcontentloaded")

