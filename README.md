# ML Security Portfolio Inventory

This repository builds a point-in-time inventory of Pooja Kiran's sibling ML security repositories. It counts test function declarations and selected rule identifiers from source, records each repository's Git revision, and renders those observations in a static HTML report.

This is **not** a security command center, monitoring service, benchmark, or production control. It has no telemetry ingestion, backend, authentication, alerting, enforcement, or runtime health data. A source count does not establish that tests pass or that a security control is effective.

## Generate the inventory

Requirements: Python 3.10+ and Git. There are no runtime Python package dependencies.

Clone the portfolio repositories as siblings:

```text
portfolio/
├── ml-security-command-center/
├── aws-agent-identity-guard/
├── hf-model-provenance-scanner/
└── ...
```

Then run:

```bash
cd ml-security-command-center
python3 generate_metrics.py
```

The script writes `metrics.json`. Missing repositories are recorded as `unavailable`; the generator never substitutes historical or invented values.

## View the report

Serve the directory so the browser can load `metrics.json`:

```bash
python3 -m http.server 8080
```

Open `http://localhost:8080/`. The page is a static inventory, not an operations interface.

## Verify

```bash
python3 -m pytest tests -q
python3 -m compileall -q generate_metrics.py
```

CI runs linting, tests, and a clean inventory generation. The generated `metrics.json` records source observations only; test execution must be verified in each repository's own CI and reproducible test artifacts.

## Data contract

Each observed repository includes:

- `revision`: Git commit inspected by the generator.
- `working_tree_dirty`: whether uncommitted files could differ from that revision.
- `test_function_count`: static AST count under `tests/`, not a passing-test count.
- `observations`: method and interpretation for every reported source count.

No detection rate, false-positive rate, latency, uptime, deployment, customer, alert, or attack-blocking claim is produced.

## Status and limitations

Status: **repositioned static portfolio component; not production-ready**.

- The configured inventory is curated in `generate_metrics.py`.
- Only Python `test_*` declarations are counted.
- Repository presence and source structure are observed; behavior is not validated.
- A dirty worktree weakens revision-level reproducibility and is shown explicitly.
- See `RUNBOOK.md`, `SECURITY.md`, and `SECURITY_AUDIT.md` for operation and boundaries.
