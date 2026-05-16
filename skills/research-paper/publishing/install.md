# Installation Guide

This skill is a standard agent skill: a folder with `SKILL.md`,
`manifest.json`, and supporting modules. It works with **any agent
runtime that speaks the agent-skills protocol** — no Claude- or
vendor-specific assumptions.

The recommended installer is the official `npx skills` CLI, which
auto-detects every agent runtime on your machine and installs the skill
into the runtime-neutral `.agents/skills/` directory used by all of
them (50+ supported: Claude Code, OpenCode, Cursor, Cline, Codex, Aider,
Amp, Antigravity, AiderDesk, Augment, IBM Bob, and more).

---

## 1. Recommended: `npx skills` (universal)

```bash
npx skills add aniketkrs/research-paper
```

That's it. The installer:

- Clones this repository.
- Detects every agent runtime on your machine.
- Installs the skill into `.agents/skills/research-paper/` (project
  scope by default).
- Symlinks the skill into runtime-specific locations where needed
  (e.g., for Claude Code, OpenCode, etc.).

### Verify

```bash
npx skills list
npx skills find research-paper
```

### Pin to a version

```bash
npx skills add aniketkrs/research-paper#v2.0.1
```

### Install globally (user scope)

```bash
npx skills add aniketkrs/research-paper --global
```

### Install to specific agents only

```bash
npx skills add aniketkrs/research-paper --agent claude-code
npx skills add aniketkrs/research-paper --agent cursor
npx skills add aniketkrs/research-paper --agent '*'         # all detected
```

### List supported agents on your machine

```bash
npx skills add aniketkrs/research-paper --list
```

### Update / upgrade

```bash
npx skills update research-paper
```

### Remove

```bash
npx skills remove research-paper
```

---

## 2. Alternative: direct npx from GitHub (no `npx skills` required)

If you can't or don't want to use the `npx skills` CLI, this repo also
ships a direct installer:

```bash
# Project scope (default)
npx -y github:aniketkrs/research-paper install

# User scope
npx -y github:aniketkrs/research-paper install --scope user

# Custom target
npx -y github:aniketkrs/research-paper install --target ./my-agents/
```

Both end up in the runtime-neutral `.agents/skills/` directory. The
only difference is that the direct installer doesn't auto-detect /
symlink to per-runtime locations — you'd handle that yourself if your
runtime requires it.

---

## 3. Manual install — universal (any agent runtime)

```bash
git clone https://github.com/aniketkrs/research-paper.git
mkdir -p .agents/skills
mv research-paper .agents/skills/
```

Most agent runtimes will auto-detect skills in `.agents/skills/`
(project scope) or `~/.agents/skills/` (user scope).

---

## 4. Manual install — Claude Code (one specific runtime)

Claude Code looks in two locations:

| Scope         | Location                                    |
| ------------- | ------------------------------------------- |
| User          | `~/.claude/skills/research-paper/`           |
| Project       | `<project>/.claude/skills/research-paper/`   |

### macOS / Linux

```bash
git clone https://github.com/aniketkrs/research-paper.git
mkdir -p ~/.claude/skills
mv research-paper ~/.claude/skills/
```

### Windows (PowerShell)

```powershell
git clone https://github.com/aniketkrs/research-paper.git
$dest = "$HOME\.claude\skills\research-paper"
New-Item -ItemType Directory -Force -Path (Split-Path $dest) | Out-Null
Move-Item -Force .\research-paper $dest
```

### Verify

In a Claude Code session:

> `/research "Test of the research-paper skill" --depth quick`

Expected: a 2-page paper with citations and at least one figure.

---

## 5. Manual install — OpenCode

```bash
# Project scope
git clone https://github.com/aniketkrs/research-paper.git \
    .opencode/skills/research-paper

# User scope
git clone https://github.com/aniketkrs/research-paper.git \
    ~/.config/opencode/skills/research-paper
```

---

## 6. Manual install — other runtimes

| Runtime                | Skills directory (typical)                   |
| ---------------------- | -------------------------------------------- |
| Cursor agents           | `.cursor/skills/` or `~/.cursor/skills/`      |
| Cline                   | `.cline/skills/` or `~/.cline/skills/`        |
| Codex                   | `.codex/skills/` or `~/.codex/skills/`        |
| Aider                   | `~/.aider/skills/`                            |
| Amp                     | `~/.amp/skills/`                              |
| Antigravity              | `~/.antigravity/skills/`                      |
| AiderDesk                | per-app preferences                            |
| Augment                  | `~/.augment/skills/`                          |
| IBM Bob                  | `~/.bob/skills/`                              |

When in doubt, use `npx skills add aniketkrs/research-paper` and it
will resolve the right location automatically.

---

## 7. Manual install — Claude Desktop

1. Settings → Skills → Add Skill → Import from folder.
2. Select the `research-paper/` folder (or a zip of it).
3. Restart the app if prompted.

---

## 8. Manual install — claude.ai (web)

1. Zip the directory:

   **macOS / Linux:**
   ```bash
   zip -r research-paper.zip research-paper
   ```

   **Windows (PowerShell):**
   ```powershell
   Compress-Archive -Path .\research-paper -DestinationPath research-paper.zip
   ```

2. Skills → Upload Skill → upload the zip.
3. Enable in the conversation panel.

---

## 9. Manual install — Anthropic API / SDK (programmatic)

```python
import os
from pathlib import Path
from anthropic import Anthropic

SKILL_DIR = Path("./research-paper")
skill_md = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")

client = Anthropic()

response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=8000,
    system=(
        "You are an academic research assistant. The following skill is "
        "available; activate it when the user requests academic writing.\n\n"
        f"<skill name='research-paper'>\n{skill_md}\n</skill>"
    ),
    tools=[
        # Provide filesystem tools so the model can read modules on demand
        # (read_file, list_dir, write_file, run_shell — at minimum read/write).
    ],
    messages=[
        {"role": "user", "content": "/research \"Graph neural networks for fraud detection\" --style ieee"}
    ],
)
print(response.content[0].text)
```

The skill is built for **progressive disclosure**: only `SKILL.md`
needs to be in the system prompt. The model reads heavier modules on
demand.

---

## 10. Manual install — generic agent runtime

Most runtimes follow the same SKILL.md convention. Drop the folder
into the runtime's skills directory, and ensure the runtime exposes
filesystem read tools.

If your runtime supports a universal `.agents/skills/` lookup (most
modern ones do), use option 3 above.

---

## 11. Optional Python toolchain

The skill emits Markdown tables + Mermaid diagrams by default. To
enable real chart images and statistical validation:

```bash
python -m pip install --upgrade \
    pandas numpy scipy statsmodels \
    matplotlib seaborn plotly scikit-learn pyyaml
```

Verify:
```bash
python toolchains/generate_charts.py --self-test
python toolchains/analyze_data.py --self-test
```

If Python is unavailable, the skill detects it and falls back to
Mermaid / Markdown — never a silent failure.

---

## 12. Updating

```bash
npx skills update research-paper                          # via npx skills
npx -y github:aniketkrs/research-paper install            # direct re-install
cd <skill-dir>/research-paper && git pull                  # manual
```

Bump `manifest.json → version` whenever you make local changes.

---

## 13. Uninstalling

```bash
npx skills remove research-paper                           # via npx skills
npx -y github:aniketkrs/research-paper uninstall           # via direct installer
rm -rf <skill-dir>/research-paper                          # manual
```

---

## 14. Troubleshooting

| Symptom                              | Likely cause                                | Fix                                                  |
| ------------------------------------ | ------------------------------------------- | ---------------------------------------------------- |
| Skill never activates                 | YAML frontmatter malformed                  | Check `SKILL.md` head with a YAML linter             |
| Slash commands don't trigger          | Command not registered in runtime            | Check `manifest.json → trigger.commands`             |
| Charts come out as Markdown only      | Python deps missing                          | See §11                                                |
| Wrong citation format                  | Style not specified or mixed                  | Re-run `format_bibliography.py --style <one-style>`  |
| Output truncated mid-section          | Context pressure                             | Switch to multi-file output (`long_context/multi-file-output.md`) |
| Filesystem errors                      | Tool permissions                             | Grant read/write to the working directory            |
| "I cannot read that file"              | Filesystem tool missing                      | Provide `read_file` to the runtime                   |
| Skill activates for unrelated requests | Trigger patterns too broad                   | Edit `manifest.json → trigger.patterns`              |

---

## 15. Security notes

- The skill does not require network access by default.
- Python toolchain scripts read / write only inside the working
  directory.
- No telemetry, no phone-home.
- Web search / fetch is **optional** and only used when the runtime
  exposes those tools.
- The skill never auto-publishes papers anywhere; delivery is local
  only unless the user explicitly invokes Pandoc, git, or another
  publishing pipeline.
