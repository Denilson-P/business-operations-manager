export type MovementType = "ENTRY" | "EXIT"

export type InventoryProduct = {
  product_code: number
  description: string
  stock: number
}

export type StockMovementRequest = {
  product_code: number
  movement_type: MovementType
  quantity: number
  description: string
}

export type StockMovementResponse = {
  movement_id: string
  product_code: number
  product_description: string
  movement_type: MovementType
  quantity: number
  previous_stock: number
  current_stock: number
}