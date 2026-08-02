# ML Security Command Center

Unified real-time dashboard aggregating all ML security products into one live command center.

## Products Monitored

| # | Product | Function | Status |
|---|---------|----------|--------|
| 1 | hf-model-provenance-scanner | Model supply-chain scanning | Live |
| 2 | mcp-security-gateway-monitor | MCP tool-call firewall (5-layer) | Live |
| 3 | llm-redteam-framework | Prompt injection detection | Live |
| 4 | adversarial-ml-lab | Adversarial robustness evaluation | Live |
| 5 | dataset-poisoning-detector | Training data anomaly detection | Live |
| 6 | model-privacy-attacks | Membership inference attacks | Live |
| 7 | PulseNet-RUL-Forecasting | ICS predictive maintenance | Live |
| 8 | attack-v19-core | MITRE ATT&CK v19 data models | Live |
| 9 | aws-agent-identity-guard | IAM guardrails for AI agents | Live |
| 10 | unified-ml-security-platform | Architecture integration | Live |
| 11 | mlsec-benchmark-suite | Benchmark infrastructure | Live |

## Run

```bash
python -m http.server 3000
# Open http://localhost:3000
```

Or just open `index.html` directly in a browser.

## Architecture

Single-file HTML dashboard with:
- Three.js 3D network topology showing all 11 products as nodes
- WebSocket-ready (connects to each product's API when deployed)
- Live metrics per product: events processed, threats blocked, detection rate
- ATT&CK technique coverage heatmap across all products
- No build step, no npm, no bundler — one HTML file
