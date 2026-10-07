from datetime import date

from app.routes.interest.dto import (
    InterestCalculationRequestDTO,
    InterestCalculationResponseDTO,
)


class InterestService:
    """Calculate simple daily interest on an overdue monetary amount.

    Uses the local current date from date.today() to count days elapsed since
    the due date. Payments due today or in the future have zero days late and
    accrue no interest. Overdue interest equals the original amount multiplied
    by the daily rate and days late, without compounding.

    Returns the original amount and dates, elapsed days, and applied rate.
    Interest and total value are rounded independently to two decimal places.
    Calculations use floating-point arithmetic and perform no file operations.

    Attributes:
        DAILY_INTEREST_RATE: Daily fractional rate of 0.025, corresponding
            to 2.5% of the original amount per overdue day."""

    DAILY_INTEREST_RATE = 0.025

    def calculate(
        self,
        data: InterestCalculationRequestDTO,
    ) -> InterestCalculationResponseDTO:
        calculation_date = date.today()

        days_late = (calculation_date - data.due_date).days
        days_late = max(days_late, 0)

        interest = (
            data.value
            * self.DAILY_INTEREST_RATE
            * days_late
        )

        total_value = data.value + interest

        return InterestCalculationResponseDTO(
            original_value=data.value,
            due_date=data.due_date,
            calculation_date=calculation_date,
            days_late=days_late,
            daily_interest_rate=self.DAILY_INTEREST_RATE,
            interest=round(interest, 2),
            total_value=round(total_value, 2),
        )