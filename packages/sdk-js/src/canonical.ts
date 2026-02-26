function sortJsonValue(value: unknown): unknown {
  if (Array.isArray(value)) {
    return value.map((item) => sortJsonValue(item))
  }

  if (value !== null && typeof value === "object") {
    const entries = Object.entries(value as Record<string, unknown>).sort(([a], [b]) => {
      if (a < b) {
        return -1
      }
      if (a > b) {
        return 1
      }
      return 0
    })
    const out: Record<string, unknown> = {}
    for (const [key, item] of entries) {
      out[key] = sortJsonValue(item)
    }
    return out
  }

  return value
}

export function canonicalize(payload: Record<string, unknown>): string {
  return JSON.stringify(sortJsonValue(payload))
}
