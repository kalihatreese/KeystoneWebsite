#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")"/.. && pwd)"
echo "Running Keystone FULL install in $ROOT"
cd "$ROOT"

# ensure .env exists
cp -n .env.example .env || true
echo "Created .env from example if missing. Edit .env and fill secrets as per docs/HUMAN-ACTION-CHECKLIST.md"

# if docker available, start compose
if command -v docker >/dev/null 2>&1 && command -v docker-compose >/dev/null 2>&1; then
  echo "Starting docker compose..."
  docker compose -f infra/docker-compose.yml up -d --build || true
  echo "Sleeping 4s to let services initialize..."
  sleep 4
  docker compose -f infra/docker-compose.yml ps
else
  echo "Docker not available - skipping container start. Install Docker for full dev experience."
fi

echo "To deploy serverless APIs to Vercel, set VERCEL_TOKEN and run: vercel --prod"
echo "Full install finished (scaffold). Edit .env and set production secrets per docs/HUMAN-ACTION-CHECKLIST.md"
