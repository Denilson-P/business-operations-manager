from datetime import date

from pydantic import BaseModel, Field


class InterestCalculationRequestDTO(BaseModel):
    """Validate the amount and due date used to calculate overdue interest.

    Attributes:
        value: Original monetary amount; must be greater than zero.
        due_date: Payment due date. Dates on or after the calculation date are
            accepted and produce no overdue interest."""

    value: float = Field(gt=0)
    due_date: date


class InterestCalculationResponseDTO(BaseModel):
    """Describe an overdue-interest calculation and the resulting balance.

    Attributes:
        original_value: Original monetary amount supplied in the request.
        due_date: Payment due date supplied in the request.
        calculation_date: Local current date used by the service.
        days_late: Elapsed days since the due date, with a minimum of zero.
        daily_interest_rate: Daily fractional rate; 0.025 means 2.5% per day.
        interest: Simple interest rounded to two decimal places.
        total_value: Original amount plus unrounded interest, then rounded
            to two decimal places."""

    original_value: float
    due_date: date
    calculation_date: date
    days_late: int
    daily_interest_rate: float
    interest: float
    total_value: float