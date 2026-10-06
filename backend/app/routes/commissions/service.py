import json
from pathlib import Path

from app.routes.commissions.dto import CommissionResultDTO


class CommissionService:
    """Calculate commissions per sale and aggregate results by seller.

    Sales below 100 earn no commission; sales from 100 up to but excluding
    500 earn 1%; sales of 500 or more earn 5%. The rate applies to each sale's
    full value, rather than marginal portions or accumulated seller totals.

    Reads records under the vendas key of the source JSON file, using vendedor
    and valor as the seller and sale value. Results follow the order in which
    sellers first appear. Sales and commission totals are rounded to two
    decimal places after aggregation. The source file is never modified.
    File access, JSON parsing, and malformed record errors propagate.

    Attributes:
        SALES_FILE: Path to app/data/sales.json. Override it to select another
            source file."""

    SALES_FILE = Path(__file__).resolve().parents[2] / "data" / "sales.json"

    @staticmethod
    def calculate_commission(value: float) -> float:
        if value < 100:
            return 0.0

        if value < 500:
            return value * 0.01

        return value * 0.05

    def calculate_all(self) -> list[CommissionResultDTO]:
        with self.SALES_FILE.open(
            mode="r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        sellers: dict[str, dict[str, float]] = {}

        for sale in data["vendas"]:
            seller = sale["vendedor"]
            value = sale["valor"]

            if seller not in sellers:
                sellers[seller] = {
                    "total_sales": 0.0,
                    "total_commission": 0.0,
                }

            sellers[seller]["total_sales"] += value
            sellers[seller]["total_commission"] += (
                self.calculate_commission(value)
            )

        return [
            CommissionResultDTO(
                seller=seller,
                total_sales=round(values["total_sales"], 2),
                total_commission=round(
                    values["total_commission"],
                    2,
                ),
            )
            for seller, values in sellers.items()
        ]