# Tests

A lightweight test suite for the `research-paper` skill.

## Run

```bash
node tests/test-runner.js
```

Or with verbose output:

```bash
node tests/test-runner.js --verbose
```

## What's tested

1. **Required files exist** — every key file in the skill is present.
2. **SKILL.md frontmatter** — YAML frontmatter parses with required fields.
3. **manifest.json schema** — valid JSON, required fields, correct types.
4. **Citation schema** — `schemas/citation-schema.json` is a valid JSON Schema.
5. **Python toolchain self-tests** (optional) — each script's `--self-test`
   reports its dependency status.
6. **Citation pipeline smoke test** — runs `format_bibliography.py` against
   `tests/fixtures/` and verifies IEEE-style output.

## Adding a test

Open `test-runner.js`, add a `test("name", () => { ... })` block. Use the
provided `assert(cond, msg)` and `fileExists(rel)` helpers.

## Fixtures

- `fixtures/small-bibliography.json` — a 2-entry JSON bibliography.
- `fixtures/small-paper-draft.md` — a tiny draft with `[cite_key]`
  placeholders.
- `golden-outputs/` — expected outputs for regression checks (optional).

## Continuous integration

Hook the test runner into your CI:

```yaml
# .github/workflows/test.yml
name: test
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install pandas numpy scipy matplotlib seaborn pyyaml
      - run: node tests/test-runner.js
```

## Failure modes

The runner exits non-zero on any failure. Failures print the test name and
the assertion message. Run with `--verbose` to see Python stderr from
toolchain tests.

## Coverage

Currently the suite covers structure, schemas, and the citation pipeline.
Future coverage:

- Statistical validator against fixture papers.
- Visualization decision-engine outputs against expected types.
- Multi-agent dispatch (when a runtime is available).
- End-to-end smoke test (small paper, full pipeline, against golden output).
