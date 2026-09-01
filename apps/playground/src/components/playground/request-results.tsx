import { Badge } from "@/components/ui/badge"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import type { PlaygroundController } from "@/hooks/use-playground"
import { prettyJson } from "@/lib/json"

export function RequestResults({ requests }: Pick<PlaygroundController, "requests">) {
  return (
    <div className="space-y-6">
      <Card className="border-border/70 bg-card/80">
        <CardHeader>
          <CardTitle>Latest Response</CardTitle>
          <CardDescription>
            Status, duration, and parsed payload from the selected request.
          </CardDescription>
        </CardHeader>
        <CardContent>
          {requests.selectedRequest ? (
            <div className="space-y-3">
              <div className="flex flex-wrap items-center gap-2">
                <Badge variant={requests.selectedRequest.ok ? "secondary" : "destructive"}>
                  {requests.selectedRequest.status}
                </Badge>
                <Badge variant="outline">{requests.selectedRequest.durationMs}ms</Badge>
                <span className="text-xs text-muted-foreground">
                  {requests.selectedRequest.method}
                </span>
                <span className="truncate text-xs text-muted-foreground">
                  {requests.selectedRequest.url}
                </span>
              </div>
              <pre className="max-h-[360px] overflow-auto rounded-md bg-muted p-3 text-xs">
                {prettyJson(requests.selectedRequest.responseBody)}
              </pre>
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">No request sent yet.</p>
          )}
        </CardContent>
      </Card>

      <Card className="border-border/70 bg-card/80">
        <CardHeader>
          <CardTitle>Recent Requests</CardTitle>
          <CardDescription>Click a row to inspect its response payload.</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Action</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Duration</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {requests.history.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={3} className="text-muted-foreground">
                    No requests yet.
                  </TableCell>
                </TableRow>
              ) : (
                requests.history.map((item) => (
                  <TableRow
                    key={item.id}
                    className="cursor-pointer"
                    onClick={() => requests.setSelectedRequestId(item.id)}
                  >
                    <TableCell>{item.title}</TableCell>
                    <TableCell>
                      <Badge variant={item.ok ? "secondary" : "destructive"}>
                        {item.status}
                      </Badge>
                    </TableCell>
                    <TableCell>{item.durationMs}ms</TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}

