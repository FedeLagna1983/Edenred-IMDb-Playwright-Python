from __future__ import annotations

from pages.base_page import BasePage


class MenuPage(BasePage):
    TOP_BOX_OFFICE_URL = "/chart/boxoffice/"
    TOP_250_TV_URL = "/chart/toptv/"
    BORN_TODAY_URL = "/search/name/?birth_monthday="

    def open_top_box_office(self) -> None:
        self.page.goto(f"{self.BASE_URL}{self.TOP_BOX_OFFICE_URL}", wait_until="domcontentloaded")
        self.accept_cookies_if_present()

    def open_top_250_tv(self) -> None:
        self.page.goto(f"{self.BASE_URL}{self.TOP_250_TV_URL}", wait_until="domcontentloaded")
        self.accept_cookies_if_present()

    def open_born_today(self) -> None:
        self.page.goto(f"{self.BASE_URL}{self.BORN_TODAY_URL}", wait_until="domcontentloaded")
        self.accept_cookies_if_present()

