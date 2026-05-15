from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from pages import ImdbPages
from utils.browser import BrowserSettings, SUPPORTED_BROWSERS, headed_from_cli_or_env


ROOT_DIR = Path(__file__).resolve().parents[1]
SCREENSHOTS_DIR = ROOT_DIR / "screenshots"


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
        help="Run browsers with a visible window.",
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
        metafunc.parametrize("browser_name", selected, ids=selected)


@pytest.fixture(scope="session")
def screenshots_dir() -> Path:
    SCREENSHOTS_DIR.mkdir(exist_ok=True)
    return SCREENSHOTS_DIR


@pytest.fixture(scope="session")
def playwright_instance() -> Iterator[Playwright]:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def imdb_credentials() -> tuple[str, str]:
    email = os.getenv("IMDB_EMAIL")
    password = os.getenv("IMDB_PASSWORD")
    if not email or not password:
        pytest.skip("IMDB_EMAIL and IMDB_PASSWORD are required for this test.")
    return email, password


@pytest.fixture()
def browser_settings(request: pytest.FixtureRequest, browser_name: str) -> BrowserSettings:
    return BrowserSettings(
        browser_name=browser_name,
        headed=headed_from_cli_or_env(
            forced_headed=request.config.getoption("--headed"),
            forced_headless=request.config.getoption("--headless"),
        ),
    )


@pytest.fixture()
def browser(playwright_instance: Playwright, browser_settings: BrowserSettings) -> Iterator[Browser]:
    launcher = getattr(playwright_instance, browser_settings.browser_name)
    browser = launcher.launch(**browser_settings.launch_options)
    yield browser
    browser.close()


@pytest.fixture()
def browser_context(browser: Browser, browser_settings: BrowserSettings) -> Iterator[BrowserContext]:
    context = browser.new_context(**browser_settings.context_options)
    yield context
    context.close()


@pytest.fixture()
def page(browser_context: BrowserContext, browser_settings: BrowserSettings) -> Iterator[Page]:
    page = browser_context.new_page()
    page.set_default_timeout(browser_settings.default_timeout_ms)
    yield page


@pytest.fixture()
def imdb(page: Page) -> ImdbPages:
    return ImdbPages.create(page)
