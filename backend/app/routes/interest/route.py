from fastapi import APIRouter

from app.routes.interest.controller import InterestController
from app.routes.interest.dto import (
    InterestCalculationRequestDTO,
    InterestCalculationResponseDTO,
)


router = APIRouter(
    prefix="/api/v1/interest",
    tags=["Interest"],
)

controller = InterestController()


@router.post(
    "/calculate",
    response_model=InterestCalculationResponseDTO,
)
def calculate_interest(
    data: InterestCalculationRequestDTO,
) -> InterestCalculationResponseDTO:
    return controller.calculate_interest(data)