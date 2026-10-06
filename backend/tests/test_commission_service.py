import json

import pytest

from app.routes.commissions.service import CommissionService


@pytest.mark.parametrize(
    ("sale_value", "expected_commission"),
    [
        (99.99, 0.0),
        (100.00, 1.0),
        (499.99, 4.9999),
        (500.00, 25.0),
    ],
)
def test_calculate_commission(
    sale_value: float,
    expected_commission: float,
) -> None:
    result = CommissionService.calculate_commission(sale_value)

    assert result == pytest.approx(expected_commission)


def test_calculate_all_commissions(tmp_path) -> None:
    sales_file = tmp_path / "sales.json"

    sales_data = {
        "vendas": [
            {"vendedor": "Seller One", "valor": 50.0},
            {"vendedor": "Seller One", "valor": 200.0},
            {"vendedor": "Seller Two", "valor": 500.0},
        ]
    }

    sales_file.write_text(
        json.dumps(sales_data),
        encoding="utf-8",
    )

    service = CommissionService()
    service.SALES_FILE = sales_file

    result = service.calculate_all()

    assert len(result) == 2

    assert result[0].seller == "Seller One"
    assert result[0].total_sales == 250.0
    assert result[0].total_commission == 2.0

    assert result[1].seller == "Seller Two"
    assert result[1].total_sales == 500.0
    assert result[1].total_commission == 25.0