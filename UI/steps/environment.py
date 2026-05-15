from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright

from pages import ImdbPages
from utils.browser import BrowserSettings, validate_browser_name


UI_ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS_DIR = UI_ROOT / "screenshots"


def before_all(context):
    context.playwright = sync_playwright().start()
    context.browser_name = context.config.userdata.get("browser", "chromium")
    validate_browser_name(context.browser_name)
    context.browser_settings = BrowserSettings(
        browser_name=context.browser_name,
        headed=context.config.userdata.getbool("headed", False),
    )
    SCREENSHOTS_DIR.mkdir(exist_ok=True)
    context.screenshots_dir = SCREENSHOTS_DIR


def before_scenario(context, scenario):
    browser_launcher = getattr(context.playwright, context.browser_name)
    context.browser = browser_launcher.launch(**context.browser_settings.launch_options)
    context.browser_context = context.browser.new_context(**context.browser_settings.context_options)
    context.page = context.browser_context.new_page()
    context.page.set_default_timeout(context.browser_settings.default_timeout_ms)
    context.imdb = ImdbPages.create(context.page)


def after_scenario(context, scenario):
    if hasattr(context, "browser_context"):
        context.browser_context.close()
    if hasattr(context, "browser"):
        context.browser.close()


def after_all(context):
    if hasattr(context, "playwright"):
        context.playwright.stop()
