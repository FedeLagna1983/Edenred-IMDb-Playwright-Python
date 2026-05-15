from __future__ import annotations

import re

from playwright.sync_api import expect

from pages.base_page import BasePage


class SignInPage(BasePage):
    def open(self) -> None:
        self.page.goto(f"{self.BASE_URL}/registration/signin", wait_until="domcontentloaded")
        self.accept_cookies_if_present()

    def login(self, email: str, password: str) -> None:
        self.open()

        imdb_sign_in = self.page.get_by_role("link", name=re.compile(r"sign in with imdb", re.I))
        if imdb_sign_in.count() > 0:
            imdb_sign_in.first.click()

        self.page.locator("#ap_email").fill(email)
        self.page.locator("#ap_password").fill(password)
        self.page.locator("#signInSubmit").click()
        expect(self.page.locator("body")).not_to_contain_text(re.compile(r"there was a problem", re.I))

