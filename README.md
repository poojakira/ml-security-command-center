# ml-security-command-center

Single-script metrics aggregator that scans 11 sibling repositories, counts test functions and rule definitions via AST analysis, records Git revisions, and renders a static HTML dashboard.

## What It Does

`generate_metrics.py` walks each sibling repo and:
1. Counts `test_*` function declarations via Python AST parsing
2. Extracts rule IDs from scanner source (where applicable)
3. Records Git SHA + dirty-tree status
4. Writes structured results to `metrics.json`
5. Renders `index.html` with the aggregated snapshot

## Output (metrics.json)

```json
{
  "summary": {
    "repositories_configured": 11,
    "repositories_observed": 11,
    "test_functions_discovered": 1304
  },
  "products": {
    "mcp-agent-security-gateway": { "test_function_count": 527 },
    "hf-model-provenance-scanner": { "test_function_count": 204 },
    "aws-agent-identity-guard": { "test_function_count": 106, "rule_id_count": 25 },
    "attack-v19-core": { "test_function_count": 104 },
    ...
  }
}
```

## Usage

```bash
# No dependencies required — stdlib only
python generate_metrics.py

# Outputs:
#   metrics.json   — structured data (schema: portfolio-source-inventory-v2)
#   index.html     — static HTML report, open in browser
```

## Portfolio Numbers

| Repo                          | Tests | Rules |
|-------------------------------|-------|-------|
| mcp-agent-security-gateway    | 527   | —     |
| hf-model-provenance-scanner   | 204   | —     |
| aws-agent-identity-guard      | 106   | 25    |
| attack-v19-core               | 104   | —     |
| PulseNet-RUL-Forecasting      | 148   | —     |
| llm-redteam-framework         | 69    | —     |
| dataset-poisoning-detector    | 55    | —     |
| adversarial-ml-lab            | 33    | —     |
| mlsec-benchmark-suite         | 28    | —     |
| model-privacy-attacks         | 18    | —     |
| unified-ml-security-platform  | 12    | —     |
| **Total**                     |**1304**| **25** |

## Structure

```
generate_metrics.py    Aggregator script (zero external dependencies)
metrics.json           Latest output snapshot
index.html             Static HTML dashboard
tests/                 Tests for the generator itself
```

## Design Decisions

- Zero dependencies: uses only Python stdlib (ast, json, subprocess for git)
- Does not execute any tests — only counts declarations
- Schema-versioned output (`portfolio-source-inventory-v2`)
- Explicit limitations documented in output JSON

## License

MIT
