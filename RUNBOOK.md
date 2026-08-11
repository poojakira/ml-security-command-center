# Operator Runbook

## Scope

This runbook operates a static portfolio inventory. There is no long-running service, security telemetry, alert queue, or enforcement action.

## Prerequisites

- Python 3.10+
- Git, when revision and dirty-worktree evidence is required
- Portfolio repositories cloned as siblings of this repository

No third-party Python packages are required to generate the inventory.

## Generate

From the repository root:

```bash
python3 generate_metrics.py
python3 -m json.tool metrics.json >/dev/null
```

Expected output states how many configured repositories were observed and how many test function declarations were discovered. It also states that tests were not executed.

## Review before publishing

Inspect `metrics.json` and stop publication when:

- an expected repository has `availability: unavailable`;
- `revision` is null and revision-level traceability is required;
- `working_tree_dirty` is true and the uncommitted state is not intentional;
- a repository was renamed or added but `REPOSITORIES` was not updated;
- the schema is not `portfolio-source-inventory-v2`.

Run each repository's own CI separately before making any statement about passing tests. This inventory cannot supply that evidence.

## Serve locally

```bash
python3 -m http.server 8080
```

Open `http://localhost:8080/`. Do not expose this ad hoc server to an untrusted network; it is only a local file server.

## Validate changes

```bash
python3 -m pytest tests -q
python3 -m compileall -q generate_metrics.py
```

## Failure handling

- Missing repository: clone it beside this repository or accept the explicit `unavailable` result.
- Missing Git executable: source counts still work, but revision and dirty state are null.
- Invalid Python test file: that file is skipped. Repair the syntax and regenerate.
- Browser cannot load JSON: serve the directory over HTTP instead of opening `index.html` through `file://`.

## Rollback

The only generated artifact is `metrics.json`. Restore the prior committed artifact with normal Git history if a generator change is reverted. No database or migration exists.
