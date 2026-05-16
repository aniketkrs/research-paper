#!/usr/bin/env node
/**
 * research-paper installer (alternative to `npx skills add`)
 * ==========================================================
 *
 * The PRIMARY recommended install path is:
 *   npx skills add aniketkrs/research-paper --yes --skill '*'
 *
 * The `--yes --skill '*'` flags make it one-shot, no prompts.
 * That's the runtime-neutral universal installer that detects all
 * compatible agent runtimes (Claude Code, OpenCode, Cursor, Cline,
 * Codex, Aider, Amp, Antigravity, AiderDesk, Augment, IBM Bob, and
 * 50+ others) and installs the skills into the universal
 * `.agents/skills/` directory used by all of them.
 *
 * This script is a SECONDARY direct-install fallback. It installs ALL
 * skills under <repo>/skills/ in one shot, no prompting.
 *
 * Usage:
 *   npx -y github:aniketkrs/research-paper install [--target <path>] [--scope user|project] [--skill <name>]
 *   npx -y github:aniketkrs/research-paper uninstall [--target <path>] [--skill <name>]
 *   npx -y github:aniketkrs/research-paper status [--target <path>]
 *   npx -y github:aniketkrs/research-paper --help
 *
 * Default targets (in order of preference):
 *   - $AGENT_SKILLS_DIR (env override)
 *   - <cwd>/.agents/skills/    (project scope, runtime-neutral, universal)
 *   - ~/.agents/skills/         (user scope, runtime-neutral, universal)
 */

"use strict";

const fs = require("fs");
const path = require("path");
const os = require("os");

// All skills live under <repo>/skills/. The installer auto-discovers them.
const REPO_ROOT = path.resolve(__dirname, "..");
const SKILLS_ROOT = path.join(REPO_ROOT, "skills");

// ---------------------------------------------------------------------------
// Argument parsing
// ---------------------------------------------------------------------------
function parseArgs(argv) {
  const args = { _: [], options: {} };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--help" || a === "-h") {
      args.options.help = true;
    } else if (a === "--target") {
      args.options.target = argv[++i];
    } else if (a === "--scope") {
      args.options.scope = argv[++i];
    } else if (a === "--skill") {
      args.options.skill = argv[++i];
    } else if (a.startsWith("--")) {
      const [k, v] = a.slice(2).split("=");
      args.options[k] = v === undefined ? true : v;
    } else {
      args._.push(a);
    }
  }
  return args;
}

// ---------------------------------------------------------------------------
// Skill discovery
// ---------------------------------------------------------------------------
function discoverSkills() {
  if (!fs.existsSync(SKILLS_ROOT)) return [];
  return fs.readdirSync(SKILLS_ROOT, { withFileTypes: true })
    .filter((e) => e.isDirectory())
    .filter((e) => fs.existsSync(path.join(SKILLS_ROOT, e.name, "SKILL.md")))
    .map((e) => e.name)
    .sort();
}

function readSkillVersion(skillName) {
  try {
    const m = JSON.parse(
      fs.readFileSync(
        path.join(SKILLS_ROOT, skillName, "manifest.json"), "utf-8"));
    return m.version || "unknown";
  } catch (_) {
    return "unknown";
  }
}

// ---------------------------------------------------------------------------
// Target resolution — runtime-neutral, matches `npx skills` convention
// ---------------------------------------------------------------------------
function resolveTarget(opts) {
  if (opts.target) return path.resolve(opts.target);
  if (process.env.AGENT_SKILLS_DIR) {
    return path.resolve(process.env.AGENT_SKILLS_DIR);
  }
  if (opts.scope === "user" || opts.scope === "global") {
    return path.resolve(os.homedir(), ".agents", "skills");
  }
  return path.resolve(process.cwd(), ".agents", "skills");
}

// ---------------------------------------------------------------------------
// File ops
// ---------------------------------------------------------------------------
function ensureDir(d) {
  fs.mkdirSync(d, { recursive: true });
}

function copyDir(src, dst) {
  ensureDir(dst);
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    if (entry.name === ".git" || entry.name === "node_modules") continue;
    const sp = path.join(src, entry.name);
    const dp = path.join(dst, entry.name);
    if (entry.isDirectory()) {
      copyDir(sp, dp);
    } else if (entry.isFile()) {
      fs.copyFileSync(sp, dp);
    }
  }
}

function rmDir(d) {
  if (!fs.existsSync(d)) return;
  fs.rmSync(d, { recursive: true, force: true });
}

// ---------------------------------------------------------------------------
// Commands
// ---------------------------------------------------------------------------
function pickSkills(opts, available) {
  if (!opts.skill || opts.skill === "*" || opts.skill === "all") {
    return available.slice();
  }
  // Comma-separated list
  const requested = opts.skill.split(",").map((s) => s.trim()).filter(Boolean);
  const missing = requested.filter((s) => !available.includes(s));
  if (missing.length) {
    console.error(`✗ Unknown skill(s): ${missing.join(", ")}`);
    console.error(`  Available: ${available.join(", ")}`);
    process.exit(1);
  }
  return requested;
}

function cmdInstall(opts) {
  const available = discoverSkills();
  if (available.length === 0) {
    console.error("✗ No skills found in repo. Expected skills/<name>/SKILL.md.");
    process.exit(1);
  }
  const target = resolveTarget(opts);
  ensureDir(target);

  const skills = pickSkills(opts, available);
  console.log(`Installing ${skills.length} skill${skills.length === 1 ? "" : "s"} to ${target}\n`);

  for (const name of skills) {
    const src = path.join(SKILLS_ROOT, name);
    const dest = path.join(target, name);
    if (fs.existsSync(dest)) {
      console.log(`  · ${name}: replacing existing install`);
      rmDir(dest);
    }
    copyDir(src, dest);
    const version = readSkillVersion(name);
    console.log(`  ✓ ${name.padEnd(22)} v${version}`);
  }

  console.log("");
  console.log("Next steps:");
  console.log("  1. Restart your agent session.");
  console.log("  2. Try one of:");
  console.log("       /research \"your topic\" --style ieee");
  console.log("       /find-paper \"your topic\"");
  console.log("       /read-paper https://arxiv.org/abs/1706.03762");
  console.log("");
  console.log("Tip: the runtime-neutral install is");
  console.log("       npx skills add aniketkrs/research-paper --yes --skill '*'");
}

function cmdUninstall(opts) {
  const available = discoverSkills();
  const target = resolveTarget(opts);
  const skills = pickSkills(opts, available);

  let removed = 0;
  for (const name of skills) {
    const dest = path.join(target, name);
    if (fs.existsSync(dest)) {
      rmDir(dest);
      console.log(`  ✓ Removed ${name}`);
      removed++;
    } else {
      console.log(`  · Not installed: ${name}`);
    }
  }
  if (removed === 0) {
    console.log("Nothing to remove.");
  }
}

function cmdStatus(opts) {
  const available = discoverSkills();
  const target = resolveTarget(opts);
  console.log(`Target directory: ${target}\n`);
  for (const name of available) {
    const dest = path.join(target, name);
    if (fs.existsSync(dest)) {
      let version = "unknown";
      try {
        version = JSON.parse(
          fs.readFileSync(path.join(dest, "manifest.json"), "utf-8")
        ).version || version;
      } catch (_) {}
      const ok = fs.existsSync(path.join(dest, "SKILL.md"));
      console.log(`  ✓ ${name.padEnd(22)} v${version}  ${ok ? "OK" : "(corrupted — reinstall)"}`);
    } else {
      console.log(`  · ${name.padEnd(22)} not installed`);
    }
  }
  console.log("");
  console.log(`To install all: npx -y github:aniketkrs/research-paper install`);
  console.log(`To install one: npx -y github:aniketkrs/research-paper install --skill <name>`);
}

function cmdHelp() {
  const available = discoverSkills();
  console.log(`
research-paper — Direct installer (alternative to 'npx skills add')

PREFERRED install path (runtime-neutral, no prompts, all skills):
  npx skills add aniketkrs/research-paper --yes --skill '*'

DIRECT install path (this script — installs all skills by default):
  npx -y github:aniketkrs/research-paper install   [--target <path>] [--scope user|project] [--skill <name>]
  npx -y github:aniketkrs/research-paper uninstall [--target <path>] [--skill <name>]
  npx -y github:aniketkrs/research-paper status    [--target <path>]
  npx -y github:aniketkrs/research-paper --help

Options:
  --target <path>     Install destination (default: $AGENT_SKILLS_DIR or ./.agents/skills/)
  --scope user        User scope (~/.agents/skills/)
  --scope project     Project scope (./.agents/skills/, default)
  --skill <name(s)>   Comma-separated skill names, or '*' for all (default: all)
  --help, -h          Show this help

Environment:
  AGENT_SKILLS_DIR    Override the default install directory.

Available skills in this repo:
${available.map((n) => "  · " + n + "  v" + readSkillVersion(n)).join("\n")}

Examples:
  # Install all three (default)
  npx -y github:aniketkrs/research-paper install

  # Install only one
  npx -y github:aniketkrs/research-paper install --skill research-paper

  # Install user-scope
  npx -y github:aniketkrs/research-paper install --scope user

  # Custom target
  npx -y github:aniketkrs/research-paper install --target ~/my-agents/

Once installed, in any compatible agent session:
  /research "your topic" --style ieee
  /find-paper "your topic"
  /read-paper <URL or path>

See:
  https://github.com/aniketkrs/research-paper
`.trim());
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
function main() {
  const args = parseArgs(process.argv.slice(2));
  const cmd = args._[0] || (args.options.help ? "help" : "install");

  try {
    switch (cmd) {
      case "install": return cmdInstall(args.options);
      case "uninstall":
      case "remove":
        return cmdUninstall(args.options);
      case "status": return cmdStatus(args.options);
      case "help":
      case "-h":
      case "--help":
        return cmdHelp();
      default:
        console.error(`Unknown command: ${cmd}`);
        cmdHelp();
        process.exit(1);
    }
  } catch (err) {
    console.error(`✗ Error: ${err.message}`);
    process.exit(1);
  }
}

main();
