import { useState } from "react"

import { formatDate } from "../utils/formatDate"
import { formatCurrency } from "../utils/formatCurrency"
import { calculateInterest } from "../services/interestService"
import type { InterestCalculationResponse } from "../types/interest"


export function Interest() {
  const [value, setValue] = useState("")
  const [dueDate, setDueDate] = useState("")
  const [result, setResult] =
    useState<InterestCalculationResponse | null>(null)

  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    setError(null)
    setResult(null)
    setIsSubmitting(true)

    try {
      const data = await calculateInterest({
        value: Number(value),
        due_date: dueDate,
      })

      setResult(data)
    } catch {
      setError("Unable to calculate interest.")
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <main>
      <h1>Interest Calculation</h1>

      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="value">Value</label>

          <input
            id="value"
            type="number"
            min="0.01"
            step="0.01"
            value={value}
            onChange={(event) => setValue(event.target.value)}
            required
          />
        </div>

        <div>
          <label htmlFor="due-date">Due Date</label>

          <input
            id="due-date"
            type="date"
            value={dueDate}
            onChange={(event) => setDueDate(event.target.value)}
            required
          />
        </div>

        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Calculating..." : "Calculate Interest"}
        </button>
      </form>

      {error && <p>{error}</p>}

      {result && (
        <section>
          <h2>Calculation Result</h2>

          <div className="result-grid">
            <div className="result-item">
              <span>Original Value</span>
              <strong>{formatCurrency(result.original_value)}</strong>
            </div>

            <div className="result-item">
              <span>Days Late</span>
              <strong>{result.days_late}</strong>
            </div>

            <div className="result-item">
              <span>Due Date</span>
              <strong>{formatDate(result.due_date)}</strong>
            </div>

            <div className="result-item">
              <span>Calculation Date</span>
              <strong>{formatDate(result.calculation_date)}</strong>
            </div>

            <div className="result-item">
              <span>Daily Rate</span>
              <strong>
                {(result.daily_interest_rate * 100).toFixed(1)}%
              </strong>
            </div>

            <div className="result-item">
              <span>Interest</span>
              <strong>{formatCurrency(result.interest)}</strong>
            </div>

            <div className="result-item">
              <span>Total Value</span>
              <strong>{formatCurrency(result.total_value)}</strong>
            </div>
          </div>
        </section>
      )}
    </main>
  )
}