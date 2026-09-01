export function parseJsonInput(value: string): unknown {
  if (!value.trim()) {
    return {}
  }

  return JSON.parse(value) as unknown
}

export function prettyJson(value: unknown): string {
  return JSON.stringify(value, null, 2)
}

