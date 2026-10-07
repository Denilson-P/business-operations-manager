from fastapi import APIRouter, status

from app.routes.inventory.controller import InventoryController
from app.routes.inventory.dto import (
    InventoryProductDTO,
    StockMovementRequestDTO,
    StockMovementResponseDTO,
)


router = APIRouter(
    prefix="/api/v1/inventory",
    tags=["Inventory"],
)

controller = InventoryController()


@router.get(
    "",
    response_model=list[InventoryProductDTO],
)
def get_inventory() -> list[InventoryProductDTO]:
    return controller.get_inventory()


@router.post(
    "/movements",
    response_model=StockMovementResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
def create_movement(
    movement: StockMovementRequestDTO,
) -> StockMovementResponseDTO:
    return controller.create_movement(movement)