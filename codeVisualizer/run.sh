#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd "$(dirname "$0")" && pwd)"

if [[ ! -x "$project_dir/.venv/bin/uvicorn" ]]; then
  echo "Missing Python environment. Follow the setup steps in README.md first."
  exit 1
fi

if [[ ! -d "$project_dir/web/node_modules" ]]; then
  echo "Missing frontend dependencies. Run npm install in web/ first."
  exit 1
fi

cleanup() {
  if [[ -n "${api_pid:-}" ]]; then
    kill "$api_pid" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

cd "$project_dir"
PYTHONPATH="$project_dir" .venv/bin/uvicorn server.app.main:app --reload --port 8000 &
api_pid=$!

cd "$project_dir/web"
npm run dev
