from __future__ import annotations

import re

from playwright.sync_api import expect

from pages.base_page import BasePage


class TitlePage(BasePage):
    def rate_with_five_stars_until_sign_in(self) -> None:
        self.open_rating_prompt()
        self.select_five_stars()
        self.submit_rating()
        self.expect_sign_in_screen()

    def open_rating_prompt(self) -> None:
        initial_rate_button = self.page.locator('button[aria-label^="Rate "].ipc-btn--on-textPrimary').filter(
            has_text=re.compile(r"^rate$", re.I)
        )
        expect(initial_rate_button.first).to_be_visible(timeout=20_000)
        for _ in range(3):
            initial_rate_button.first.evaluate("element => element.click()")
            try:
                expect(self.rating_prompt).to_be_visible(timeout=3_000)
                return
            except AssertionError:
                self.page.wait_for_timeout(1_000)
        expect(self.rating_prompt).to_be_visible()

    def select_five_stars(self) -> None:
        star_five = self.rating_prompt.get_by_role("button", name="Rate 5")
        expect(star_five).to_be_visible()
        star_five.evaluate("element => element.click()")
        expect(self.page.locator(".ipc-rating-display__rating")).to_have_text("5")

    def submit_rating(self) -> None:
        submit = self.rating_prompt.locator("button.ipc-rating-prompt__rate-button").filter(
            has_text=re.compile(r"^rate$", re.I)
        )
        expect(submit).to_be_enabled()
        submit.click()

    def expect_sign_in_screen(self) -> None:
        expect(self.page).to_have_url(re.compile(r"/registration/signin|/ap/signin"), timeout=20_000)
        expect(self.page.locator("body")).to_contain_text(re.compile(r"sign in|iniciar sesi", re.I))

    @property
    def rating_prompt(self):
        return self.page.locator(".ipc-rating-prompt__container")
