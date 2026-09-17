# Kakashi Agent Documentation

## Overview

Kakashi is a read-only code explainer agent. Give it a file path, function name, or snippet from your workspace and it explains **why** the code is written that way — purpose, design choices, tradeoffs, context, and sharp edges.

## Usage

### opencode
```bash
# In opencode chat
@kakashi why does parseConfig in src/config/parser.ts use a visitor pattern?
```

### Codex
```toml
# ~/.codex/agents/kakashi.toml is auto-generated
# Use via Codex agent selector
```

### Claude Code
```bash
# In Claude Code
> kakashi explain the retry logic in src/http/client.py
```

## Input Format

Kakashi accepts:
- **File path**: `src/utils/parser.ts`
- **Function name**: `parseConfig`
- **Snippet**: paste code directly
- **Directory**: `src/auth/` (explains the module)

## What It Returns

For each explanation, Kakashi covers:

| Section | What You Get |
|---------|--------------|
| **Purpose** | What problem this solves |
| **Design choice** | Why this pattern over the obvious alternative |
| **Tradeoffs** | What was accepted vs rejected |
| **Context** | Legacy, workaround, or deliberate constraint |
| **Watch outs** | Where it breaks, footguns, fragility |

## Example

**You**: "Why is `parseConfig` in `src/config/parser.ts` using a visitor pattern instead of a simple switch?"

**Kakashi**: "Because the config schema has 12 node types and they added a plugin system in v3. A switch would've meant touching this file every time a plugin adds a node. The visitor lets plugins extend without modifying core. Tradeoff: harder to follow for newcomers. See `src/config/visitors/plugin-adapter.ts:45` for how plugins hook in."

## Constraints

- **Read-only** — never modifies files
- **Workspace-scoped** — works from current directory
- **Honest gaps** — if context is missing (no tests, no git history), it says so
- **No hallucination** — if code isn't found, it tells you

## Configuration

Source of truth: `/home/jonas/agents/agents/kakashi/`
- `agent.md` — persona body
- `meta.yaml` — description + per-tool config

Regenerate after changes:
```bash
cd /home/jonas/agents && python3 build.py && bash sync.sh
```