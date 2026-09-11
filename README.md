# Agents

Personal AI agent definitions for opencode, Codex, and Claude Code, kept in
one repo so every agent stays in sync across all three tools.

The Sisyphus engineering workflow (Erwin Smith and his council) is the
decision engine; these agents are the cast it routes work to, plus two
study companions (Frieren and Koro-sensei) that live outside the workflow.

## Layout

```
agents/<name>/
  agent.md      the persona body. The single source of truth, written once.
  meta.yaml     description + per-tool config (permissions, sandbox, tools)
dist/           generated output, one format per tool. Committed for
                convenience so others can copy without running the build.
build.py        reads agents/, writes dist/
sync.sh         copies dist/ into the three runtime directories
```

The three tools need three different file shapes for the same agent:

- opencode:  `~/.config/opencode/agents/<name>.md`   (YAML frontmatter)
- Codex:     `~/.codex/agents/<name>.toml`           (TOML, developer_instructions)
- Claude:    `~/.claude/agents/<name>.md`            (YAML frontmatter with tools)

You only edit `agents/<name>/agent.md` and `meta.yaml`. Everything else is
generated.

## Adding an agent

1. Create `agents/<name>/agent.md` with the persona instructions.
2. Create `agents/<name>/meta.yaml`:

   ```yaml
   name: <name>
   description: <what this agent is for>
   opencode:
     mode: all              # or subagent
     permission: { ... }    # opencode permission block
   codex:
     sandbox_mode: workspace-write   # or read-only
   claude:
     tools: Glob, Grep, Read, Write  # tools for the Claude subagent
   ```

3. Rebuild and sync into all three tools:

   ```bash
   python3 build.py
   bash sync.sh
   ```

That's it. The agent now exists in opencode, Codex, and Claude Code.

## Copying these agents elsewhere

If you fork these and run them on your machine, expect to adjust the
hardcoded personal paths in the prompt bodies. They were written for one
person's filesystem: `~/Documents/projects/my-notes` (Frieren's vault),
`~/learning-hub/recaps` and `~/Documents/projects/learn/publish.sh`
(Koro-sensei's hub), and `~/.agents/sisyphus` (the workflow). Steal the
format, keep the voices, change the paths.

## License

MIT. See [LICENSE](LICENSE).