.PHONY: dev install test lint fmt migrate-up verify-all generate-dev-keypair examples-purchase-smoke

install:
	cd apps/api && python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements-dev.txt

dev:
	cd apps/api && . .venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	cd apps/api && . .venv/bin/activate && pytest

lint:
	cd apps/api && . .venv/bin/activate && ruff check . && mypy app

fmt:
	cd apps/api && . .venv/bin/activate && ruff format .

migrate-up:
	cd apps/api && . .venv/bin/activate && alembic upgrade head

verify-all:
	bash scripts/verify_all.sh

generate-dev-keypair:
	bash scripts/generate_dev_keypair.sh

examples-purchase-smoke:
	bash scripts/examples_purchase_smoke.sh
