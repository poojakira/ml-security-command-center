# ML Security Command Center

Real-time metrics dashboard for the ML security tool portfolio. Displays actual rule counts, test results, false-positive rates, and detection scores collected from live tool outputs — not random numbers.

## Quick Start

```bash
# Generate metrics from local repos
py generate_metrics.py

# View dashboard
start index.html
# or serve it:
py -m http.server 3000
```

## How It Works

`generate_metrics.py` scans sibling repos and extracts real data:

| Source | What's Extracted |
|--------|-----------------|
| `aws-agent-identity-guard/src/` | Rule count (22 IAM policy rules) |
| `aws-agent-identity-guard/tests/` | Test function count (63 tests) |
| `hf-model-provenance-scanner/evidence/` | FP rate (5.9%), detection rate, red team results |
| `hf-model-provenance-scanner/tests/` | Test function count (130 tests) |
| `mcp-security-gateway-monitor/evidence/` | P95 latency, replay iterations |
| `mcp-security-gateway-monitor/tests/` | Test function count (476 tests) |
| Other repos `/tests/` | Test function counts |

The script writes `metrics.json`, which `index.html` loads at runtime. No Math.random(). No fake backends.

## What's Displayed

- **Header stats**: Total IAM rules, total tests passing, ATT&CK technique coverage
- **3D graph**: Products as nodes, sized by test count, connected to central hub
- **Product cards**: Per-repo metrics (tests, detection rates, FP rates, F1 scores)
- **ATT&CK grid**: Technique coverage across all tools
- **Evidence summary**: Key findings from evidence JSON artifacts

## Files

| File | Purpose |
|------|---------|
| `generate_metrics.py` | Collects real metrics from sibling repos → `metrics.json` |
| `metrics.json` | Generated data file (not committed, regenerate locally) |
| `index.html` | Dashboard (Three.js 3D visualization + metric cards) |
| `dashboard/index.html` | Legacy flat layout (still uses old mock data) |

## Metrics Are Real

All values come from:
- Committed evidence JSON artifacts (FP rates, red team reports, replay benchmarks)
- Counted `def test_*` functions in actual test files
- Rule IDs extracted from actual scanner source code

If a repo isn't available locally, the script falls back to last-known documented values and marks the source as "fallback" in the JSON.

## Regenerating

Run `py generate_metrics.py` whenever you want fresh numbers. The dashboard reads `metrics.json` on page load.

## Requirements

- Python 3.10+ (no pip dependencies needed)
- Sibling repos checked out at `../` relative to this repo
