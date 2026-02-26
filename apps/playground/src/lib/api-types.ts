export interface paths {
    "/health": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Health Check
         * @description Returns API, PostgreSQL and Redis health status.
         */
        get: operations["health_check_health_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/workspaces": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Create Workspace
         * @description Creates a workspace for local bootstrap/dev flows.
         */
        post: operations["create_workspace_endpoint_workspaces_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/workspaces/{workspace_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Get Workspace
         * @description Fetches a workspace by id within authenticated tenant context.
         */
        get: operations["get_workspace_endpoint_workspaces__workspace_id__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/agents": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Create Agent
         * @description Registers a new agent identity in a workspace.
         */
        post: operations["create_agent_endpoint_agents_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/agents/{agent_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Get Agent
         * @description Fetches a single agent by id.
         */
        get: operations["get_agent_endpoint_agents__agent_id__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/agents/{agent_id}/revoke": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Revoke Agent
         * @description Revokes an active agent. Future actions are denied.
         */
        post: operations["revoke_agent_endpoint_agents__agent_id__revoke_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/policies": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Create Policy
         * @description Creates a versioned policy in a workspace.
         */
        post: operations["create_policy_endpoint_policies_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/agents/{agent_id}/bind_policy": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Bind Policy To Agent
         * @description Binds a policy to an agent, deactivating previous active binding if any.
         */
        post: operations["bind_policy_endpoint_agents__agent_id__bind_policy_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/capabilities/request": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Issue Capability
         * @description Issues a signed capability token if agent/policy constraints allow it.
         */
        post: operations["request_capability_endpoint_capabilities_request_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/verify": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Verify Action
         * @description Validates an agent action request against capability token, signature, policy binding and runtime constraints.
         */
        post: operations["verify_endpoint_verify_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/audit/events": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * List Audit Events
         * @description Returns paginated audit events with optional filters.
         */
        get: operations["list_audit_events_endpoint_audit_events_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/audit/export.json": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Export Audit Events (JSON)
         * @description Exports filtered audit events as JSON.
         */
        get: operations["export_audit_json_endpoint_audit_export_json_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/audit/export.csv": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Export Audit Events (CSV)
         * @description Exports filtered audit events as CSV.
         */
        get: operations["export_audit_csv_endpoint_audit_export_csv_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/audit/integrity/check": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Check Audit Chain Integrity
         * @description Verifies hash-chain continuity in a workspace. Returns OK, BROKEN or PARTIAL.
         */
        get: operations["check_audit_integrity_endpoint_audit_integrity_check_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/metrics": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Metrics Endpoint */
        get: operations["metrics_endpoint_metrics_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
}
export type webhooks = Record<string, never>;
export interface components {
    schemas: {
        /** AgentCreateRequest */
        AgentCreateRequest: {
            /**
             * Workspace Id
             * Format: uuid
             * @description Workspace identifier (must match X-Workspace-Id).
             */
            workspace_id: string;
            /**
             * Name
             * @description Human readable agent name.
             */
            name: string;
            /**
             * Public Key
             * @description Base64-encoded Ed25519 public key (32 bytes).
             */
            public_key: string;
            /**
             * Runtime Type
             * @description Optional runtime label (e.g. codex, internal-bot).
             */
            runtime_type?: string | null;
            /**
             * Metadata
             * @description Free-form metadata.
             */
            metadata?: {
                [key: string]: unknown;
            };
        };
        /** AgentResponse */
        AgentResponse: {
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /**
             * Workspace Id
             * Format: uuid
             */
            workspace_id: string;
            /** Name */
            name: string;
            /** Status */
            status: string;
            /** Public Key */
            public_key: string;
            /** Key Alg */
            key_alg: string;
            /** Fingerprint */
            fingerprint: string;
            /** Runtime Type */
            runtime_type: string | null;
            /** Metadata */
            metadata: {
                [key: string]: unknown;
            };
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
            /** Revoked At */
            revoked_at: string | null;
            /** Revoke Reason */
            revoke_reason: string | null;
        };
        /** AgentRevokeRequest */
        AgentRevokeRequest: {
            /**
             * Workspace Id
             * Format: uuid
             * @description Workspace identifier (must match X-Workspace-Id).
             */
            workspace_id: string;
            /**
             * Reason
             * @description Reason for revocation.
             */
            reason: string;
        };
        /** AgentRevokeResponse */
        AgentRevokeResponse: {
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Status */
            status: string;
            /**
             * Revoked At
             * Format: date-time
             */
            revoked_at: string;
        };
        /** AuditEventResponse */
        AuditEventResponse: {
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /**
             * Event Time
             * Format: date-time
             */
            event_time: string;
            /** Event Type */
            event_type: string;
            /**
             * Workspace Id
             * Format: uuid
             */
            workspace_id: string;
            /** Actor Type */
            actor_type: string;
            /** Actor Id */
            actor_id: string | null;
            /** Subject Type */
            subject_type: string;
            /** Subject Id */
            subject_id: string | null;
            /** Event Data */
            event_data: {
                [key: string]: unknown;
            };
            /** Prev Hash */
            prev_hash: string | null;
            /** Event Hash */
            event_hash: string | null;
        };
        /** AuditEventsListResponse */
        AuditEventsListResponse: {
            /** Items */
            items: components["schemas"]["AuditEventResponse"][];
            /** Count */
            count: number;
            /** Limit */
            limit: number;
            /** Offset */
            offset: number;
        };
        /** AuditIntegrityResponse */
        AuditIntegrityResponse: {
            /**
             * Workspace Id
             * Format: uuid
             */
            workspace_id: string;
            /**
             * Status
             * @enum {string}
             */
            status: "OK" | "BROKEN" | "PARTIAL";
            /** Checked Count */
            checked_count: number;
            /** Broken At Event Id */
            broken_at_event_id: string | null;
            /** Message */
            message: string;
        };
        /** CapabilityIssueResponse */
        CapabilityIssueResponse: {
            /**
             * Capability Id
             * Format: uuid
             */
            capability_id: string;
            /** Token */
            token: string;
            /** Jti */
            jti: string;
            /**
             * Issued At
             * Format: date-time
             */
            issued_at: string;
            /**
             * Expires At
             * Format: date-time
             */
            expires_at: string;
        };
        /** CapabilityRequest */
        CapabilityRequest: {
            /**
             * Workspace Id
             * Format: uuid
             * @description Workspace identifier (must match X-Workspace-Id).
             */
            workspace_id: string;
            /**
             * Agent Id
             * Format: uuid
             */
            agent_id: string;
            /**
             * Action
             * @description Requested action.
             */
            action: string;
            /**
             * Target Service
             * @description Target service id.
             */
            target_service: string;
            /**
             * Requested Scopes
             * @description Requested capability scopes.
             */
            requested_scopes: string[];
            /**
             * Requested Limits
             * @description Requested limits.
             */
            requested_limits?: {
                [key: string]: unknown;
            };
            /**
             * Ttl Minutes
             * @description Capability TTL.
             */
            ttl_minutes?: number | null;
        };
        /** PolicyBindRequest */
        PolicyBindRequest: {
            /**
             * Workspace Id
             * Format: uuid
             * @description Workspace identifier (must match X-Workspace-Id).
             */
            workspace_id: string;
            /**
             * Policy Id
             * Format: uuid
             * @description Policy id to bind.
             */
            policy_id: string;
        };
        /** PolicyBindingResponse */
        PolicyBindingResponse: {
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /**
             * Workspace Id
             * Format: uuid
             */
            workspace_id: string;
            /**
             * Agent Id
             * Format: uuid
             */
            agent_id: string;
            /**
             * Policy Id
             * Format: uuid
             */
            policy_id: string;
            /** Status */
            status: string;
            /**
             * Bound At
             * Format: date-time
             */
            bound_at: string;
            /** Unbound At */
            unbound_at: string | null;
        };
        /** PolicyCreateRequest */
        PolicyCreateRequest: {
            /**
             * Workspace Id
             * Format: uuid
             * @description Workspace identifier (must match X-Workspace-Id).
             */
            workspace_id: string;
            /**
             * Name
             * @description Policy name.
             */
            name: string;
            /**
             * Version
             * @description Policy version, unique per (workspace, name).
             */
            version: number;
            /**
             * Schema Version
             * @description Policy schema version.
             * @default 1
             */
            schema_version: number;
            /**
             * Policy Json
             * @description Policy payload.
             */
            policy_json: {
                [key: string]: unknown;
            };
        };
        /** PolicyResponse */
        PolicyResponse: {
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /**
             * Workspace Id
             * Format: uuid
             */
            workspace_id: string;
            /** Name */
            name: string;
            /** Version */
            version: number;
            /** Is Active */
            is_active: boolean;
            /** Schema Version */
            schema_version: number;
            /** Policy Json */
            policy_json: {
                [key: string]: unknown;
            };
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
        };
        /** VerifyRequest */
        VerifyRequest: {
            /**
             * Workspace Id
             * Format: uuid
             * @description Workspace identifier (must match X-Workspace-Id).
             */
            workspace_id: string;
            /**
             * Agent Id
             * Format: uuid
             */
            agent_id: string;
            /** Action Type */
            action_type: string;
            /** Target Service */
            target_service: string;
            /** Payload */
            payload: {
                [key: string]: unknown;
            };
            /**
             * Signature
             * @description Base64-encoded Ed25519 signature.
             */
            signature: string;
            /**
             * Capability Token
             * @description JWT capability token.
             */
            capability_token: string;
            /** Request Context */
            request_context?: {
                [key: string]: unknown;
            };
        };
        /** VerifyResponse */
        VerifyResponse: {
            /**
             * Decision
             * @enum {string}
             */
            decision: "ALLOW" | "DENY";
            /**
             * Reason Code
             * @description Reason code when decision is DENY, otherwise null.
             */
            reason_code?: string | null;
            /**
             * Audit Event Id
             * Format: uuid
             */
            audit_event_id: string;
        };
        /** WorkspaceCreateRequest */
        WorkspaceCreateRequest: {
            /**
             * Name
             * @description Human readable workspace name.
             */
            name: string;
            /**
             * Slug
             * @description Optional unique slug. Lowercase letters, numbers and dashes.
             */
            slug?: string | null;
        };
        /** WorkspaceResponse */
        WorkspaceResponse: {
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Name */
            name: string;
            /** Slug */
            slug: string;
            /** Status */
            status: string;
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
        };
    };
    responses: never;
    parameters: never;
    requestBodies: never;
    headers: never;
    pathItems: never;
}
export type $defs = Record<string, never>;
export interface operations {
    health_check_health_get: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": {
                        [key: string]: string;
                    };
                };
            };
        };
    };
    create_workspace_endpoint_workspaces_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["WorkspaceCreateRequest"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["WorkspaceResponse"];
                };
            };
            /** @description Missing or invalid authentication headers. */
            401: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "AUTH_WORKSPACE_MISSING",
                     *         "message": "Missing X-Workspace-Id header"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Workspace mismatch with authenticated context. */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "WORKSPACE_MISMATCH",
                     *         "message": "Workspace does not match authenticated context"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Workspace slug already exists. */
            409: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "WORKSPACE_SLUG_ALREADY_EXISTS",
                     *         "message": "Workspace slug already exists"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Validation error on payload/query params. */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "VALIDATION_ERROR",
                     *         "message": "Query param 'from' must be <= 'to'"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Workspace bootstrap endpoint disabled by configuration. */
            503: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "WORKSPACE_BOOTSTRAP_DISABLED",
                     *         "message": "Workspace bootstrap is disabled; configure KYA_WORKSPACE_BOOTSTRAP_TOKEN"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
        };
    };
    get_workspace_endpoint_workspaces__workspace_id__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                workspace_id: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["WorkspaceResponse"];
                };
            };
            /** @description Missing or invalid authentication headers. */
            401: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "AUTH_WORKSPACE_MISSING",
                     *         "message": "Missing X-Workspace-Id header"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Workspace mismatch with authenticated context. */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "WORKSPACE_MISMATCH",
                     *         "message": "Workspace does not match authenticated context"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Workspace not found. */
            404: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "WORKSPACE_NOT_FOUND",
                     *         "message": "Workspace not found"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Validation error on payload/query params. */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "VALIDATION_ERROR",
                     *         "message": "Query param 'from' must be <= 'to'"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
        };
    };
    create_agent_endpoint_agents_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["AgentCreateRequest"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AgentResponse"];
                };
            };
            /** @description Missing or invalid authentication headers. */
            401: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "AUTH_WORKSPACE_MISSING",
                     *         "message": "Missing X-Workspace-Id header"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Workspace mismatch with authenticated context. */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "WORKSPACE_MISMATCH",
                     *         "message": "Workspace does not match authenticated context"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Agent fingerprint already exists. */
            409: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "AGENT_FINGERPRINT_ALREADY_EXISTS",
                     *         "message": "An agent with this public key already exists"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Validation error on payload/query params. */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "VALIDATION_ERROR",
                     *         "message": "Query param 'from' must be <= 'to'"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
        };
    };
    get_agent_endpoint_agents__agent_id__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                agent_id: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AgentResponse"];
                };
            };
            /** @description Missing or invalid authentication headers. */
            401: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "AUTH_WORKSPACE_MISSING",
                     *         "message": "Missing X-Workspace-Id header"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Workspace mismatch with authenticated context. */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "WORKSPACE_MISMATCH",
                     *         "message": "Workspace does not match authenticated context"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Agent not found. */
            404: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "AGENT_NOT_FOUND",
                     *         "message": "Agent not found"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Validation error on payload/query params. */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "VALIDATION_ERROR",
                     *         "message": "Query param 'from' must be <= 'to'"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
        };
    };
    revoke_agent_endpoint_agents__agent_id__revoke_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                agent_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["AgentRevokeRequest"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AgentRevokeResponse"];
                };
            };
            /** @description Missing or invalid authentication headers. */
            401: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "AUTH_WORKSPACE_MISSING",
                     *         "message": "Missing X-Workspace-Id header"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Workspace mismatch with authenticated context. */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "WORKSPACE_MISMATCH",
                     *         "message": "Workspace does not match authenticated context"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Agent not found. */
            404: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "AGENT_NOT_FOUND",
                     *         "message": "Agent not found"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Agent already revoked. */
            409: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "AGENT_ALREADY_REVOKED",
                     *         "message": "Agent is already revoked"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Validation error on payload/query params. */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "VALIDATION_ERROR",
                     *         "message": "Query param 'from' must be <= 'to'"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
        };
    };
    create_policy_endpoint_policies_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["PolicyCreateRequest"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["PolicyResponse"];
                };
            };
            /** @description Missing or invalid authentication headers. */
            401: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "AUTH_WORKSPACE_MISSING",
                     *         "message": "Missing X-Workspace-Id header"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Workspace mismatch with authenticated context. */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "WORKSPACE_MISMATCH",
                     *         "message": "Workspace does not match authenticated context"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Policy version already exists. */
            409: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "POLICY_VERSION_ALREADY_EXISTS",
                     *         "message": "Policy version already exists"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Validation error on payload/query params. */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "VALIDATION_ERROR",
                     *         "message": "Query param 'from' must be <= 'to'"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
        };
    };
    bind_policy_endpoint_agents__agent_id__bind_policy_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                agent_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["PolicyBindRequest"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["PolicyBindingResponse"];
                };
            };
            /** @description Missing or invalid authentication headers. */
            401: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "AUTH_WORKSPACE_MISSING",
                     *         "message": "Missing X-Workspace-Id header"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Workspace mismatch with authenticated context. */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "WORKSPACE_MISMATCH",
                     *         "message": "Workspace does not match authenticated context"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Agent or policy not found. */
            404: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "POLICY_OR_AGENT_NOT_FOUND",
                     *         "message": "Agent or policy not found"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Agent is revoked and cannot be bound. */
            409: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "AGENT_REVOKED",
                     *         "message": "Agent is revoked"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Validation error on payload/query params. */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "VALIDATION_ERROR",
                     *         "message": "Query param 'from' must be <= 'to'"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
        };
    };
    request_capability_endpoint_capabilities_request_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["CapabilityRequest"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["CapabilityIssueResponse"];
                };
            };
            /** @description Missing or invalid authentication headers. */
            401: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "AUTH_WORKSPACE_MISSING",
                     *         "message": "Missing X-Workspace-Id header"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Workspace mismatch with authenticated context. */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "WORKSPACE_MISMATCH",
                     *         "message": "Workspace does not match authenticated context"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Agent or policy binding not found. */
            404: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "POLICY_NOT_BOUND",
                     *         "message": "No active policy binding found for this agent"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Agent revoked. */
            409: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "AGENT_REVOKED",
                     *         "message": "Agent is revoked"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Validation error on payload/query params. */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "VALIDATION_ERROR",
                     *         "message": "Query param 'from' must be <= 'to'"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
        };
    };
    verify_endpoint_verify_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["VerifyRequest"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["VerifyResponse"];
                };
            };
            /** @description Missing or invalid authentication headers. */
            401: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "AUTH_WORKSPACE_MISSING",
                     *         "message": "Missing X-Workspace-Id header"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Workspace mismatch with authenticated context. */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "WORKSPACE_MISMATCH",
                     *         "message": "Workspace does not match authenticated context"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Validation error on payload/query params. */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "VALIDATION_ERROR",
                     *         "message": "Query param 'from' must be <= 'to'"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
        };
    };
    list_audit_events_endpoint_audit_events_get: {
        parameters: {
            query: {
                /** @description Workspace identifier */
                workspace_id: string;
                /** @description Start datetime */
                from?: string | null;
                /** @description End datetime */
                to?: string | null;
                /** @description Filter by event type */
                event_type?: string | null;
                /** @description Filter by subject id */
                subject_id?: string | null;
                /** @description ALLOW or DENY filter */
                decision?: ("ALLOW" | "DENY") | null;
                /** @description Page size */
                limit?: number;
                /** @description Page offset */
                offset?: number;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AuditEventsListResponse"];
                };
            };
            /** @description Missing or invalid authentication headers. */
            401: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "AUTH_WORKSPACE_MISSING",
                     *         "message": "Missing X-Workspace-Id header"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Workspace mismatch with authenticated context. */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "WORKSPACE_MISMATCH",
                     *         "message": "Workspace does not match authenticated context"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Validation error on payload/query params. */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "VALIDATION_ERROR",
                     *         "message": "Query param 'from' must be <= 'to'"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
        };
    };
    export_audit_json_endpoint_audit_export_json_get: {
        parameters: {
            query: {
                /** @description Workspace identifier */
                workspace_id: string;
                /** @description Start datetime */
                from?: string | null;
                /** @description End datetime */
                to?: string | null;
                /** @description Filter by event type */
                event_type?: string | null;
                /** @description Filter by subject id */
                subject_id?: string | null;
                /** @description ALLOW or DENY filter */
                decision?: ("ALLOW" | "DENY") | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AuditEventResponse"][];
                };
            };
            /** @description Missing or invalid authentication headers. */
            401: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "AUTH_WORKSPACE_MISSING",
                     *         "message": "Missing X-Workspace-Id header"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Workspace mismatch with authenticated context. */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "WORKSPACE_MISMATCH",
                     *         "message": "Workspace does not match authenticated context"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Validation error on payload/query params. */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "VALIDATION_ERROR",
                     *         "message": "Query param 'from' must be <= 'to'"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
        };
    };
    export_audit_csv_endpoint_audit_export_csv_get: {
        parameters: {
            query: {
                /** @description Workspace identifier */
                workspace_id: string;
                /** @description Start datetime */
                from?: string | null;
                /** @description End datetime */
                to?: string | null;
                /** @description Filter by event type */
                event_type?: string | null;
                /** @description Filter by subject id */
                subject_id?: string | null;
                /** @description ALLOW or DENY filter */
                decision?: ("ALLOW" | "DENY") | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Missing or invalid authentication headers. */
            401: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "AUTH_WORKSPACE_MISSING",
                     *         "message": "Missing X-Workspace-Id header"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Workspace mismatch with authenticated context. */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "WORKSPACE_MISMATCH",
                     *         "message": "Workspace does not match authenticated context"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Validation error on payload/query params. */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "VALIDATION_ERROR",
                     *         "message": "Query param 'from' must be <= 'to'"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
        };
    };
    check_audit_integrity_endpoint_audit_integrity_check_get: {
        parameters: {
            query: {
                /** @description Workspace identifier */
                workspace_id: string;
                /** @description Start datetime */
                from?: string | null;
                /** @description End datetime */
                to?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AuditIntegrityResponse"];
                };
            };
            /** @description Missing or invalid authentication headers. */
            401: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "AUTH_WORKSPACE_MISSING",
                     *         "message": "Missing X-Workspace-Id header"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Workspace mismatch with authenticated context. */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "WORKSPACE_MISMATCH",
                     *         "message": "Workspace does not match authenticated context"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
            /** @description Validation error on payload/query params. */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    /**
                     * @example {
                     *       "detail": {
                     *         "code": "VALIDATION_ERROR",
                     *         "message": "Query param 'from' must be <= 'to'"
                     *       }
                     *     }
                     */
                    "application/json": unknown;
                };
            };
        };
    };
    metrics_endpoint_metrics_get: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
        };
    };
}
