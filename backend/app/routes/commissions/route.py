from fastapi import APIRouter

from app.routes.commissions.controller import CommissionController
from app.routes.commissions.dto import CommissionResultDTO


router = APIRouter(
    prefix="/api/v1/commissions",
    tags=["Commissions"],
)

controller = CommissionController()


@router.get(
    "",
    response_model=list[CommissionResultDTO],
)
def get_commissions() -> list[CommissionResultDTO]:
    return controller.calculate_commissions()