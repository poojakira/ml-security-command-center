# ML Security Command Center

Portfolio metrics dashboard that pulls real data from all ML security tools. Generates a `metrics.json` artifact by scanning sibling repository directories for evidence files, test counts, and rule counts, then displays them in an interactive HTML dashboard.

## Install

```powershell
git clone https://github.com/poojakira/ml-security-command-center.git
cd ml-security-command-center
py -m pip install aws-agent-identity-guard
```

## Generate Metrics

```powershell
py generate_metrics.py
# This reads real data from sibling repo directories
```

The script scans sibling repositories for:
- Evidence JSON artifacts
- Test function counts (`def test_*` in test files)
- Rule IDs in scanner source code
- Results from benchmark runs

Output is written to `metrics.json` in the project root.

## View Dashboard

```powershell
start index.html
```

On Mac/Linux:
```bash
open index.html
```

## Metrics Displayed

- **aws-agent-identity-guard**: Rule count, false-positive rate, test count
- **hf-model-provenance-scanner**: Scan results, detection metrics
- **mcp-security-gateway-monitor**: Detection rate
- **llm-redteam-framework**: F1 score, OOD performance
- **model-privacy-attacks**: Attack success metrics
- **adversarial-ml-lab**: Attack/defense evaluation results
- **PulseNet-RUL-Forecasting**: Prediction metrics
- **dataset-poisoning-detector**: AUC scores

All metrics link back to committed evidence files. Synthetic or unavailable data is clearly labeled.
