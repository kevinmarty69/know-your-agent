import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import type { PlaygroundController } from "@/hooks/use-playground"

export function ConnectionHeader({ connection }: Pick<PlaygroundController, "connection">) {
  return (
    <header className="bg-grid rounded-xl border border-border/70 bg-card/60 p-6 backdrop-blur">
      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-semibold">Limiq.io API Playground</h1>
          <p className="text-sm text-muted-foreground">
            Internal test bench for backend flows. Uses live API responses and keeps the last 20
            requests.
          </p>
        </div>
        <Badge variant="secondary">internal tool</Badge>
      </div>

      <div className="mt-5 grid gap-3 md:grid-cols-2 lg:grid-cols-4">
        <div>
          <label className="mb-1 block text-xs font-medium text-muted-foreground">
            API Base URL
          </label>
          <Input
            value={connection.baseUrl}
            onChange={(event) => connection.setBaseUrl(event.target.value)}
          />
        </div>
        <div>
          <label className="mb-1 block text-xs font-medium text-muted-foreground">
            X-Workspace-Id
          </label>
          <Input
            value={connection.workspaceId}
            onChange={(event) => connection.setWorkspaceId(event.target.value)}
          />
        </div>
        <div>
          <label className="mb-1 block text-xs font-medium text-muted-foreground">
            X-Workspace-Key
          </label>
          <Input
            type="password"
            value={connection.workspaceKey}
            onChange={(event) => connection.setWorkspaceKey(event.target.value)}
          />
        </div>
        <div>
          <label className="mb-1 block text-xs font-medium text-muted-foreground">
            X-Bootstrap-Token
          </label>
          <Input
            type="password"
            placeholder="required for POST /workspaces"
            value={connection.bootstrapToken}
            onChange={(event) => connection.setBootstrapToken(event.target.value)}
          />
        </div>
      </div>
    </header>
  )
}

