from datetime import date

import pytest
from pydantic import ValidationError

import app.routes.interest.service as interest_service_module
from app.routes.interest.dto import InterestCalculationRequestDTO
from app.routes.interest.service import InterestService


class FixedDate(date):
    @classmethod
    def today(cls) -> date:
        return cls(2026, 10, 7)


@pytest.fixture
def interest_service(monkeypatch) -> InterestService:
    monkeypatch.setattr(
        interest_service_module,
        "date",
        FixedDate,
    )

    return InterestService()


def test_calculates_interest_for_overdue_payment(
    interest_service: InterestService,
) -> None:
    data = InterestCalculationRequestDTO(
        value=100.00,
        due_date=date(2026, 10, 5),
    )

    result = interest_service.calculate(data)

    assert result.original_value == 100.00
    assert result.days_late == 2
    assert result.daily_interest_rate == 0.025
    assert result.interest == 5.00
    assert result.total_value == 105.00


def test_calculates_interest_for_multiple_days(
    interest_service: InterestService,
) -> None:
    data = InterestCalculationRequestDTO(
        value=200.00,
        due_date=date(2026, 10, 3),
    )

    result = interest_service.calculate(data)

    assert result.days_late == 4
    assert result.interest == 20.00
    assert result.total_value == 220.00


def test_due_today_has_no_interest(
    interest_service: InterestService,
) -> None:
    data = InterestCalculationRequestDTO(
        value=100.00,
        due_date=date(2026, 10, 7),
    )

    result = interest_service.calculate(data)

    assert result.days_late == 0
    assert result.interest == 0.00
    assert result.total_value == 100.00


def test_future_due_date_has_no_interest(
    interest_service: InterestService,
) -> None:
    data = InterestCalculationRequestDTO(
        value=100.00,
        due_date=date(2026, 10, 10),
    )

    result = interest_service.calculate(data)

    assert result.days_late == 0
    assert result.interest == 0.00
    assert result.total_value == 100.00


@pytest.mark.parametrize("value", [0, -1])
def test_value_must_be_greater_than_zero(value: float) -> None:
    with pytest.raises(ValidationError):
        InterestCalculationRequestDTO(
            value=value,
            due_date=date(2026, 10, 5),
        )