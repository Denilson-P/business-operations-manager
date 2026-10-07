from fastapi import HTTPException, status

from app.routes.inventory.dto import (
    InventoryProductDTO,
    StockMovementRequestDTO,
    StockMovementResponseDTO,
)
from app.routes.inventory.service import (
    InsufficientStockError,
    InventoryService,
    ProductNotFoundError,
)


class InventoryController:
    """Coordinate inventory API operations and translate business errors.

    Delegates inventory reads and stock movements to InventoryService. Missing
    products become HTTP 404 errors; exits exceeding available stock become
    HTTP 409 errors. Other service exceptions propagate to the caller.

    Attributes:
        service: InventoryService instance created during initialization."""

    def __init__(self) -> None:
        self.service = InventoryService()

    def get_inventory(self) -> list[InventoryProductDTO]:
        return self.service.get_inventory()

    def create_movement(
        self,
        movement: StockMovementRequestDTO,
    ) -> StockMovementResponseDTO:
        try:
            return self.service.create_movement(movement)

        except ProductNotFoundError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(error),
            ) from error

        except InsufficientStockError as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(error),
            ) from error