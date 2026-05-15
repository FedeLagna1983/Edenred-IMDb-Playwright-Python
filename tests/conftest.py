from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright


ROOT_DIR = Path(__file__).resolve().parents[1]
SCREENSHOTS_DIR = ROOT_DIR / "screenshots"
SUPPORTED_BROWSERS = ("chromium", "firefox")


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--browser",
        action="append",
        choices=SUPPORTED_BROWSERS,
        help="Browser to run UI tests against. May be passed more than once.",
    )
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run browsers with a visible window. This is the local default unless HEADLESS is true.",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browsers without a visible window.",
    )


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    if "browser_name" in metafunc.fixturenames:
        selected = metafunc.config.getoption("--browser") or list(SUPPORTED_BROWSERS)
        metafunc.parametrize("browser_name", selected)


@pytest.fixture(scope="session")
def screenshots_dir() -> Path:
    SCREENSHOTS_DIR.mkdir(exist_ok=True)
    return SCREENSHOTS_DIR


@pytest.fixture(scope="session")
def imdb_credentials() -> tuple[str, str]:
    email = os.getenv("IMDB_EMAIL")
    password = os.getenv("IMDB_PASSWORD")
    if not email or not password:
        pytest.skip("IMDB_EMAIL and IMDB_PASSWORD are required for this test.")
    return email, password


@pytest.fixture()
def page(request: pytest.FixtureRequest, browser_name: str) -> Iterator[Page]:
    headless_from_env = os.getenv("HEADLESS", "false").lower() in {"1", "true", "yes"}
    if request.config.getoption("--headless"):
        headed = False
    elif request.config.getoption("--headed"):
        headed = True
    else:
        headed = not headless_from_env

    with sync_playwright() as playwright:
        browser_launcher = getattr(playwright, browser_name)
        browser: Browser = browser_launcher.launch(headless=not headed, slow_mo=100 if headed else 0)
        context: BrowserContext = browser.new_context(
            locale="en-US",
            timezone_id="America/Santiago",
            user_agent=_user_agent_for(browser_name),
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9"},
            viewport={"width": 1440, "height": 1000},
        )
        page = context.new_page()
        page.set_default_timeout(15_000)
        yield page
        context.close()
        browser.close()


def _user_agent_for(browser_name: str) -> str:
    if browser_name == "firefox":
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) "
            "Gecko/20100101 Firefox/148.0"
        )
    return (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/147.0.0.0 Safari/537.36"
    )

