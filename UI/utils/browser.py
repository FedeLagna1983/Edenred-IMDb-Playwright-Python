from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Final

SUPPORTED_BROWSERS: Final[tuple[str, ...]] = ("chromium", "firefox")
DEFAULT_TIMEOUT_MS: Final[int] = 15_000
DEFAULT_VIEWPORT: Final[dict[str, int]] = {"width": 1440, "height": 1000}
DEFAULT_LOCALE: Final[str] = "en-US"
DEFAULT_TIMEZONE: Final[str] = "America/Santiago"
ACCEPT_LANGUAGE: Final[str] = "en-US,en;q=0.9"


@dataclass(frozen=True)
class BrowserSettings:
    browser_name: str
    headed: bool = False
    slow_mo_ms: int = 100
    default_timeout_ms: int = DEFAULT_TIMEOUT_MS

    @property
    def launch_options(self) -> dict[str, object]:
        return {
            "headless": not self.headed,
            "slow_mo": self.slow_mo_ms if self.headed else 0,
        }

    @property
    def context_options(self) -> dict[str, object]:
        return {
            "locale": DEFAULT_LOCALE,
            "timezone_id": DEFAULT_TIMEZONE,
            "user_agent": user_agent_for(self.browser_name),
            "extra_http_headers": {"Accept-Language": ACCEPT_LANGUAGE},
            "viewport": DEFAULT_VIEWPORT,
        }


def user_agent_for(browser_name: str) -> str:
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


def headed_from_cli_or_env(*, forced_headed: bool, forced_headless: bool) -> bool:
    if forced_headless:
        return False
    if forced_headed:
        return True
    return os.getenv("HEADLESS", "false").lower() not in {"1", "true", "yes"}


def validate_browser_name(browser_name: str) -> None:
    if browser_name not in SUPPORTED_BROWSERS:
        supported = ", ".join(SUPPORTED_BROWSERS)
        raise ValueError(f"Unsupported browser '{browser_name}'. Use one of: {supported}.")
