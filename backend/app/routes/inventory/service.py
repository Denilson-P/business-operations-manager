import json
from pathlib import Path
from uuid import uuid4

from app.routes.inventory.dto import (
    InventoryProductDTO,
    MovementType,
    StockMovementRequestDTO,
    StockMovementResponseDTO,
)


class ProductNotFoundError(Exception):
    """Signal that a stock movement targets a product absent from inventory.

    Raised before the inventory is saved. Its message identifies the missing
    product code, and the controller translates it into an HTTP 404 error."""

    pass


class InsufficientStockError(Exception):
    """Signal that an outgoing movement exceeds a product's available stock.

    Raised before saving, so the stored balance remains unchanged. Its message
    includes available and requested quantities. The controller translates
    this exception into an HTTP 409 error."""

    pass


class InventoryService:
    """Read inventory balances and persist stock entries and exits in JSON.

    Each operation loads records under the estoque key, using codigoProduto,
    descricaoProduto, and estoque as the product code, description, and stock.
    Entries increase stock; exits decrease it only if enough units exist.
    Missing products and insufficient stock raise dedicated exceptions before
    any save occurs.

    Successful movements rewrite the file and return the old and new balances
    with a generated UUID. Movement descriptions and UUIDs are not persisted,
    and no movement history is maintained. File operations have no locking,
    so concurrent updates can overwrite one another. File access, JSON parsing,
    and malformed record errors propagate to the caller.

    Attributes:
        INVENTORY_FILE: Path to app/data/inventory.json, used for reads and
            writes. Override it to select another inventory file."""

    INVENTORY_FILE = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "inventory.json"
    )

    def get_inventory(self) -> list[InventoryProductDTO]:
        data = self._load_inventory()

        return [
            InventoryProductDTO(
                product_code=product["codigoProduto"],
                description=product["descricaoProduto"],
                stock=product["estoque"],
            )
            for product in data["estoque"]
        ]

    def create_movement(
        self,
        movement: StockMovementRequestDTO,
    ) -> StockMovementResponseDTO:
        data = self._load_inventory()

        product = self._find_product(
            data=data,
            product_code=movement.product_code,
        )

        previous_stock = product["estoque"]

        if movement.movement_type == MovementType.ENTRY:
            current_stock = previous_stock + movement.quantity

        else:
            if movement.quantity > previous_stock:
                raise InsufficientStockError(
                    f"Estoque insuficiente. "
                    f"Disponível: {previous_stock}, "
                    f"solicitado: {movement.quantity}."
                )

            current_stock = previous_stock - movement.quantity

        product["estoque"] = current_stock

        self._save_inventory(data)

        return StockMovementResponseDTO(
            movement_id=uuid4(),
            product_code=product["codigoProduto"],
            product_description=product["descricaoProduto"],
            movement_type=movement.movement_type,
            quantity=movement.quantity,
            previous_stock=previous_stock,
            current_stock=current_stock,
        )

    def _find_product(
        self,
        data: dict,
        product_code: int,
    ) -> dict:
        for product in data["estoque"]:
            if product["codigoProduto"] == product_code:
                return product

        raise ProductNotFoundError(
            f"Product with code {product_code} not found."
        )

    def _load_inventory(self) -> dict:
        with self.INVENTORY_FILE.open(
            mode="r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def _save_inventory(self, data: dict) -> None:
        with self.INVENTORY_FILE.open(
            mode="w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2,
            )