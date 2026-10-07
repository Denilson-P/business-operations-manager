export function formatDate(value: string): string {
  const [year, month, day] = value.split("-")

  return `${day}/${month}/${year}`
}