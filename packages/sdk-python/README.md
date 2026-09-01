# limiq-sdk (Python)

Minimal Python SDK for Limiq.io.

## Features (v0.1)
- deterministic canonicalization (backend-compatible)
- Ed25519 key generation and signature
- verify request builder
- sync + async HTTP clients for capability/verify

## Install (local workspace)
```bash
python -m pip install -e "packages/sdk-python[dev]"
```

```python
from limiq_sdk import LimiqClient

client = LimiqClient(
    base_url="http://localhost:8000",
    workspace_id="<workspace_uuid>",
    workspace_key="<workspace_api_key>",
)
```
