#!/usr/bin/env node
/**
 * research-paper installer
 * ========================
 *
 * Copies the skill into a Claude / Agent Skills runtime directory.
 *
 * Usage:
 *   npx @aniketkrs/research-paper install [--target <path>] [--scope user|project]
 *   npx @aniketkrs/research-paper uninstall [--target <path>]
 *   npx @aniketkrs/research-paper status [--target <path>]
 *   npx @aniketkrs/research-paper --help
 *
 * Default targets (in order of preference):
 *   - $CLAUDE_SKILLS_DIR (env override)
 *   - ~/.claude/skills/        (Claude Code, user scope)
 *   - .claude/skills/          (Claude Code, project scope, when --scope project)
 *   - ~/.config/opencode/skills/ (OpenCode)
 */

"use strict";

const fs = require("fs");
const path = require("path");
const os = require("os");

const SKILL_NAME = "research-paper";
const SKILL_ROOT = path.resolve(__dirname, "..");

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
// Target resolution
// ---------------------------------------------------------------------------
function resolveTarget(opts) {
  if (opts.target) return path.resolve(opts.target);
  if (process.env.CLAUDE_SKILLS_DIR) {
    return path.resolve(process.env.CLAUDE_SKILLS_DIR);
  }
  if (opts.scope === "project") {
    return path.resolve(process.cwd(), ".claude", "skills");
  }
  return path.resolve(os.homedir(), ".claude", "skills");
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
  console.log("Next steps:");
  console.log("  1. Restart your Claude Code / agent session.");
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
    console.log(`  Run:  npx @aniketkrs/research-paper install`);
  }
}

function cmdHelp() {
  console.log(`
@aniketkrs/research-paper — Claude Agent Skill installer

Usage:
  npx @aniketkrs/research-paper install   [--target <path>] [--scope user|project]
  npx @aniketkrs/research-paper uninstall [--target <path>]
  npx @aniketkrs/research-paper status    [--target <path>]
  npx @aniketkrs/research-paper --help

Options:
  --target <path>   Install destination (default: $CLAUDE_SKILLS_DIR or ~/.claude/skills)
  --scope user      Install to user scope (default; ~/.claude/skills)
  --scope project   Install to project scope (./.claude/skills)
  --help, -h        Show this help

Environment:
  CLAUDE_SKILLS_DIR Override the default install directory.

Examples:
  npx @aniketkrs/research-paper install
  npx @aniketkrs/research-paper install --scope project
  npx @aniketkrs/research-paper install --target ~/.config/opencode/skills/
  npx @aniketkrs/research-paper uninstall
  npx @aniketkrs/research-paper status

Once installed, in Claude Code / OpenCode:
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
