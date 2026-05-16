#!/usr/bin/env node
/**
 * test-runner.js
 * ==============
 * Lightweight test runner for the research-paper skill.
 *
 * Repo layout (skills.sh / npx skills convention):
 *   .
 *   ├── README.md, LICENSE, CHANGELOG.md, etc.   ← repo root
 *   ├── bin/install.js, tests/, docs/            ← repo-level
 *   └── skills/
 *       └── research-paper/                       ← actual skill
 *           ├── SKILL.md, manifest.json
 *           ├── instructions/, orchestration/, ...
 *           └── toolchains/*.py
 *
 * Usage:
 *   node tests/test-runner.js
 *   node tests/test-runner.js --verbose
 */

"use strict";

const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const REPO_ROOT = path.resolve(__dirname, "..");
const SKILL = path.join(REPO_ROOT, "skills", "research-paper");
const SKILL_GET = path.join(REPO_ROOT, "skills", "get-research-paper");
const VERBOSE = process.argv.includes("--verbose");

let pass = 0;
let fail = 0;
const failures = [];

function test(name, fn) {
  try {
    fn();
    pass++;
    console.log(`  ✓ ${name}`);
  } catch (e) {
    fail++;
    failures.push({ name, error: e.message });
    console.log(`  ✗ ${name}`);
    console.log(`    ${e.message}`);
  }
}

function assert(cond, msg) {
  if (!cond) throw new Error(msg);
}

function exists(absPath) {
  return fs.existsSync(absPath);
}

function repoFile(rel) {
  const p = path.join(REPO_ROOT, rel);
  assert(exists(p), `Missing repo file: ${rel}`);
}

function skillFile(rel) {
  const p = path.join(SKILL, rel);
  assert(exists(p), `Missing skill file: skills/research-paper/${rel}`);
}

function getSkillFile(rel) {
  const p = path.join(SKILL_GET, rel);
  assert(exists(p), `Missing skill file: skills/get-research-paper/${rel}`);
}

function readJson(absPath) {
  return JSON.parse(fs.readFileSync(absPath, "utf-8"));
}

function readText(absPath) {
  return fs.readFileSync(absPath, "utf-8");
}

// ---------------------------------------------------------------------------
console.log("\n=== research-paper test runner ===\n");

console.log("• Repo-level files (root)");
[
  "README.md",
  "INSTALLATION.md",
  "CHANGELOG.md",
  "LICENSE",
  "package.json",
  "bin/install.js",
  ".gitignore",
].forEach((f) => test(f, () => repoFile(f)));

console.log("\n• Skill structure (skills/research-paper/)");
[
  "SKILL.md",
  "manifest.json",
  "instructions/core.md",
  "instructions/activation.md",
  "instructions/multi-agent.md",
  "instructions/voice-and-tone.md",
  "orchestration/pipeline.md",
  "orchestration/agents.md",
  "orchestration/routing.md",
  "orchestration/failure-handling.md",
  "long_context/strategy.md",
  "long_context/chunking.md",
  "long_context/multi-file-output.md",
  "memory/citation-memory.md",
  "memory/methodology-memory.md",
  "memory/session-state.md",
  "quality_control/publication-checklist.md",
  "quality_control/known-gaps-protocol.md",
  "quality_control/final-gate.md",
  "publishing/install.md",
  "templates/arxiv-paper.md",
  "templates/ieee-paper.md",
  "templates/acm-paper.md",
  "templates/nature-paper.md",
  "templates/harvard-paper.md",
  "templates/literature-review.md",
  "templates/thesis-chapter.md",
  "templates/whitepaper.md",
  "templates/survey-paper.md",
  "templates/policy-paper.md",
  "schemas/paper-schema.json",
  "schemas/citation-schema.json",
  "toolchains/format_bibliography.py",
  "toolchains/validate_citations.py",
  "toolchains/analyze_data.py",
  "toolchains/generate_charts.py",
  "toolchains/statistical_validation.py",
  "examples/sample-paper-arxiv.md",
  "examples/bibliography.example.yaml",
].forEach((f) => test(f, () => skillFile(f)));

console.log("\n• SKILL.md frontmatter");
test("SKILL.md has YAML frontmatter", () => {
  const text = readText(path.join(SKILL, "SKILL.md"));
  assert(text.startsWith("---"), "no opening ---");
  const second = text.indexOf("---", 3);
  assert(second > 0, "no closing ---");
  const fm = text.slice(3, second);
  assert(/name:\s*research-paper/.test(fm), "name not set to research-paper");
  assert(/description:/.test(fm), "no description field");
  assert(/version:/.test(fm), "no version field");
  assert(/license:/.test(fm), "no license field");
});

console.log("\n• manifest.json schema");
test("manifest.json parses", () => readJson(path.join(SKILL, "manifest.json")));
test("manifest.json has required fields", () => {
  const m = readJson(path.join(SKILL, "manifest.json"));
  ["name", "version", "description", "trigger", "capabilities",
   "supported_formats", "supported_citation_styles", "files",
   "quality_gates"].forEach((k) =>
    assert(m[k] !== undefined, `manifest missing field: ${k}`));
  assert(m.name === "research-paper", "name mismatch");
  assert(/^\d+\.\d+\.\d+/.test(m.version), "version is not semver");
  assert(Array.isArray(m.trigger.commands), "trigger.commands not array");
  assert(m.trigger.commands.includes("/research"), "/research command missing");
});

console.log("\n• Citation schema validity");
test("schemas/citation-schema.json is valid JSON Schema", () => {
  const s = readJson(path.join(SKILL, "schemas", "citation-schema.json"));
  assert(s["$schema"], "missing $schema");
  assert(s.type === "object", "type must be object");
  assert(s.required && s.required.length > 0, "no required fields");
});

console.log("\n• Python toolchain self-tests (optional)");
function tryPython(args) {
  const r = spawnSync("python", args, { cwd: SKILL, encoding: "utf-8" });
  return { code: r.status, out: r.stdout || "", err: r.stderr || "" };
}
test("python interpreter present", () => {
  const r = tryPython(["--version"]);
  if (r.code !== 0) throw new Error("python not on PATH (optional)");
});
test("generate_charts.py --self-test", () => {
  const r = tryPython(["toolchains/generate_charts.py", "--self-test"]);
  if (r.code !== 0) {
    if (VERBOSE) console.log(r.err);
    throw new Error("self-test failed (or python missing)");
  }
});
test("analyze_data.py --self-test", () => {
  const r = tryPython(["toolchains/analyze_data.py", "--self-test"]);
  if (r.code !== 0) throw new Error("self-test failed (or python missing)");
});

console.log("\n• Citation pipeline smoke test");
test("format_bibliography.py runs against fixture", () => {
  const fix = path.join(REPO_ROOT, "tests", "fixtures");
  const r = tryPython([
    "toolchains/format_bibliography.py",
    "--bib", path.join(fix, "small-bibliography.json"),
    "--paper", path.join(fix, "small-paper-draft.md"),
    "--out", path.join(fix, "small-paper-cited.tmp.md"),
    "--style", "ieee",
  ]);
  if (r.code !== 0) {
    if (VERBOSE) console.log(r.err);
    throw new Error("format_bibliography.py failed (python deps?)");
  }
  const cited = fs.readFileSync(
    path.join(fix, "small-paper-cited.tmp.md"), "utf-8");
  assert(/\[1\]/.test(cited), "no IEEE [1] citation in output");
  assert(/## References/.test(cited), "no References section");
  fs.unlinkSync(path.join(fix, "small-paper-cited.tmp.md"));
});

console.log("\n• get-research-paper skill structure (skills/get-research-paper/)");
[
  "SKILL.md",
  "manifest.json",
  "instructions/core.md",
  "workflows/search.md",
  "workflows/synthesis.md",
  "workflows/handoff-to-writer.md",
  "sources/source-priority.md",
  "sources/arxiv.md",
  "sources/google-scholar.md",
  "sources/semantic-scholar.md",
  "sources/pubmed.md",
  "prompts/search-strategy.md",
  "prompts/summarization.md",
  "prompts/ranking.md",
  "templates/reading-list.md",
  "templates/paper-summary.md",
  "templates/briefing.md",
  "schemas/paper-result.json",
  "toolchains/arxiv_search.py",
  "examples/sample-results.md",
].forEach((f) => test(`get-research-paper/${f}`, () => getSkillFile(f)));

console.log("\n• get-research-paper SKILL.md frontmatter");
test("get-research-paper SKILL.md has YAML frontmatter", () => {
  const text = readText(path.join(SKILL_GET, "SKILL.md"));
  assert(text.startsWith("---"), "no opening ---");
  const second = text.indexOf("---", 3);
  assert(second > 0, "no closing ---");
  const fm = text.slice(3, second);
  assert(/name:\s*get-research-paper/.test(fm), "name not set to get-research-paper");
  assert(/description:/.test(fm), "no description field");
  assert(/version:/.test(fm), "no version field");
});

console.log("\n• get-research-paper manifest.json schema");
test("get-research-paper manifest.json parses", () => readJson(path.join(SKILL_GET, "manifest.json")));
test("get-research-paper manifest.json has required fields", () => {
  const m = readJson(path.join(SKILL_GET, "manifest.json"));
  ["name", "version", "description", "trigger", "capabilities",
   "supported_sources", "files"].forEach((k) =>
    assert(m[k] !== undefined, `manifest missing field: ${k}`));
  assert(m.name === "get-research-paper", "name mismatch");
  assert(/^\d+\.\d+\.\d+/.test(m.version), "version is not semver");
  assert(Array.isArray(m.trigger.commands), "trigger.commands not array");
  assert(m.trigger.commands.includes("/get-research-paper"),
    "/get-research-paper command missing");
  assert(m.trigger.commands.includes("/find-paper"),
    "/find-paper command missing");
});

console.log("\n• get-research-paper paper-result schema");
test("paper-result schema is valid JSON Schema", () => {
  const s = readJson(path.join(SKILL_GET, "schemas", "paper-result.json"));
  assert(s["$schema"], "missing $schema");
  assert(s.type === "object", "type must be object");
  assert(s.required && s.required.length > 0, "no required fields");
});

console.log("\n• arxiv_search.py self-test (optional)");
function tryPythonGet(args) {
  const r = spawnSync("python", args, { cwd: SKILL_GET, encoding: "utf-8" });
  return { code: r.status, out: r.stdout || "", err: r.stderr || "" };
}
test("arxiv_search.py --self-test", () => {
  const r = tryPythonGet(["toolchains/arxiv_search.py", "--self-test"]);
  if (r.code !== 0) {
    if (VERBOSE) console.log(r.err);
    throw new Error("self-test failed");
  }
  assert(/urllib stdlib: True/.test(r.out), "urllib not detected");
  assert(/xml\.etree stdlib: True/.test(r.out), "xml.etree not detected");
});

// ---------------------------------------------------------------------------
console.log(`\n=== Result: ${pass} passed, ${fail} failed ===`);
if (fail > 0) {
  console.log("\nFailures:");
  failures.forEach((f) => console.log(`  - ${f.name}: ${f.error}`));
  process.exit(1);
}
process.exit(0);
