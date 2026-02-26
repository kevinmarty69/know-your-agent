export type PlaygroundHttpMethod = "GET" | "POST"

export type PlaygroundRequest = {
  id: string
  title: string
  method: PlaygroundHttpMethod
  url: string
  startedAt: string
  durationMs: number
  status: number
  ok: boolean
  requestBody?: unknown
  responseBody: unknown
}

export type ApiCallInput = {
  title: string
  baseUrl: string
  workspaceId: string
  bootstrapToken?: string
  method: PlaygroundHttpMethod
  path: string
  body?: unknown
}

export type ApiCallResult = {
  request: PlaygroundRequest
  rawText: string
}
