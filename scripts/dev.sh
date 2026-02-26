#!/usr/bin/env bash
set -euo pipefail

if [ ! -d "apps/api/.venv" ]; then
  make install
fi

cp -n apps/api/.env.example apps/api/.env || true
docker compose up -d
make migrate-up
make dev
