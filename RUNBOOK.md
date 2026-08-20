# RUNBOOK — ml-security-command-center

## Overview
Python script that aggregates test/rule counts across repos and renders an HTML dashboard.

## Install
```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

## Run Aggregation
```bash
python aggregate.py --config repos.yaml
```
This scans configured repos, counts tests and security rules, and writes results to `data/counts.json`.

## View Dashboard
```bash
python render.py
# Opens or generates dashboard at output/dashboard.html
start output/dashboard.html   # Windows
```

## Customize
- **Add a repo**: Edit `repos.yaml`, add entry with path and rule glob pattern.
- **Change output format**: Edit `templates/dashboard.html` (Jinja2 template).
- **Adjust rule patterns**: Modify `config.yaml` regex under `rule_patterns`.
- **Schedule runs**: Use cron/Task Scheduler to run `aggregate.py` periodically.

## Troubleshooting
- **Repo not found**: Verify paths in `repos.yaml` are absolute or relative to project root.
- **Zero counts**: Check that glob patterns match actual test/rule file names.
- **Template errors**: Validate Jinja2 syntax in `templates/` directory.
