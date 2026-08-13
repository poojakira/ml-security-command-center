# Runbook — ML Security Command Center

Step-by-step guide to generate real metrics and view the command center dashboard.

---

## Prerequisites

- Python 3.10+ (`py --version` on Windows, `python3 --version` on Linux)
- pip (bundled with Python)
- Git
- Sibling repos cloned (see Step 2)

---

## Step 1: Install aws-agent-identity-guard

The metrics generator depends on `aws-agent-identity-guard` to count IAM rules.

**Windows (PowerShell):**
```powershell
py -m pip install aws-agent-identity-guard
```

**Linux/macOS:**
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
```

Expected output:
```
Scanning sibling repos...
Found: aws-agent-identity-guard (22 rules)
Found: hf-model-provenance-scanner (XX tests)
...
Wrote metrics.json
```

Verify the output:
```powershell
Get-Content metrics.json | py -m json.tool
```

---

## Step 4: Open index.html in Browser

**Windows (PowerShell):**
```powershell
# Option A: Open directly
Start-Process index.html

# Option B: Serve locally (avoids CORS issues with fetch())
py -m http.server 8080
# Open http://localhost:8080
```

**Linux/macOS:**
```bash
python3 -m http.server 8080
# Open http://localhost:8080
```

The dashboard reads `metrics.json` and displays real portfolio metrics.

---

## Step 5: Verify Metrics Are Real (Not Random)

After loading the dashboard, confirm the data is sourced from `metrics.json`:

1. **Check metrics.json has a recent timestamp:**
   ```powershell
   py -c "import json; d=json.load(open('metrics.json')); print(d.get('generated_at', 'NO TIMESTAMP'))"
   ```

2. **Compare dashboard values to metrics.json:**
   - Rule count should be 22 (from aws-agent-identity-guard)
   - Test counts should match actual `def test_*` functions in sibling repos
   - No values should be suspiciously round or obviously random

3. **Verify no Math.random() in current index.html:**
   ```powershell
   Select-String -Pattern "Math.random" index.html
   # Should return nothing. If it does, the dashboard is showing fake data.
   ```

4. **Check that index.html loads metrics.json:**
   ```powershell
   Select-String -Pattern "metrics.json" index.html
   # Should find a fetch() or XMLHttpRequest call
   ```

---

## Troubleshooting

### generate_metrics.py Fails with ImportError

```
ModuleNotFoundError: No module named 'aws_agent_identity_guard'
```

**Fix:** Install the package (Step 1):
```powershell
py -m pip install aws-agent-identity-guard
```

---

### Metrics Show Zero for Some Repos

The script falls back to last-known values if a repo isn't found. Check:
```powershell
# Verify the sibling directory exists
Test-Path ..\aws-agent-identity-guard
Test-Path ..\adversarial-ml-lab
```

If repos are in a different location, the script expects them as siblings of this directory.

---

### Dashboard Shows "Loading..." or Blank

1. CORS issue — serve with `py -m http.server` instead of opening `file://` directly.
2. Check browser console (F12) for fetch errors.
3. Verify `metrics.json` exists and is valid JSON:
   ```powershell
   py -c "import json; json.load(open('metrics.json')); print('Valid JSON')"
   ```

---

### Dashboard Still Shows Random Data

If `index.html` still uses `Math.random()`:
1. Ensure you're viewing the **root** `index.html`, not `dashboard/index.html`.
2. The `dashboard/index.html` is the old static mockup — it may still have random data.
3. The root `index.html` should fetch from `metrics.json`.

---

## Files Reference

| File | Purpose |
|------|---------|
| `index.html` | Main dashboard — reads metrics.json for real data |
| `generate_metrics.py` | Scans sibling repos, produces metrics.json |
| `metrics.json` | Generated metrics (do not hand-edit) |
| `dashboard/index.html` | Legacy static dashboard (uses simulated data) |
| `SECURITY_AUDIT.md` | Known issues documented |

---

## Known Limitations

- `dashboard/index.html` is the **old** mockup with Math.random() — it still exists for reference
- Root `index.html` is the real dashboard that reads `metrics.json`
- Metrics are point-in-time snapshots — re-run `generate_metrics.py` to refresh
- No auto-refresh or live data pipeline
