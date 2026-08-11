# Security Policy

## Supported scope

The current repository is a static source-inventory generator and HTML report. It has no supported hosted service or API. Security fixes are applied to the latest `main` branch only.

## Report a vulnerability

Use GitHub's private vulnerability reporting feature if it is enabled. If it is unavailable, open a minimal public issue requesting a private contact channel and omit vulnerability details. Do not include credentials, private repository contents, customer data, or exploit payloads in a public issue.

Include the affected commit, reproduction steps, expected impact, and any suggested mitigation. No response-time or remediation-time guarantee is claimed.

## Security boundaries

- The generator reads sibling repository source and Git metadata.
- It does not execute sibling test suites or repository code.
- It writes only `metrics.json` in this repository.
- The HTML report reads that local JSON file and has no backend.
- `python3 -m http.server` is for local inspection only and is not a hardened deployment.

See `SECURITY_AUDIT.md` for known limitations and the current readiness decision.
