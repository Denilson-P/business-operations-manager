import { useEffect, useState } from "react"

import {
  createStockMovement,
  getInventory,
} from "../services/inventoryService"
import type {
  InventoryProduct,
  MovementType,
  StockMovementResponse,
} from "../types/inventory"


export function Inventory() {
  const [products, setProducts] = useState<InventoryProduct[]>([])
  const [productCode, setProductCode] = useState("")
  const [movementType, setMovementType] =
    useState<MovementType>("ENTRY")
  const [quantity, setQuantity] = useState("")
  const [description, setDescription] = useState("")

  const [lastMovement, setLastMovement] =
    useState<StockMovementResponse | null>(null)

  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function loadInventory() {
    try {
      const data = await getInventory()
      setProducts(data)
    } catch {
      setError("Unable to load inventory.")
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    loadInventory()
  }, [])

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    setError(null)
    setLastMovement(null)
    setIsSubmitting(true)

    try {
      const result = await createStockMovement({
        product_code: Number(productCode),
        movement_type: movementType,
        quantity: Number(quantity),
        description,
      })

      setLastMovement(result)

      setQuantity("")
      setDescription("")

      await loadInventory()
    } catch {
      setError("Unable to perform stock movement.")
    } finally {
      setIsSubmitting(false)
    }
  }

  if (isLoading) {
    return <p>Loading inventory...</p>
  }

  return (
    <main>
      <h1>Inventory</h1>

      {error && (
        <p className="error-message">
          {error}
        </p>
      )}

      <h2>Products</h2>

      <table>
        <thead>
          <tr>
            <th>Code</th>
            <th>Product</th>
            <th>Stock</th>
          </tr>
        </thead>

        <tbody>
          {products.map((product) => (
            <tr key={product.product_code}>
              <td>{product.product_code}</td>
              <td>{product.description}</td>
              <td>
                <span className="inventory-stock">
                  {product.stock}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>New Movement</h2>

      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="product">Product</label>

          <select
            id="product"
            value={productCode}
            onChange={(event) => setProductCode(event.target.value)}
            required
          >
            <option value="">Select a product</option>

            {products.map((product) => (
              <option
                key={product.product_code}
                value={product.product_code}
              >
                {product.description}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="movement-type">Movement</label>

          <select
            id="movement-type"
            value={movementType}
            onChange={(event) =>
              setMovementType(event.target.value as MovementType)
            }
          >
            <option value="ENTRY">Entry</option>
            <option value="EXIT">Exit</option>
          </select>
        </div>

        <div>
          <label htmlFor="quantity">Quantity</label>

          <input
            id="quantity"
            type="number"
            min="1"
            value={quantity}
            onChange={(event) => setQuantity(event.target.value)}
            required
          />
        </div>

        <div>
          <label htmlFor="description">Description</label>

          <input
            id="description"
            type="text"
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            required
          />
        </div>

        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Saving..." : "Perform Movement"}
        </button>
      </form>

            {lastMovement && (
        <section>
          <h2>Movement Performed</h2>

          <div className="result-grid">
            <div className="result-item">
              <span>Product</span>
              <strong>{lastMovement.product_description}</strong>
            </div>

            <div className="result-item">
              <span>Movement</span>
              <strong>
                {lastMovement.movement_type === "ENTRY"
                  ? "Entry"
                  : "Exit"}
              </strong>
            </div>

            <div className="result-item">
              <span>Previous Stock</span>
              <strong>{lastMovement.previous_stock}</strong>
            </div>

            <div className="result-item">
              <span>Current Stock</span>
              <strong>{lastMovement.current_stock}</strong>
            </div>
          </div>

          <p>
            ID da movimentação: {lastMovement.movement_id}
          </p>
        </section>
      )}
    </main>
  )
}