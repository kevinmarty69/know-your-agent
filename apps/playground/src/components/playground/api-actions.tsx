import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Textarea } from "@/components/ui/textarea"
import type { PlaygroundController } from "@/hooks/use-playground"

type Controller = PlaygroundController

function WorkspaceActions({
  workspace,
  actions,
}: Pick<Controller, "workspace" | "actions">) {
  return (
    <TabsContent value="workspace" className="space-y-4 pt-4">
      <div className="grid gap-3 md:grid-cols-2">
        <Input
          placeholder="workspace name"
          value={workspace.name}
          onChange={(event) => workspace.setName(event.target.value)}
        />
        <Input
          placeholder="workspace slug (optional)"
          value={workspace.slug}
          onChange={(event) => workspace.setSlug(event.target.value)}
        />
      </div>
      <div className="flex flex-wrap gap-2">
        <Button onClick={actions.createWorkspace}>Create Workspace</Button>
        <Button
          variant="secondary"
          disabled={!workspace.lookupId}
          onClick={actions.getWorkspace}
        >
          Get Workspace
        </Button>
      </div>
      <Input
        placeholder="workspace id"
        value={workspace.lookupId}
        onChange={(event) => workspace.setLookupId(event.target.value)}
      />
    </TabsContent>
  )
}

function AgentActions({ agent, actions }: Pick<Controller, "agent" | "actions">) {
  return (
    <TabsContent value="agents" className="space-y-4 pt-4">
      <div className="grid gap-3 md:grid-cols-2">
        <Input
          placeholder="agent name"
          value={agent.name}
          onChange={(event) => agent.setName(event.target.value)}
        />
        <Input
          placeholder="base64 public key"
          value={agent.publicKey}
          onChange={(event) => agent.setPublicKey(event.target.value)}
        />
      </div>
      <div className="flex flex-wrap gap-2">
        <Button onClick={actions.createAgent}>Create Agent</Button>
        <Button variant="secondary" disabled={!agent.id} onClick={actions.getAgent}>
          Get Agent
        </Button>
        <Button variant="destructive" disabled={!agent.id} onClick={actions.revokeAgent}>
          Revoke Agent
        </Button>
      </div>
      <Input
        placeholder="agent id"
        value={agent.id}
        onChange={(event) => agent.setId(event.target.value)}
      />
    </TabsContent>
  )
}

function PolicyActions({
  agent,
  policy,
  actions,
}: Pick<Controller, "agent" | "policy" | "actions">) {
  return (
    <TabsContent value="policy" className="space-y-4 pt-4">
      <div className="grid gap-3 md:grid-cols-2">
        <Input
          placeholder="policy name"
          value={policy.name}
          onChange={(event) => policy.setName(event.target.value)}
        />
        <Input
          placeholder="version"
          value={policy.version}
          onChange={(event) => policy.setVersion(event.target.value)}
        />
      </div>
      <Textarea
        rows={8}
        value={policy.json}
        onChange={(event) => policy.setJson(event.target.value)}
      />
      <div className="flex flex-wrap gap-2">
        <Button onClick={actions.createPolicy}>Create Policy</Button>
        <Button
          variant="secondary"
          disabled={!agent.id || !policy.id}
          onClick={actions.bindPolicy}
        >
          Bind Policy
        </Button>
      </div>
      <div className="grid gap-3 md:grid-cols-2">
        <Input
          placeholder="agent id"
          value={agent.id}
          onChange={(event) => agent.setId(event.target.value)}
        />
        <Input
          placeholder="policy id"
          value={policy.id}
          onChange={(event) => policy.setId(event.target.value)}
        />
      </div>
    </TabsContent>
  )
}

function CapabilityActions({
  agent,
  capability,
  actions,
}: Pick<Controller, "agent" | "capability" | "actions">) {
  return (
    <TabsContent value="capability" className="space-y-4 pt-4">
      <div className="grid gap-3 md:grid-cols-2">
        <Input
          placeholder="action"
          value={capability.action}
          onChange={(event) => capability.setAction(event.target.value)}
        />
        <Input
          placeholder="target service"
          value={capability.target}
          onChange={(event) => capability.setTarget(event.target.value)}
        />
      </div>
      <div className="grid gap-3 md:grid-cols-2">
        <Textarea
          rows={5}
          value={capability.scopes}
          onChange={(event) => capability.setScopes(event.target.value)}
        />
        <Textarea
          rows={5}
          value={capability.limits}
          onChange={(event) => capability.setLimits(event.target.value)}
        />
      </div>
      <div className="grid gap-3 md:grid-cols-[1fr_auto]">
        <Input
          placeholder="agent id"
          value={agent.id}
          onChange={(event) => agent.setId(event.target.value)}
        />
        <Input
          placeholder="ttl minutes"
          value={capability.ttlMinutes}
          onChange={(event) => capability.setTtlMinutes(event.target.value)}
        />
      </div>
      <Button disabled={!agent.id} onClick={actions.requestCapability}>
        Request Capability
      </Button>
      <Textarea
        rows={4}
        placeholder="capability token"
        value={capability.token}
        onChange={(event) => capability.setToken(event.target.value)}
      />
    </TabsContent>
  )
}

function VerifyActions({
  agent,
  capability,
  verification,
  actions,
}: Pick<Controller, "agent" | "capability" | "verification" | "actions">) {
  return (
    <TabsContent value="verify" className="space-y-4 pt-4">
      <div className="rounded-md border border-border/70 bg-muted/40 p-3">
        <div className="mb-2 flex flex-wrap items-center gap-2">
          <Badge variant={verification.hasDevKey ? "secondary" : "outline"}>
            {verification.hasDevKey ? "dev key loaded" : "no dev key"}
          </Badge>
          <span className="text-xs text-muted-foreground">
            Dev helper: generate keypair, sign payload, then verify.
          </span>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button variant="secondary" onClick={actions.generateDevKeypair}>
            Generate Dev Keypair
          </Button>
          <Button variant="secondary" onClick={actions.setAllowPreset}>
            Preset ALLOW
          </Button>
          <Button variant="secondary" onClick={actions.setDenySpendPreset}>
            Preset DENY Spend
          </Button>
          <Button variant="secondary" onClick={actions.signVerifyRequest}>
            Sign Verify Request
          </Button>
        </div>
      </div>

      <div className="grid gap-3 md:grid-cols-2">
        <Input
          placeholder="action type"
          value={verification.action}
          onChange={(event) => verification.setAction(event.target.value)}
        />
        <Input
          placeholder="target service"
          value={verification.target}
          onChange={(event) => verification.setTarget(event.target.value)}
        />
      </div>
      <Textarea
        rows={6}
        value={verification.payload}
        onChange={(event) => verification.setPayload(event.target.value)}
      />
      <Textarea
        rows={4}
        placeholder="base64 signature"
        value={verification.signature}
        onChange={(event) => verification.setSignature(event.target.value)}
      />
      <Textarea
        rows={4}
        placeholder="capability token"
        value={capability.token}
        onChange={(event) => capability.setToken(event.target.value)}
      />
      <Button
        disabled={!agent.id || !capability.token || !verification.signature}
        onClick={actions.verifyAction}
      >
        Verify Action
      </Button>
    </TabsContent>
  )
}

function AuditActions({ audit, actions }: Pick<Controller, "audit" | "actions">) {
  return (
    <TabsContent value="audit" className="space-y-4 pt-4">
      <div className="grid gap-3 md:grid-cols-[1fr_auto_auto]">
        <Select
          value={audit.mode}
          onValueChange={(value) =>
            audit.setMode(value as "events" | "export-json" | "export-csv")
          }
        >
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="events">/audit/events</SelectItem>
            <SelectItem value="export-json">/audit/export.json</SelectItem>
            <SelectItem value="export-csv">/audit/export.csv</SelectItem>
          </SelectContent>
        </Select>
        <Select
          value={audit.decisionFilter}
          onValueChange={(value) =>
            audit.setDecisionFilter(value as "ALL" | "ALLOW" | "DENY")
          }
        >
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="ALL">All decisions</SelectItem>
            <SelectItem value="ALLOW">ALLOW</SelectItem>
            <SelectItem value="DENY">DENY</SelectItem>
          </SelectContent>
        </Select>
        <Button onClick={actions.runAuditQuery}>Run Audit Query</Button>
      </div>
      <div className="flex flex-wrap gap-2">
        <Button variant="secondary" onClick={actions.checkAuditIntegrity}>
          Check Integrity
        </Button>
        <Button variant="secondary" onClick={actions.readMetrics}>
          Read Metrics
        </Button>
      </div>
    </TabsContent>
  )
}

export function ApiActions({ controller }: { controller: Controller }) {
  const { workspace, agent, policy, capability, verification, audit, actions } = controller

  return (
    <Card className="border-border/70 bg-card/80">
      <CardHeader>
        <CardTitle>API Actions</CardTitle>
        <CardDescription>
          Trigger endpoint calls with editable payloads. IDs are auto-filled from successful
          responses.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="agents" className="w-full">
          <TabsList className="grid w-full grid-cols-6">
            <TabsTrigger value="workspace">Workspace</TabsTrigger>
            <TabsTrigger value="agents">Agents</TabsTrigger>
            <TabsTrigger value="policy">Policy</TabsTrigger>
            <TabsTrigger value="capability">Capability</TabsTrigger>
            <TabsTrigger value="verify">Verify</TabsTrigger>
            <TabsTrigger value="audit">Audit</TabsTrigger>
          </TabsList>
          <WorkspaceActions workspace={workspace} actions={actions} />
          <AgentActions agent={agent} actions={actions} />
          <PolicyActions agent={agent} policy={policy} actions={actions} />
          <CapabilityActions agent={agent} capability={capability} actions={actions} />
          <VerifyActions
            agent={agent}
            capability={capability}
            verification={verification}
            actions={actions}
          />
          <AuditActions audit={audit} actions={actions} />
        </Tabs>
      </CardContent>
    </Card>
  )
}

