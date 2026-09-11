#!/usr/bin/env python3
"""Generate tool-specific agent files from the canonical repo source.

Source of truth:  agents/<name>/agent.md   (the persona body)
                  agents/<name>/meta.yaml  (description + per-tool config)

Output:           dist/opencode/agents/<name>.md
                  dist/codex/agents/<name>.toml
                  dist/claude/agents/<name>.md

Run:  python3 build.py          (regenerates everything under dist/)
Then: bash sync.sh              (copies dist/ into the three runtime dirs)

Adding an agent: create agents/<name>/agent.md and meta.yaml, rerun both.
"""
import json
import pathlib
import sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parent
AGENTS_DIR = ROOT / "agents"
DIST = ROOT / "dist"

OPENCODE_OUT = DIST / "opencode" / "agents"
CODEX_OUT = DIST / "codex" / "agents"
CLAUDE_OUT = DIST / "claude" / "agents"


def must_none(body: str, needle: str, what: str) -> None:
    if needle in body:
        sys.exit(f"ERROR: {what} contains {needle!r}; refusing to generate")


def toml_str(value: str) -> str:
    """Quote a string safely inside a TOML basic string."""
    return json.dumps(value, ensure_ascii=False)


def write_opencode(name, meta, body, out: pathlib.Path) -> None:
    frontmatter = {
        "description": meta["description"],
        "mode": meta["opencode"].get("mode", "all"),
        "permission": meta["opencode"].get("permission", {}),
    }
    text = "---\n" + yaml.safe_dump(frontmatter, sort_keys=False,
                                    allow_unicode=True, default_flow_style=False) + "---\n" + body
    out.write_text(text)


def write_codex(name, meta, body, out: pathlib.Path) -> None:
    must_none(body, '"""', f"codex {name}")
    lines = [
        f'name = "{name}"',
        f"description = {toml_str(meta['description'])}",
        'developer_instructions = """',
        body.rstrip("\n"),
        '"""',
        f"sandbox_mode = {toml_str(meta['codex'].get('sandbox_mode', 'workspace-write'))}",
        "",
    ]
    out.write_text("\n".join(lines))


def write_claude(name, meta, body, out: pathlib.Path) -> None:
    frontmatter = {"name": name, "description": meta["description"]}
    tools = meta["claude"].get("tools")
    if tools:
        frontmatter["tools"] = tools
    text = "---\n" + yaml.safe_dump(frontmatter, sort_keys=False,
                                    allow_unicode=True) + "---\n" + body
    out.write_text(text)


def clean(dir_: pathlib.Path, valid_names: set[str]) -> None:
    """Remove generated files that no longer have a canonical source."""
    for p in dir_.glob("*.md"):
        if p.stem not in valid_names:
            p.unlink()
    for p in dir_.glob("*.toml"):
        if p.stem not in valid_names:
            p.unlink()


def main() -> None:
    for d in (OPENCODE_OUT, CODEX_OUT, CLAUDE_OUT):
        d.mkdir(parents=True, exist_ok=True)

    names = sorted(p.name for p in AGENTS_DIR.iterdir()
                   if p.is_dir() and (p / "meta.yaml").exists())
    if not names:
        sys.exit("ERROR: no agent dirs found under agents/")
    valid = set(names)

    clean(OPENCODE_OUT, valid)
    clean(CODEX_OUT, valid)
    clean(CLAUDE_OUT, valid)

    for name in names:
        meta = yaml.safe_load((AGENTS_DIR / name / "meta.yaml").read_text())
        body = (AGENTS_DIR / name / "agent.md").read_text()
        write_opencode(name, meta, body, OPENCODE_OUT / f"{name}.md")
        write_codex(name, meta, body, CODEX_OUT / f"{name}.toml")
        write_claude(name, meta, body, CLAUDE_OUT / f"{name}.md")
        print(f"built {name} (opencode, codex, claude)")


if __name__ == "__main__":
    main()