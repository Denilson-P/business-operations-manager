import { useEffect, useState } from "react"

import { getCommissions } from "../services/commissionService"
import type { Commission } from "../types/commission"
import { formatCurrency } from "../utils/formatCurrency"


export function Commissions() {
  const [commissions, setCommissions] = useState<Commission[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadCommissions() {
      try {
        const data = await getCommissions()

        setCommissions(data)
      } catch {
        setError("Unable to load commissions.")
      } finally {
        setIsLoading(false)
      }
    }

    loadCommissions()
  }, [])

  if (isLoading) {
    return <p>Loading commissions...</p>
  }

  if (error) {
    return <p>{error}</p>
  }

  return (
    <main>
      <h1>Commissions</h1>

      <table>
        <thead>
          <tr>
            <th>Seller</th>
            <th>Total Sales</th>
            <th>Commission</th>
          </tr>
        </thead>

        <tbody>
          {commissions.map((commission) => (
            <tr key={commission.seller}>
              <td>{commission.seller}</td>
              <td>{formatCurrency(commission.total_sales)}</td>
              <td>{formatCurrency(commission.total_commission)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  )
}