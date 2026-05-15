from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from playwright.sync_api import Page

from pages.Charts import BoxOfficePage, TopTvPage
from pages.Home import HomePage
from pages.Menu import MenuPage
from pages.Name import PersonPage
from pages.Photos import MediaGalleryPage
from pages.Search import NameSearchPage
from pages.Title import TitlePage


@dataclass(frozen=True)
class ImdbPages:
    home: HomePage
    menu: MenuPage
    search: NameSearchPage
    person: PersonPage
    box_office: BoxOfficePage
    top_tv: TopTvPage
    media_gallery: MediaGalleryPage
    title: TitlePage

    @classmethod
    def create(cls, page: Page) -> "ImdbPages":
        return cls(
            home=HomePage(page),
            menu=MenuPage(page),
            search=NameSearchPage(page),
            person=PersonPage(page),
            box_office=BoxOfficePage(page),
            top_tv=TopTvPage(page),
            media_gallery=MediaGalleryPage(page),
            title=TitlePage(page),
        )

    def open_nicolas_cage_completed_upcoming_title(self) -> None:
        self.home.search_person("Nicolas Cage")
        self.search.open_person_result("Nicolas Cage")
        self.person.open_first_completed_upcoming_credit()

    def rate_second_top_box_office_movie_until_sign_in(self) -> None:
        self.menu.open_top_box_office()
        self.box_office.open_second_movie()
        self.title.rate_with_five_stars_until_sign_in()

    def open_breaking_bad_second_danny_trejo_photo(self) -> None:
        self.menu.open_top_250_tv()
        self.top_tv.open_breaking_bad()
        self.media_gallery.open_from_current_title()
        self.media_gallery.filter_by_danny_trejo()
        self.media_gallery.open_second_photo()

    def capture_third_person_born_yesterday(self, screenshot_path: Path) -> None:
        self.menu.open_born_today()
        self.search.open_people_born_yesterday()
        self.search.open_third_person_result_and_capture(screenshot_path)

    def capture_first_description_link_for_person_born_40_years_ago(self, screenshot_path: Path) -> None:
        self.menu.open_born_today()
        self.search.open_people_born_exactly_40_years_ago()
        self.search.open_first_description_link_or_capture_results(screenshot_path)
