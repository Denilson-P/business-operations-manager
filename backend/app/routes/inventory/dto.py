from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class MovementType(str, Enum):
    """Define the supported directions of an inventory movement.

    Attributes:
        ENTRY: Add the requested quantity to the product's stock.
        EXIT: Remove units, subject to the available stock balance.

    Enum string values are used in API request and response payloads."""

    ENTRY = "ENTRY"
    EXIT = "EXIT"


class StockMovementRequestDTO(BaseModel):
    """Validate the input for a stock change on an existing product.

    Attributes:
        product_code: Identifier of the product whose stock will be changed.
        movement_type: Direction of the movement: ENTRY or EXIT.
        quantity: Number of units to add or remove; must be greater than zero.
        description: Nonempty explanation of the movement. The current service
            does not persist this text or include it in the response.

    Product existence and stock availability are checked by the service after
    Pydantic validates the request fields."""

    product_code: int
    movement_type: MovementType
    quantity: int = Field(gt=0)
    description: str = Field(min_length=1)


class StockMovementResponseDTO(BaseModel):
    """Describe the result of a successfully persisted stock movement.

    Attributes:
        movement_id: UUID generated for this response. It is not persisted.
        product_code: Identifier of the updated product.
        product_description: Description from the stored product record.
        movement_type: Direction of the completed movement.
        quantity: Number of units added or removed.
        previous_stock: Balance before the movement.
        current_stock: Balance after the movement."""

    movement_id: UUID
    product_code: int
    product_description: str
    movement_type: MovementType
    quantity: int
    previous_stock: int
    current_stock: int


class InventoryProductDTO(BaseModel):
    """Expose a stored product and its current inventory balance.

    Attributes:
        product_code: Product identifier mapped from codigoProduto in storage.
        description: Product description mapped from descricaoProduto.
        stock: Available quantity mapped from the product's estoque field."""

    product_code: int
    description: str
    stock: int