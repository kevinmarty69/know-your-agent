# Example — FastAPI Target (Runnable)

Simple target service that verifies actions with KYA before executing business logic.

## Prerequisites
- API KYA running on `http://localhost:8000`
- Python 3.12+

## Run
```bash
cd examples/fastapi-target
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
set -a; source .env; set +a
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8001}
```

Server starts on `http://localhost:8001`.

## Endpoints
- `GET /health`
- `POST /purchase`

`POST /purchase` expects the same payload as `POST /verify`.
If KYA returns `DENY`, target returns `403`.
