from app.routes.interest.dto import (
    InterestCalculationRequestDTO,
    InterestCalculationResponseDTO,
)
from app.routes.interest.service import InterestService


class InterestController:
    """Coordinate the API operation for calculating overdue payment interest.

    Passes a validated InterestCalculationRequestDTO to InterestService and
    returns its InterestCalculationResponseDTO. Exceptions propagate without
    HTTP-specific translation.

    Attributes:
        service: InterestService instance created during initialization."""

    def __init__(self) -> None:
        self.service = InterestService()

    def calculate_interest(
        self,
        data: InterestCalculationRequestDTO,
    ) -> InterestCalculationResponseDTO:
        return self.service.calculate(data)