export type InterestCalculationRequest = {
  value: number
  due_date: string
}

export type InterestCalculationResponse = {
  original_value: number
  due_date: string
  calculation_date: string
  days_late: number
  daily_interest_rate: number
  interest: number
  total_value: number
}