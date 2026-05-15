from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright


SUPPORTED_BROWSERS = ("chromium", "firefox")
UI_ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS_DIR = UI_ROOT / "screenshots"


def before_all(context):
    context.playwright = sync_playwright().start()
    context.browser_name = context.config.userdata.get("browser", "chromium")
    if context.browser_name not in SUPPORTED_BROWSERS:
        supported = ", ".join(SUPPORTED_BROWSERS)
        raise ValueError(f"Unsupported browser '{context.browser_name}'. Use one of: {supported}.")
    context.headed = context.config.userdata.getbool("headed", False)
    SCREENSHOTS_DIR.mkdir(exist_ok=True)
    context.screenshots_dir = SCREENSHOTS_DIR


def before_scenario(context, scenario):
    browser_launcher = getattr(context.playwright, context.browser_name)
    context.browser = browser_launcher.launch(
        headless=not context.headed,
        slow_mo=100 if context.headed else 0,
    )
    context.browser_context = context.browser.new_context(
        locale="en-US",
        timezone_id="America/Santiago",
        user_agent=_user_agent_for(context.browser_name),
        extra_http_headers={"Accept-Language": "en-US,en;q=0.9"},
        viewport={"width": 1440, "height": 1000},
    )
    context.page = context.browser_context.new_page()
    context.page.set_default_timeout(15_000)


def after_scenario(context, scenario):
    if hasattr(context, "browser_context"):
        context.browser_context.close()
    if hasattr(context, "browser"):
        context.browser.close()


def after_all(context):
    context.playwright.stop()


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

