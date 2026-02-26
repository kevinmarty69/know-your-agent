# Contributing to Know Your Agent

Thanks for contributing.

## Project Status
The project is currently in `v0.x`.
APIs and internals may change between minor releases.

## Local Setup
From repository root:

```bash
make install
cp apps/api/.env.example apps/api/.env
docker compose up -d
make migrate-up
make lint
make test
```

For playground frontend work:
```bash
corepack enable
corepack prepare pnpm@latest --activate
pnpm install
pnpm --filter playground dev
pnpm --filter playground build
pnpm --filter playground types:api
pnpm --filter @kya/sdk-js test
pnpm --filter @kya/sdk-js build
bash scripts/examples_smoke.sh
python -m pip install -e "packages/sdk-python[dev]"
pytest -q packages/sdk-python/tests
```

Global one-shot verification:
```bash
make verify-all
```

## Branch & PR Workflow
- Create a branch from `main`.
- Keep PRs focused and small.
- Add or update tests for behavior changes.
- Update docs when API/behavior changes.

Suggested branch naming:
- `feat/<short-topic>`
- `fix/<short-topic>`
- `docs/<short-topic>`

## Definition of Done
A contribution is ready when:
- `make lint` passes
- `make test` passes
- `make verify-all` passes before merge for release-sensitive changes
- `pnpm --filter playground build` passes (if frontend changed)
- `pnpm --filter @kya/sdk-js test` passes (if SDK changed)
- `bash scripts/examples_smoke.sh` passes (if examples changed)
- `pytest -q packages/sdk-python/tests` passes (if sdk-python changed)
- docs are updated if needed
- PR description explains what changed and why

## Commit Messages
Use concise, descriptive messages. Example:
- `feat(audit): add integrity check endpoint`
- `fix(verify): enforce workspace match on request`

## Code Style
- Python style enforced by Ruff + mypy.
- Keep changes explicit and maintainable.
- Prefer small modules and clear function contracts.

## Questions
Use GitHub Discussions/Issues for questions and design proposals.
