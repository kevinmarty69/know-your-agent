# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Open source governance and contribution baseline documents.
- Workspace bootstrap endpoint (`POST /workspaces`) and workspace get route.
- Internal playground updates for workspace management and dev signing helpers.
- SDK JS package (`@kya/sdk-js`) with canonicalization/signature/client helpers.
- Shared verify test vectors (including non-ASCII key coverage).
- Runnable integration examples (`examples/express-target`, `examples/fastapi-target`).
- Examples smoke script + CI job.
- SDK Python package (`kya-sdk`) with sync/async clients and vector compatibility tests.

### Changed
- Canonical key ordering hardened to pure lexicographic ordering (no locale sorting).
- CI expanded with dedicated `sdk_js`, `sdk_python`, and `examples_smoke` jobs.

## [0.5.0] - 2026-02-25

### Added
- MVP backend capabilities including:
  - agent registry
  - policy binding
  - capability issuance
  - verification engine
  - audit exports
  - audit integrity check
  - OpenAPI/ReDoc documentation
