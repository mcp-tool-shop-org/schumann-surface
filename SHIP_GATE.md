# Ship Gate

> No repo is "done" until every applicable line is checked.
> Copy this into your repo root. Check items off per-release.

**Tags:** `[all]` every repo · `[npm]` `[pypi]` `[vsix]` `[desktop]` `[container]` published artifacts · `[mcp]` MCP servers · `[cli]` CLI tools

Repo shape: Python data pipeline (scripts run by an operator) + a static HTML viewer + a published dataset. Not an npm/PyPI package, not an MCP server, not a desktop app.

---

## A. Security Baseline

- [x] `[all]` SECURITY.md exists (report email, supported versions, response timeline) — executed by `npx @mcptoolshop/shipcheck security-docs` (2026-09-08)
- [x] `[all]` README includes threat model paragraph (data touched, data NOT touched, permissions required) — executed by `npx @mcptoolshop/shipcheck security-docs` (2026-09-08, "Trust and data" section)
- [x] `[all]` No secrets, tokens, or credentials in source or diagnostics output — identity scan `RESULT CLEAN` on the tracked tree 2026-09-08; Hugging Face upload uses the operator's local login, never a token in the repo
- [x] `[all]` No telemetry by default — stated in SECURITY.md and README (2026-09-08)

### Default safety posture

- [x] `[cli|mcp|desktop]` Dangerous actions (kill, delete, restart) require explicit `--allow-*` flag — the only deletion is the fetcher removing its own temporary span file after extraction; no script deletes anything else (2026-09-08)
- [x] `[cli|mcp|desktop]` File operations constrained to known directories — every script writes under `data/` or `viewer/` relative to the checkout (2026-09-08)
- [ ] `[mcp]` SKIP: not an MCP server
- [ ] `[mcp]` SKIP: not an MCP server

## B. Error Handling

- [x] `[all]` Errors follow the Structured Error Shape: `code`, `message`, `hint`, `cause?`, `retryable?` — the verifier reports `VERIFY FAIL: <reasons>` and exits 2; fetch/process assert with the failing entry named; the viewer shows "No data embedded. Run scripts/build_viewer.py." instead of a blank page (2026-09-08)
- [x] `[cli]` Exit codes: 0 ok · 1 user error · 2 runtime error · 3 partial success — verify script exits 0/1; verifier exits 0/2; `pipeline_month.py` prints which months completed (2026-09-08)
- [ ] `[cli]` SKIP: research scripts raise Python tracebacks on programmer error by design; there is no end-user CLI surface to hide them behind `--debug`
- [ ] `[mcp]` SKIP: not an MCP server
- [ ] `[mcp]` SKIP: not an MCP server
- [ ] `[desktop]` SKIP: not a desktop app
- [ ] `[vscode]` SKIP: not a VS Code extension

## C. Operator Docs

- [x] `[all]` README is current: what it does, install, usage, supported platforms + runtime versions (2026-09-08; Python ≥ 3.11, NumPy, SciPy, PyArrow; any OS)
- [x] `[all]` CHANGELOG.md (Keep a Changelog format) (2026-09-08)
- [x] `[all]` LICENSE file present and repo states support status (MIT; SECURITY.md supported-versions table) (2026-09-08)
- [x] `[cli]` `--help` output accurate for all commands and flags — each script's module docstring is its help and states usage and outputs (2026-09-08)
- [ ] `[cli|mcp|desktop]` SKIP: scripts print progress lines only; there are no log levels and nothing sensitive is ever logged
- [ ] `[mcp]` SKIP: not an MCP server
- [ ] `[complex]` SKIP: not a long-running service; recovery is "re-run the script, steps are idempotent"

## D. Shipping Hygiene

- [x] `[all]` `verify` script exists (test + build + smoke in one command) — `verify.sh` (2026-09-08)
- [x] `[all]` Version in manifest matches git tag — `pyproject.toml` 1.0.0, tag `v1.0.0` cut with this treatment (2026-09-08)
- [x] `[all]` Dependency scanning runs in CI (ecosystem-appropriate) — `pip-audit` step in `ci.yml` (2026-09-08)
- [x] `[all]` No known high/critical vulnerabilities in any dependency tree, and Dependabot alerts are enabled — `pip-audit` in CI; Dependabot alerts enabled via the API on 2026-09-08
- [ ] `[all]` SKIP: no automated dependency-update bot by org rule (CI minutes); alerts are enabled, updates are manual
- [ ] `[npm]` SKIP: not an npm package
- [ ] `[npm]` SKIP: not an npm package
- [x] `[npm]` `engines.node` set · `[pypi]` `python_requires` set — `requires-python = ">=3.11"` in pyproject.toml (2026-09-08)
- [ ] `[npm]` SKIP: not published to npm or PyPI; no lockfile because the pipeline has three floor-pinned runtime deps and is run from a checkout
- [ ] `[vsix]` SKIP: not a VS Code extension
- [ ] `[desktop]` SKIP: not a desktop app

## E. Identity (soft gate — does not block ship)

- [x] `[all]` Logo in README header — brand/logos/schumann-surface/readme.png (2026-09-08)
- [x] `[all]` Translations (polyglot-mcp, 8 languages) — TranslateGemma 27B local, 7 languages + nav bar (2026-09-08)
- [x] `[org]` Landing page (@mcptoolshop/site-theme) — site/ with Starlight handbook, viewer served under /viewer/ (2026-09-08)
- [x] `[all]` GitHub repo metadata: description, homepage, topics (2026-09-08)

---

## Gate Rules

**Hard gate (A–D):** Must pass before any version is tagged or published.
If a section doesn't apply, mark `SKIP:` with justification — don't leave it unchecked.

**Soft gate (E):** Should be done. Product ships without it, but isn't "whole."

**Executed vs attested.** `shipcheck audit` only *counts these checkboxes* — it does not read your repo, so a box can be green while the fact is false. The lines that say **"executed by `npx @mcptoolshop/shipcheck <gate>`"** are backed by a command that reads the real artifact and exits 1 on the real defect. Run those gates; don't just tick their boxes.

**Checking off:**
```
- [x] `[all]` SECURITY.md exists (2026-02-27)
```

**Skipping:**
```
- [ ] `[pypi]` SKIP: not a Python project
```
