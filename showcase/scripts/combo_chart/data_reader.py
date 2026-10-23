import csv
from dataclasses import dataclass
from datetime import date

from tools.runtime import get_data_path

COMPANY_FILES = {
    "AAPL": "apple.csv",
    "NVDA": "nvidia.csv",
    "MSFT": "microsoft.csv",
    "AMZN": "amazon.csv",
    "TSLA": "tesla.csv",
}


@dataclass(frozen=True, slots=True)
class StockDataPoint:
    date: date
    close: float


@dataclass(frozen=True, slots=True)
class AnnualRevenue:
    fiscal_year: int
    period_end: date
    revenue: int


@dataclass(frozen=True, slots=True)
class ComboChartData:
    symbol: str
    monthly_prices: list[StockDataPoint]
    annual_revenue: list[AnnualRevenue]


def get_combo_chart_data(symbol: str) -> ComboChartData:
    """Read monthly stock prices and annual revenue from a local CSV file."""
    symbol = symbol.strip().upper()
    if symbol not in COMPANY_FILES:
        supported = ", ".join(COMPANY_FILES)
        raise ValueError(f"Unsupported symbol {symbol!r}. Choose one of: {supported}")

    monthly_prices: list[StockDataPoint] = []
    annual_revenue: list[AnnualRevenue] = []

    with get_data_path(COMPANY_FILES[symbol]).open(
        newline="",
        encoding="utf-8",
    ) as file:
        for row in csv.DictReader(file):
            row_date = date.fromisoformat(row["date"])

            if row["monthly_close"]:
                monthly_prices.append(
                    StockDataPoint(
                        date=row_date,
                        close=float(row["monthly_close"]),
                    )
                )

            if row["annual_revenue"]:
                annual_revenue.append(
                    AnnualRevenue(
                        fiscal_year=int(row["fiscal_year"]),
                        period_end=row_date,
                        revenue=int(row["annual_revenue"]),
                    )
                )

    return ComboChartData(
        symbol=symbol,
        monthly_prices=monthly_prices,
        annual_revenue=annual_revenue,
    )
