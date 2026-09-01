# Security Policy

## Reporting a Vulnerability
Please use **GitHub Security Advisories** to report vulnerabilities privately.
Do not open public issues for security-sensitive reports.

## Response Process (Best Effort)
- Initial triage target: within 5 business days
- Status updates: as available during investigation
- Fix timeline: depends on severity and complexity

## Scope
This policy covers the code in this repository, including API routes, auth/context handling, signing/verification, and audit integrity logic.

## Current Boundary
Tenant routes require a workspace ID and an HMAC-derived workspace key. Capability tokens are bound to the agent, workspace and target service; spend checks use exact decimal values and currency matching. See the explicit non-goals in the main README before exposing the reference implementation to untrusted users.

## Disclosure
After a fix is available, maintainers may publish a summary in release notes/changelog.
