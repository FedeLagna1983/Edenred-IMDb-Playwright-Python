from __future__ import annotations

import re
from pathlib import Path

from behave import given, then, when
from playwright.sync_api import expect


@given('I search IMDb for the person "{person_name}"')
def step_search_person(context, person_name: str) -> None:
    context.imdb.home.search_person(person_name)


@when('I open the "{person_name}" person result')
def step_open_person_result(context, person_name: str) -> None:
    context.imdb.search.open_person_result(person_name)


@when("I open the first completed upcoming credit")
def step_open_first_completed_upcoming_credit(context) -> None:
    context.imdb.person.open_first_completed_upcoming_credit()


@then("I should be on an IMDb title page")
def step_should_be_on_title_page(context) -> None:
    expect(context.page).to_have_url(re.compile(r"/title/"))


@given("I open the IMDb top box office page")
def step_open_top_box_office(context) -> None:
    context.imdb.menu.open_top_box_office()


@when("I open the second box office movie")
def step_open_second_box_office_movie(context) -> None:
    context.imdb.box_office.open_second_movie()


@when("I select 5 stars in the rating prompt")
def step_select_five_star_rating(context) -> None:
    context.imdb.title.open_rating_prompt()
    context.imdb.title.select_five_stars()


@when("I submit the rating")
def step_submit_rating(context) -> None:
    context.imdb.title.submit_rating()


@then("I should be redirected to the IMDb sign in page")
def step_should_be_on_sign_in(context) -> None:
    context.imdb.title.expect_sign_in_screen()


@given("I open the IMDb top 250 TV page")
def step_open_top_250_tv(context) -> None:
    context.imdb.menu.open_top_250_tv()


@when("I open the Breaking Bad title page")
def step_open_breaking_bad(context) -> None:
    context.imdb.top_tv.open_breaking_bad()


@when("I open the Breaking Bad photo gallery")
def step_open_breaking_bad_gallery(context) -> None:
    context.imdb.media_gallery.open_from_current_title()


@when("I filter the gallery by Danny Trejo")
def step_filter_gallery_by_danny_trejo(context) -> None:
    context.imdb.media_gallery.filter_by_danny_trejo()


@when("I open the second media photo")
def step_open_second_media_photo(context) -> None:
    context.imdb.media_gallery.open_second_photo()


@then("I should be on an IMDb media viewer page")
def step_should_be_on_media_viewer(context) -> None:
    expect(context.page).to_have_url(re.compile(r"/title/.*/mediaviewer/|/media/"))


@given("I open IMDb born today")
def step_open_born_today(context) -> None:
    context.imdb.menu.open_born_today()


@when("I search for celebrities born yesterday")
def step_search_born_yesterday(context) -> None:
    context.imdb.search.open_people_born_yesterday()


@when('I open the third person result and capture "{screenshot_name}"')
def step_open_third_result_and_capture(context, screenshot_name: str) -> None:
    screenshot_path = _screenshot_path(context, screenshot_name)
    context.imdb.search.open_third_person_result_and_capture(screenshot_path)
    context.latest_screenshot = screenshot_path


@when("I search for celebrities born exactly 40 years ago")
def step_search_born_40_years_ago(context) -> None:
    context.imdb.search.open_people_born_exactly_40_years_ago()


@when('I open the first description link and capture "{screenshot_name}"')
def step_open_first_description_link_and_capture(context, screenshot_name: str) -> None:
    screenshot_path = _screenshot_path(context, screenshot_name)
    context.imdb.search.open_first_description_link_or_capture_results(screenshot_path)
    context.latest_screenshot = screenshot_path


@then('the screenshot "{screenshot_name}" should exist')
def step_screenshot_should_exist(context, screenshot_name: str) -> None:
    assert _screenshot_path(context, screenshot_name).exists()


def _screenshot_path(context, screenshot_name: str) -> Path:
    return context.screenshots_dir / f"{screenshot_name}_{context.browser_name}.png"
