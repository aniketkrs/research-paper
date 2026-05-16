# Publishing — Per-Platform Installation

This skill ships as a standard Anthropic Agent Skill: a folder with
`SKILL.md`, `manifest.json`, and supporting modules. It works
**anywhere Agent Skills are supported**.

The fastest install is via npx; manual install is also covered for
each runtime.

---

## 1. One-line install (npx)

The fastest way (works immediately, no npm account needed):

```bash
npx -y github:aniketkrs/research-paper install
```

If/when published to npm:

```bash
npx @aniketkrs/research-paper install
```

Both copy the skill into your active skills directory. Restart your
session and the skill activates on academic-writing requests.

To pin a version (GitHub):

```bash
npx -y github:aniketkrs/research-paper#v2.0.0 install
```

To pin a version (npm):

```bash
npx @aniketkrs/research-paper@2.0.0 install
```

To install into a specific runtime's directory:

```bash
npx -y github:aniketkrs/research-paper install --target ~/.claude/skills/
npx -y github:aniketkrs/research-paper install --target ~/.config/opencode/skills/
npx -y github:aniketkrs/research-paper install --scope project    # ./.claude/skills
```

---

## 2. Manual install — Claude Code (CLI)

Two scopes:

| Scope          | Location                                    |
| -------------- | ------------------------------------------- |
| User-scope     | `~/.claude/skills/research-paper/`           |
| Project-scope  | `<project>/.claude/skills/research-paper/`   |

### Install

**macOS / Linux:**
```bash
git clone https://github.com/aniketkrs/research-paper.git
mkdir -p ~/.claude/skills
mv research-paper ~/.claude/skills/research-paper
```

**Windows (PowerShell):**
```powershell
git clone https://github.com/aniketkrs/research-paper.git
$dest = "$HOME\.claude\skills\research-paper"
New-Item -ItemType Directory -Force -Path (Split-Path $dest) | Out-Null
Move-Item -Force .\research-paper $dest
```

### Verify

In a Claude Code session:

> "List the skills you have available."

Expected: `research-paper` appears with the description from
`manifest.json`.

> `/research "Test of the research-paper skill" --depth quick`

Expected: a 2-page paper with citations and at least one figure.

---

## 3. Manual install — Claude Desktop

1. Settings → Skills → Add Skill → Import from folder.
2. Select the `research-paper/` folder (or a zip of it).
3. Restart the app if prompted.

---

## 4. Manual install — claude.ai (web)

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

## 5. Manual install — Anthropic API / SDK (programmatic)

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
needs to be in the system prompt. The model reads heavier modules
(workflows, templates, engines) on demand.

---

## 6. Manual install — OpenCode

```bash
mkdir -p ~/.config/opencode/skills
git clone https://github.com/aniketkrs/research-paper.git \
    ~/.config/opencode/skills/research-paper
```

Or project-scope:
```bash
mkdir -p .opencode/skills
git clone https://github.com/aniketkrs/research-paper.git \
    .opencode/skills/research-paper
```

---

## 7. Manual install — generic agent runtime

Most runtimes (Aider, Cline, Cursor agents, custom LangGraph /
LlamaIndex agents) follow the same SKILL.md convention. Drop the
folder into the runtime's skills directory, and ensure the runtime
exposes filesystem read tools.

---

## 8. Optional Python toolchain

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
Mermaid / Markdown — never silent failure.

---

## 9. Updating

```bash
cd ~/.claude/skills/research-paper
git pull
```

Or via npx:
```bash
npx @aniketkrs/research-paper@latest install
```

Bump `manifest.json → version` whenever you make local changes.

---

## 10. Uninstalling

```bash
rm -rf ~/.claude/skills/research-paper
```

Or via the skills CLI:
```bash
npx skills remove research-paper
```

---

## 11. Troubleshooting

| Symptom                              | Likely cause                                | Fix                                                  |
| ------------------------------------ | ------------------------------------------- | ---------------------------------------------------- |
| Skill never activates                 | YAML frontmatter malformed                  | Check `SKILL.md` head with a YAML linter             |
| Slash commands don't trigger          | Command not registered in runtime            | Check `manifest.json → trigger.commands`             |
| Charts come out as Markdown only      | Python deps missing                          | See §8                                                |
| Wrong citation format                  | Style not specified or mixed                  | Re-run `format_bibliography.py --style <one-style>`  |
| Output truncated mid-section          | Context pressure                             | Switch to multi-file output (long_context/multi-file-output.md) |
| Filesystem errors                      | Tool permissions                             | Grant read/write to the working directory            |
| "I cannot read that file"              | Filesystem tool missing                      | Provide `read_file` to the runtime                   |
| Skill activates for unrelated requests | Trigger patterns too broad                   | Edit `manifest.json → trigger.patterns`              |

---

## 12. Security notes

- Skill does not require network access by default.
- Python scripts read / write only inside the working directory.
- No telemetry, no phone-home.
- Web search / fetch is **optional** and only used when the runtime
  exposes those tools.
- The skill never auto-publishes papers anywhere; delivery is local
  only unless the user explicitly invokes Pandoc, git, or another
  publishing pipeline.
