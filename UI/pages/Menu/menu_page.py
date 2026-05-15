from __future__ import annotations

from pages.base_page import BasePage


class MenuPage(BasePage):
    TOP_BOX_OFFICE_URL = "chart/boxoffice/"
    TOP_250_TV_URL = "chart/toptv/"
    BORN_TODAY_URL = "search/name/?birth_monthday="

    def open_top_box_office(self) -> None:
        self.open_url(self.TOP_BOX_OFFICE_URL)

    def open_top_250_tv(self) -> None:
        self.open_url(self.TOP_250_TV_URL)

    def open_born_today(self) -> None:
        self.open_url(self.BORN_TODAY_URL)
