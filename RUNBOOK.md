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
pip install aws-agent-identity-guard
```

Verify installation:
```powershell
aws-agent-identity-guard --version
```

---

## Step 2: Ensure Sibling Repos Are Cloned

`generate_metrics.py` reads evidence files and counts tests from sibling repositories. These repos must be cloned in the same parent directory:

```
C:\Users\pooja\repos\
├── ml-security-command-center\    ← you are here
├── aws-agent-identity-guard\
├── hf-model-provenance-scanner\
├── adversarial-ml-lab\
├── dataset-poisoning-detector\
├── llm-redteam-framework\
├── model-privacy-attacks\
├── attack-v19-core\
├── mcp-security-gateway-monitor\
├── unified-ml-security-platform\
├── PulseNet-RUL-Forecasting\  [ARCHIVED — not an active security product]
└── mlsec-benchmark-suite\
```

**Clone any missing repos:**
```powershell
cd C:\Users\pooja\repos
git clone https://github.com/poojakira/aws-agent-identity-guard.git
git clone https://github.com/poojakira/hf-model-provenance-scanner.git
git clone https://github.com/poojakira/adversarial-ml-lab.git
# ... etc for any missing repos
```

---

## Step 3: Run generate_metrics.py

This script scans sibling repos and produces `metrics.json` with real data.

**Windows (PowerShell):**
```powershell
cd C:\Users\pooja\repos\ml-security-command-center
py generate_metrics.py
```

**Linux/macOS:**
```bash
cd ~/repos/ml-security-command-center
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
