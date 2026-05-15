from __future__ import annotations

import re
from pathlib import Path

from behave import given, then, when
from playwright.sync_api import expect

from pages.Charts import BoxOfficePage, TopTvPage
from pages.Home import HomePage
from pages.Menu import MenuPage
from pages.Name import PersonPage
from pages.Photos import MediaGalleryPage
from pages.Search import NameSearchPage
from pages.Title import TitlePage


@given('I search IMDb for the person "{person_name}"')
def step_search_person(context, person_name: str) -> None:
    HomePage(context.page).search_person(person_name)


@when('I open the "{person_name}" person result')
def step_open_person_result(context, person_name: str) -> None:
    NameSearchPage(context.page).open_person_result(person_name)


@when("I open the first completed upcoming credit")
def step_open_first_completed_upcoming_credit(context) -> None:
    PersonPage(context.page).open_first_completed_upcoming_credit()


@then("I should be on an IMDb title page")
def step_should_be_on_title_page(context) -> None:
    expect(context.page).to_have_url(re.compile(r"/title/"))


@given("I open the IMDb top box office page")
def step_open_top_box_office(context) -> None:
    MenuPage(context.page).open_top_box_office()


@when("I open the second box office movie")
def step_open_second_box_office_movie(context) -> None:
    BoxOfficePage(context.page).open_second_movie()


@when("I select 5 stars in the rating prompt")
def step_select_five_star_rating(context) -> None:
    title_page = TitlePage(context.page)
    title_page.open_rating_prompt()
    title_page.select_five_stars()


@when("I submit the rating")
def step_submit_rating(context) -> None:
    TitlePage(context.page).submit_rating()


@then("I should be redirected to the IMDb sign in page")
def step_should_be_on_sign_in(context) -> None:
    TitlePage(context.page).expect_sign_in_screen()


@given("I open the IMDb top 250 TV page")
def step_open_top_250_tv(context) -> None:
    MenuPage(context.page).open_top_250_tv()


@when("I open the Breaking Bad title page")
def step_open_breaking_bad(context) -> None:
    TopTvPage(context.page).open_breaking_bad()


@when("I open the Breaking Bad photo gallery")
def step_open_breaking_bad_gallery(context) -> None:
    MediaGalleryPage(context.page).open_from_current_title()


@when("I filter the gallery by Danny Trejo")
def step_filter_gallery_by_danny_trejo(context) -> None:
    MediaGalleryPage(context.page).filter_by_danny_trejo()


@when("I open the second media photo")
def step_open_second_media_photo(context) -> None:
    MediaGalleryPage(context.page).open_second_photo()


@then("I should be on an IMDb media viewer page")
def step_should_be_on_media_viewer(context) -> None:
    expect(context.page).to_have_url(re.compile(r"/title/.*/mediaviewer/|/media/"))


@given("I open IMDb born today")
def step_open_born_today(context) -> None:
    MenuPage(context.page).open_born_today()


@when("I search for celebrities born yesterday")
def step_search_born_yesterday(context) -> None:
    NameSearchPage(context.page).open_people_born_yesterday()


@when('I open the third person result and capture "{screenshot_name}"')
def step_open_third_result_and_capture(context, screenshot_name: str) -> None:
    screenshot_path = _screenshot_path(context, screenshot_name)
    NameSearchPage(context.page).open_third_person_result_and_capture(screenshot_path)
    context.latest_screenshot = screenshot_path


@when("I search for celebrities born exactly 40 years ago")
def step_search_born_40_years_ago(context) -> None:
    NameSearchPage(context.page).open_people_born_exactly_40_years_ago()


@when('I open the first description link and capture "{screenshot_name}"')
def step_open_first_description_link_and_capture(context, screenshot_name: str) -> None:
    screenshot_path = _screenshot_path(context, screenshot_name)
    NameSearchPage(context.page).open_first_description_link_or_capture_results(screenshot_path)
    context.latest_screenshot = screenshot_path


@then('the screenshot "{screenshot_name}" should exist')
def step_screenshot_should_exist(context, screenshot_name: str) -> None:
    assert _screenshot_path(context, screenshot_name).exists()


def _screenshot_path(context, screenshot_name: str) -> Path:
    return context.screenshots_dir / f"{screenshot_name}_{context.browser_name}.png"

