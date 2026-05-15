from __future__ import annotations

from pathlib import Path

import pytest
from playwright.sync_api import Page

from pages.Charts import BoxOfficePage, TopTvPage
from pages.Home import HomePage
from pages.Menu import MenuPage
from pages.Name import PersonPage
from pages.Photos import MediaGalleryPage
from pages.Search import NameSearchPage
from pages.Title import TitlePage


@pytest.mark.ui
@pytest.mark.imdb
def test_nicolas_cage_first_completed_upcoming_credit(page: Page) -> None:
    HomePage(page).search_person("Nicolas Cage")
    NameSearchPage(page).open_person_result("Nicolas Cage")
    PersonPage(page).open_first_completed_upcoming_credit()


@pytest.mark.ui
@pytest.mark.imdb
def test_rate_second_top_box_office_movie_with_five_stars_until_sign_in(page: Page) -> None:
    MenuPage(page).open_top_box_office()
    BoxOfficePage(page).open_second_movie()
    TitlePage(page).rate_with_five_stars_until_sign_in()


@pytest.mark.ui
@pytest.mark.imdb
def test_breaking_bad_second_danny_trejo_photo(page: Page) -> None:
    MenuPage(page).open_top_250_tv()
    TopTvPage(page).open_breaking_bad()
    MediaGalleryPage(page).open_from_current_title()
    MediaGalleryPage(page).filter_by_danny_trejo()
    MediaGalleryPage(page).open_second_photo()


@pytest.mark.ui
@pytest.mark.imdb
def test_third_person_born_yesterday_screenshot(
    page: Page,
    browser_name: str,
    screenshots_dir: Path,
) -> None:
    screenshot_path = screenshots_dir / f"born_yesterday_third_person_{browser_name}.png"

    MenuPage(page).open_born_today()
    NameSearchPage(page).open_people_born_yesterday()
    NameSearchPage(page).open_third_person_result_and_capture(screenshot_path)

    assert screenshot_path.exists()


@pytest.mark.ui
@pytest.mark.imdb
def test_first_description_link_for_person_born_exactly_40_years_ago_screenshot(
    page: Page,
    browser_name: str,
    screenshots_dir: Path,
) -> None:
    screenshot_path = screenshots_dir / f"born_40_years_ago_first_description_link_{browser_name}.png"

    MenuPage(page).open_born_today()
    NameSearchPage(page).open_people_born_exactly_40_years_ago()
    NameSearchPage(page).open_first_description_link_or_capture_results(screenshot_path)

    assert screenshot_path.exists()
