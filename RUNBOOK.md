# Runbook — ML Security Command Center

## What This Is

A static HTML dashboard showing all ML security products in one view. There is no backend, no database, no server — just HTML files you open in a browser.

## How to Use

### Option 1: Open directly

Double-click `index.html` or `dashboard/index.html` in your file explorer. It opens in your default browser.

### Option 2: Serve locally (avoids file:// CORS issues)

```bash
cd ml-security-command-center
python -m http.server 8080
# Open http://localhost:8080
```

### Option 3: View the hosted version

Visit: https://poojakira.github.io/mlsec-dashboards/ml-security-command-center/

## What's Real and What's Not

- The product list is real — those repos exist
- All numbers on the dashboard are **fake** (generated with Math.random())
- Status indicators are cosmetic animations, not live connections
- There is no API, no data pipeline, no monitoring

## Files

| File | Purpose |
|------|---------|
| `index.html` | 3D visualization landing page |
| `dashboard/index.html` | Product status grid (simulated) |
| `README.md` | This repo's documentation |

## Known Limitations

- Zero source code — this is purely a visualization
- No CI/CD pipeline
- No tests
- Not a substitute for actual monitoring tooling
