import json

import pytest
from pydantic import ValidationError

from app.routes.inventory.dto import MovementType, StockMovementRequestDTO
from app.routes.inventory.service import (
    InsufficientStockError,
    InventoryService,
    ProductNotFoundError,
)


@pytest.fixture
def inventory_service(tmp_path) -> InventoryService:
    inventory_file = tmp_path / "inventory.json"

    inventory_file.write_text(
        json.dumps(
            {
                "estoque": [
                    {
                        "codigoProduto": 101,
                        "descricaoProduto": "Blue Pen",
                        "estoque": 150,
                    },
                    {
                        "codigoProduto": 102,
                        "descricaoProduto": "Notebook",
                        "estoque": 75,
                    },
                ]
            }
        ),
        encoding="utf-8",
    )

    service = InventoryService()
    service.INVENTORY_FILE = inventory_file

    return service


def test_get_inventory(inventory_service: InventoryService) -> None:
    inventory = inventory_service.get_inventory()

    assert len(inventory) == 2
    assert inventory[0].product_code == 101
    assert inventory[0].description == "Blue Pen"
    assert inventory[0].stock == 150


def test_entry_increases_stock(inventory_service: InventoryService) -> None:
    movement = StockMovementRequestDTO(
        product_code=101,
        movement_type=MovementType.ENTRY,
        quantity=50,
        description="Stock replenishment",
    )

    result = inventory_service.create_movement(movement)

    assert result.previous_stock == 150
    assert result.current_stock == 200
    assert result.quantity == 50
    assert result.movement_type == MovementType.ENTRY


def test_exit_decreases_stock(inventory_service: InventoryService) -> None:
    movement = StockMovementRequestDTO(
        product_code=101,
        movement_type=MovementType.EXIT,
        quantity=50,
        description="Stock removal",
    )

    result = inventory_service.create_movement(movement)

    assert result.previous_stock == 150
    assert result.current_stock == 100
    assert result.quantity == 50
    assert result.movement_type == MovementType.EXIT


def test_movement_persists_updated_stock(
    inventory_service: InventoryService,
) -> None:
    movement = StockMovementRequestDTO(
        product_code=101,
        movement_type=MovementType.ENTRY,
        quantity=25,
        description="Stock replenishment",
    )

    inventory_service.create_movement(movement)

    inventory = inventory_service.get_inventory()
    product = next(
        item for item in inventory if item.product_code == 101
    )

    assert product.stock == 175


def test_product_not_found(inventory_service: InventoryService) -> None:
    movement = StockMovementRequestDTO(
        product_code=999,
        movement_type=MovementType.ENTRY,
        quantity=10,
        description="Stock replenishment",
    )

    with pytest.raises(ProductNotFoundError):
        inventory_service.create_movement(movement)


def test_insufficient_stock(inventory_service: InventoryService) -> None:
    movement = StockMovementRequestDTO(
        product_code=102,
        movement_type=MovementType.EXIT,
        quantity=100,
        description="Stock removal",
    )

    with pytest.raises(InsufficientStockError):
        inventory_service.create_movement(movement)


@pytest.mark.parametrize("quantity", [0, -1])
def test_quantity_must_be_greater_than_zero(quantity: int) -> None:
    with pytest.raises(ValidationError):
        StockMovementRequestDTO(
            product_code=101,
            movement_type=MovementType.ENTRY,
            quantity=quantity,
            description="Stock replenishment",
        )


def test_description_must_not_be_empty() -> None:
    with pytest.raises(ValidationError):
        StockMovementRequestDTO(
            product_code=101,
            movement_type=MovementType.ENTRY,
            quantity=10,
            description="",
        )