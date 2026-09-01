import { ApiActions } from "@/components/playground/api-actions"
import { ConnectionHeader } from "@/components/playground/connection-header"
import { RequestResults } from "@/components/playground/request-results"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { usePlayground } from "@/hooks/use-playground"

function App() {
  const playground = usePlayground()

  return (
    <main className="min-h-screen p-4 md:p-8">
      <div className="mx-auto max-w-7xl space-y-6">
        <ConnectionHeader connection={playground.connection} />

        {playground.errorText ? (
          <Alert variant="destructive">
            <AlertTitle>Request Error</AlertTitle>
            <AlertDescription>{playground.errorText}</AlertDescription>
          </Alert>
        ) : null}

        <div className="grid gap-6 xl:grid-cols-[1.25fr_1fr]">
          <ApiActions controller={playground} />
          <RequestResults requests={playground.requests} />
        </div>
      </div>
    </main>
  )
}

export default App
