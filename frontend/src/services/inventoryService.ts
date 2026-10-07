import { api } from "./api"
import type {
  InventoryProduct,
  StockMovementRequest,
  StockMovementResponse,
} from "../types/inventory"

export async function getInventory(): Promise<InventoryProduct[]> {
  const response = await api.get<InventoryProduct[]>("/inventory")

  return response.data
}

export async function createStockMovement(
  movement: StockMovementRequest,
): Promise<StockMovementResponse> {
  const response = await api.post<StockMovementResponse>(
    "/inventory/movements",
    movement,
  )

  return response.data
}