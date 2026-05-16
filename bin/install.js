#!/usr/bin/env node
/**
 * research-paper installer (alternative to `npx skills add`)
 * ==========================================================
 *
 * The PRIMARY recommended install path is:
 *   npx skills add aniketkrs/research-paper
 *
 * That's the runtime-neutral universal installer that detects all
 * compatible agent runtimes (Claude Code, OpenCode, Cursor, Cline,
 * Codex, Aider, Amp, Antigravity, AiderDesk, Augment, IBM Bob, and
 * 50+ others) and installs the skill into the universal
 * `.agents/skills/` directory used by all of them.
 *
 * This script is a SECONDARY direct-install fallback for users who
 * want to install without `npx skills`. It copies this repository
 * into a target skills directory.
 *
 * Usage:
 *   npx -y github:aniketkrs/research-paper install [--target <path>] [--scope user|project]
 *   npx -y github:aniketkrs/research-paper uninstall [--target <path>]
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

const SKILL_NAME = "research-paper";
// The actual skill content lives in <repo>/skills/<SKILL_NAME>/
// (the skills.sh / npx skills convention).
const SKILL_ROOT = path.resolve(__dirname, "..", "skills", SKILL_NAME);

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
  // Default: project scope (mirrors `npx skills` default)
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
function cmdInstall(opts) {
  const target = resolveTarget(opts);
  ensureDir(target);
  const dest = path.join(target, SKILL_NAME);

  if (fs.existsSync(dest)) {
    console.log(`! Skill already installed at: ${dest}`);
    console.log(`  Replacing with current version...`);
    rmDir(dest);
  }

  copyDir(SKILL_ROOT, dest);

  // Read version from manifest
  let version = "unknown";
  try {
    const manifest = JSON.parse(
      fs.readFileSync(path.join(dest, "manifest.json"), "utf-8")
    );
    version = manifest.version || version;
  } catch (_) {}

  console.log(`✓ Installed ${SKILL_NAME} v${version}`);
  console.log(`  Location: ${dest}`);
  console.log("");
  console.log("Tip: the recommended install path is the runtime-neutral");
  console.log("     'npx skills add aniketkrs/research-paper' command,");
  console.log("     which auto-detects all installed agent runtimes.");
  console.log("");
  console.log("Next steps:");
  console.log("  1. Restart your agent session.");
  console.log(`  2. Try:  /research "your topic" --depth quick`);
  console.log(`  3. Read: ${path.join(dest, "SKILL.md")}`);
}

function cmdUninstall(opts) {
  const target = resolveTarget(opts);
  const dest = path.join(target, SKILL_NAME);
  if (!fs.existsSync(dest)) {
    console.log(`Skill not installed at: ${dest}`);
    process.exit(1);
  }
  rmDir(dest);
  console.log(`✓ Uninstalled ${SKILL_NAME}`);
  console.log(`  Removed: ${dest}`);
}

function cmdStatus(opts) {
  const target = resolveTarget(opts);
  const dest = path.join(target, SKILL_NAME);
  console.log(`Target directory: ${target}`);
  if (fs.existsSync(dest)) {
    let version = "unknown";
    try {
      const manifest = JSON.parse(
        fs.readFileSync(path.join(dest, "manifest.json"), "utf-8")
      );
      version = manifest.version || version;
    } catch (_) {}
    console.log(`Status: installed`);
    console.log(`  Version: ${version}`);
    console.log(`  Path: ${dest}`);
    const skillMd = path.join(dest, "SKILL.md");
    if (fs.existsSync(skillMd)) {
      console.log(`  SKILL.md: ✓`);
    } else {
      console.log(`  SKILL.md: ✗ (corrupted install — try reinstalling)`);
    }
  } else {
    console.log(`Status: not installed`);
    console.log(`  Recommended install:  npx skills add aniketkrs/research-paper`);
    console.log(`  Direct install:        npx -y github:aniketkrs/research-paper install`);
  }
}

function cmdHelp() {
  console.log(`
research-paper — Direct installer (alternative to 'npx skills add')

PREFERRED install path (runtime-neutral, auto-detects all agents):
  npx skills add aniketkrs/research-paper

DIRECT install path (this script):
  npx -y github:aniketkrs/research-paper install   [--target <path>] [--scope user|project]
  npx -y github:aniketkrs/research-paper uninstall [--target <path>]
  npx -y github:aniketkrs/research-paper status    [--target <path>]
  npx -y github:aniketkrs/research-paper --help

Options:
  --target <path>   Install destination (default: $AGENT_SKILLS_DIR or ./.agents/skills/)
  --scope user      User scope (~/.agents/skills/)
  --scope project   Project scope (./.agents/skills/, default)
  --help, -h        Show this help

Environment:
  AGENT_SKILLS_DIR  Override the default install directory.

Examples:
  # Project-scope (default; like 'npx skills add' default)
  npx -y github:aniketkrs/research-paper install

  # User-scope (global)
  npx -y github:aniketkrs/research-paper install --scope user

  # Custom directory
  npx -y github:aniketkrs/research-paper install --target ./my-agents-folder

  # Status
  npx -y github:aniketkrs/research-paper status

  # Uninstall
  npx -y github:aniketkrs/research-paper uninstall

Once installed, in any compatible agent session:
  /research "your topic" --depth standard --style ieee

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
