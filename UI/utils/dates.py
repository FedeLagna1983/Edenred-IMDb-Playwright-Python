from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class BirthDateFilters:
    yesterday_month_day: str
    forty_years_ago: str


def get_birth_date_filters(today: date | None = None) -> BirthDateFilters:
    """Return IMDb-compatible date filters for the dynamic birthday scenarios."""
    current_date = today or date.today()
    yesterday = current_date - timedelta(days=1)
    forty_years_ago = _same_day_previous_year(current_date, years=40)

    return BirthDateFilters(
        yesterday_month_day=yesterday.strftime("%m-%d"),
        forty_years_ago=forty_years_ago.isoformat(),
    )


def _same_day_previous_year(value: date, years: int) -> date:
    try:
        return value.replace(year=value.year - years)
    except ValueError:
        return value.replace(year=value.year - years, day=28)

