import { api } from "./api"
import type {
  InterestCalculationRequest,
  InterestCalculationResponse,
} from "../types/interest"

export async function calculateInterest(
  data: InterestCalculationRequest,
): Promise<InterestCalculationResponse> {
  const response = await api.post<InterestCalculationResponse>(
    "/interest/calculate",
    data,
  )

  return response.data
}