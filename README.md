# ML Security Command Center

[![Live Dashboard](https://img.shields.io/badge/Live_Dashboard-View-blue)](https://poojakira.github.io/ml-security-command-center/)

A single-page HTML dashboard that displays all 11 ML security projects in one view. It shows a 3D network graph of the products, their descriptions, and a MITRE ATT&CK technique coverage grid.

**This is a static HTML page with simulated data.** The metrics (events/min, threats blocked, detection rates) are randomly generated in JavaScript — nothing connects to real services. The "Live" indicators and activity feed are cosmetic animations, not real-time data.

## What's in it

- `index.html` — Main dashboard (Three.js 3D node graph + product cards + ATT&CK grid)
- `dashboard/index.html` — Alternative flat dashboard layout

Both files are self-contained HTML with inline CSS/JS. No build step, no dependencies to install.

## How to use it

**Option A: Just open the file**

Double-click `index.html` in your file explorer. It opens in any modern browser.

**Option B: Serve it locally** (needed if the browser blocks CDN scripts from a `file://` URL)

```bash
cd ml-security-command-center
python -m http.server 3000
# Then open http://localhost:3000
```

## Products shown

The dashboard lists these 11 repositories as nodes:

1. hf-model-provenance-scanner — Model supply-chain scanning
2. mcp-security-gateway-monitor — MCP tool-call firewall
3. llm-redteam-framework — Prompt injection detection
4. adversarial-ml-lab — Adversarial robustness evaluation
5. dataset-poisoning-detector — Training data anomaly detection
6. model-privacy-attacks — Membership inference attacks
7. PulseNet-RUL-Forecasting — ICS predictive maintenance
8. attack-v19-core — MITRE ATT&CK v19 data models
9. aws-agent-identity-guard — IAM guardrails for AI agents
10. unified-ml-security-platform — Architecture integration
11. mlsec-benchmark-suite — Benchmark infrastructure

## Limitations

- All numbers on the dashboard are fake (randomly generated on page load and updated with `Math.random()` every few seconds).
- There are no WebSocket connections or API calls to real backends.
- The ATT&CK coverage grid is hardcoded, not computed from actual detection results.
- This is a visualization/portfolio piece, not an operational monitoring tool.
