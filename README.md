# Know Your Agent (KYA)

Identity & Permission Layer for Autonomous Agents.

Current status: `v0.x` MVP. APIs may evolve between minor releases.

## What It Does
- agent identity registry
- policy binding
- capability token issuance
- signed action verification (ALLOW/DENY + reason)
- audit trail with export and integrity check

## Quickstart (Mac)
Prerequisites:
- Docker Desktop
- Python 3.12+
- `make`

From repository root:

```bash
make install
cp apps/api/.env.example apps/api/.env
# optional: copy root template for cross-component env hints
cp .env.example .env
docker compose up -d
make migrate-up
make dev
```

Generate your dev keypair (required before starting API):
```bash
make generate-dev-keypair
```
This prints `KYA_JWT_PRIVATE_KEY_PEM` and `KYA_JWT_PUBLIC_KEY_PEM` values to paste into `apps/api/.env`.

API base URL:
- `http://localhost:8000`

## API Docs
- OpenAPI JSON: `http://localhost:8000/openapi.json`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Guides:
- `docs/API_GUIDE_V01.md`
- `docs/OPENAPI_REDOC_V01.md`

## Dev Commands
```bash
make lint
make test
make migrate-up
make verify-all
make generate-dev-keypair
```

## Front Playground (Internal Dev Tool)
The repository includes an API playground at `apps/playground` for rapid endpoint testing.

Prerequisite:
- `pnpm` (`corepack enable && corepack prepare pnpm@latest --activate`)

Commands:
```bash
pnpm install
pnpm --filter playground dev
pnpm --filter playground build
pnpm --filter playground types:api
```

`types:api` uses `openapi/openapi.snapshot.json` by default (CI-safe).
Use live API instead:
```bash
OPENAPI_SOURCE=url pnpm --filter playground types:api
```

## SDK JS (MVP)
`packages/sdk-js` provides:
- key generation (Ed25519, base64)
- canonicalization + signature helpers
- verify request builder
- lightweight KYA API client for capability + verify

Commands:
```bash
pnpm --filter @kya/sdk-js test
pnpm --filter @kya/sdk-js build
```

Integration examples:
- `examples/express-target/README.md`
- `examples/fastapi-target/README.md`

Runnable examples:
```bash
# Express target
cd examples/express-target && npm install && npm run dev

# FastAPI target
cd examples/fastapi-target && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && uvicorn main:app --reload
```

Smoke check for examples:
```bash
bash scripts/examples_smoke.sh
```

## SDK Python (MVP)
`packages/sdk-python` provides parity helpers for Python integrators:
- canonicalization + Ed25519 signature
- verify request builder
- sync and async client helpers

Commands:
```bash
python -m pip install -e "packages/sdk-python[dev]"
pytest -q packages/sdk-python/tests
```

## Architecture
- `docs/ARCHITECTURE_V01.md`

## Contributing
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`

## Security
- `SECURITY.md`

## Support
- `SUPPORT.md`

## License
Apache-2.0 — see `LICENSE`.
