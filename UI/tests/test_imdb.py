from __future__ import annotations

import re
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from pages import ImdbPages


@pytest.mark.ui
@pytest.mark.imdb
def test_nicolas_cage_first_completed_upcoming_credit(imdb: ImdbPages, page: Page) -> None:
    imdb.open_nicolas_cage_completed_upcoming_title()
    expect(page).to_have_url(re.compile(r"/title/"))


@pytest.mark.ui
@pytest.mark.imdb
def test_rate_second_top_box_office_movie_with_five_stars_until_sign_in(imdb: ImdbPages) -> None:
    imdb.rate_second_top_box_office_movie_until_sign_in()


@pytest.mark.ui
@pytest.mark.imdb
def test_breaking_bad_second_danny_trejo_photo(imdb: ImdbPages, page: Page) -> None:
    imdb.open_breaking_bad_second_danny_trejo_photo()
    expect(page).to_have_url(re.compile(r"/title/.*/mediaviewer/|/media/"))


@pytest.mark.ui
@pytest.mark.imdb
def test_third_person_born_yesterday_screenshot(
    imdb: ImdbPages,
    browser_name: str,
    screenshots_dir: Path,
) -> None:
    screenshot_path = screenshots_dir / f"born_yesterday_third_person_{browser_name}.png"

    imdb.capture_third_person_born_yesterday(screenshot_path)

    assert screenshot_path.exists()


@pytest.mark.ui
@pytest.mark.imdb
def test_first_description_link_for_person_born_exactly_40_years_ago_screenshot(
    imdb: ImdbPages,
    browser_name: str,
    screenshots_dir: Path,
) -> None:
    screenshot_path = screenshots_dir / f"born_40_years_ago_first_description_link_{browser_name}.png"

    imdb.capture_first_description_link_for_person_born_40_years_ago(screenshot_path)

    assert screenshot_path.exists()
