import { api } from "./api"
import type { Commission } from "../types/commission"

export async function getCommissions(): Promise<Commission[]> {
  const response = await api.get<Commission[]>("/commissions")

  return response.data
}