from __future__ import annotations

import re
from urllib.parse import urljoin

from playwright.sync_api import Error, Locator, Page


class BasePage:
    BASE_URL = "https://www.imdb.com"

    def __init__(self, page: Page) -> None:
        self.page = page

    def open_url(self, path_or_url: str, *, wait_until: str = "domcontentloaded") -> None:
        self.page.goto(self.absolute_url(path_or_url), wait_until=wait_until)
        self.accept_cookies_if_present()

    def open_url_resilient(self, path_or_url: str) -> None:
        url = self.absolute_url(path_or_url)
        for _ in range(2):
            try:
                self.page.goto(url, wait_until="domcontentloaded")
                return
            except Error:
                self.page.evaluate("window.stop()")
                self.page.wait_for_timeout(500)
        self.page.goto(url, wait_until="commit")
        self.page.wait_for_load_state("domcontentloaded")

    def absolute_url(self, path_or_url: str) -> str:
        return urljoin(f"{self.BASE_URL}/", path_or_url)

    def accept_cookies_if_present(self) -> None:
        for name in (re.compile(r"accept", re.I), re.compile(r"aceptar", re.I), re.compile(r"agree", re.I)):
            button = self.page.get_by_role("button", name=name)
            if button.count() == 0:
                continue
            try:
                button.first.click(timeout=2_000)
                return
            except Error:
                continue

    def click_if_available(self, locator: Locator) -> bool:
        if locator.count() == 0:
            return False
        try:
            locator.first.click(timeout=3_000)
            self.page.wait_for_load_state("domcontentloaded")
            return True
        except Error:
            return False

    def click_or_open_href(self, locator: Locator) -> None:
        try:
            locator.click(timeout=5_000)
            return
        except Error:
            href = locator.get_attribute("href")
            if not href:
                raise
            self.open_url(href)

    def href_or_fail(self, locator: Locator, message: str) -> str:
        href = locator.get_attribute("href")
        if not href:
            raise AssertionError(message)
        return href
