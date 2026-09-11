#!/usr/bin/env bash
# Copy generated dist/ files into the three runtime agent directories.
# Run after python3 build.py.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

copy_dir() {
  local src="$1" dst="$2"
  if [[ ! -d "$dst" ]]; then
    echo "SKIP: $dst does not exist" >&2
    return
  fi
  cp -f "$src"/* "$dst"/
  echo "synced -> $dst"
}

copy_dir "$ROOT/dist/opencode/agents" "$HOME/.config/opencode/agents"
copy_dir "$ROOT/dist/codex/agents" "$HOME/.codex/agents"
copy_dir "$ROOT/dist/claude/agents" "$HOME/.claude/agents"

echo "done"