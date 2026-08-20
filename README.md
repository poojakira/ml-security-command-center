# ml-security-command-center

Static metrics aggregator. A single Python script that scans sibling repos, counts tests and rules, records Git revisions, and renders a static HTML report.

## What It Does

`generate_metrics.py` walks the portfolio repos, extracts counts (test files, rule definitions, Git SHAs), writes them to `metrics.json`, and updates `index.html` with the results.

## What It Is Not

This is not a monitoring service, SIEM, or live dashboard. It produces a point-in-time snapshot as a static HTML file.

## Usage

```bash
python generate_metrics.py
# Outputs: metrics.json, index.html
```

## Structure

```
generate_metrics.py   - Script that collects metrics
metrics.json          - Output data
index.html            - Static HTML report
tests/                - Tests for the metrics generator
```

## Status

Simple utility script. Zero external dependencies.
