#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-.tmp/dev-keys}"
mkdir -p "$OUT_DIR"

PRIVATE_PEM="$OUT_DIR/private.pem"
PUBLIC_PEM="$OUT_DIR/public.pem"

openssl genpkey -algorithm ed25519 -out "$PRIVATE_PEM"
openssl pkey -in "$PRIVATE_PEM" -pubout -out "$PUBLIC_PEM"

echo "Generated keypair:"
echo "  private: $PRIVATE_PEM"
echo "  public : $PUBLIC_PEM"
echo

echo "Copy these values into apps/api/.env:"
PRIVATE_ESCAPED=$(awk '{printf "%s\\n", $0}' "$PRIVATE_PEM")
PUBLIC_ESCAPED=$(awk '{printf "%s\\n", $0}' "$PUBLIC_PEM")
printf 'KYA_JWT_PRIVATE_KEY_PEM="%s"\n' "$PRIVATE_ESCAPED"
printf 'KYA_JWT_PUBLIC_KEY_PEM="%s"\n' "$PUBLIC_ESCAPED"
