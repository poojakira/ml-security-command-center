"""Build a traceable, point-in-time inventory of sibling repositories.

This collector intentionally does not report security effectiveness, passing test
counts, uptime, alerts, or deployment status. It performs static source inspection
and records the Git revision so readers can reproduce the observations.
"""

from __future__ import annotations

import ast
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPOS_DIR = SCRIPT_DIR.parent
OUTPUT_PATH = SCRIPT_DIR / "metrics.json"

REPOSITORIES = (
    "adversarial-ml-lab",
    "attack-v19-core",
    "aws-agent-identity-guard",
    "dataset-poisoning-detector",
    "hf-model-provenance-scanner",
    "llm-redteam-framework",
    "mcp-agent-security-gateway",
    "mlsec-benchmark-suite",
    "model-privacy-attacks",
    "PulseNet-RUL-Forecasting",
    "unified-ml-security-platform",
)


def count_test_functions(test_dir: Path) -> int:
    """Count Python test function declarations without executing them."""
    count = 0
    if not test_dir.is_dir():
        return count

    for path in test_dir.rglob("test_*.py"):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, SyntaxError, UnicodeError):
            continue
        count += sum(
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
            for node in ast.walk(tree)
        )
    return count


def count_aws_rule_ids(repo: Path) -> int | None:
    """Count unique AIG rule identifiers declared in scanner source files."""
    source_dir = repo / "src" / "aws_agent_identity_guard"
    if not source_dir.is_dir():
        return None

    rule_ids: set[str] = set()
    for path in source_dir.rglob("*.py"):
        try:
            source = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        rule_ids.update(re.findall(r'\bAIG(?:-|)[A-Z0-9]*\d{3}\b', source))
    return len(rule_ids)


def run_git(repo: Path, *args: str) -> str | None:
    """Run a read-only Git query and return stripped output when successful."""
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def collect_repository(repo_name: str) -> dict:
    """Collect reproducible static observations for one sibling repository."""
    repo = REPOS_DIR / repo_name
    if not repo.is_dir():
        return {
            "availability": "unavailable",
            "source": "none",
            "revision": None,
            "working_tree_dirty": None,
            "test_function_count": None,
            "observations": [],
        }

    revision = run_git(repo, "rev-parse", "HEAD")
    status = run_git(repo, "status", "--porcelain")
    test_count = count_test_functions(repo / "tests")
    observations = [
        {
            "name": "test_function_count",
            "value": test_count,
            "method": "AST count of test_* function declarations under tests/",
            "interpretation": "Static source count only; tests were not executed.",
        }
    ]

    record = {
        "availability": "observed",
        "source": "repository_source_snapshot",
        "revision": revision,
        "working_tree_dirty": bool(status) if status is not None else None,
        "test_function_count": test_count,
        "observations": observations,
    }

    if repo_name == "aws-agent-identity-guard":
        rule_count = count_aws_rule_ids(repo)
        record["rule_id_count"] = rule_count
        observations.append(
            {
                "name": "rule_id_count",
                "value": rule_count,
                "method": "Unique AIG rule identifiers found in scanner Python source",
                "interpretation": "Declared rule IDs only; not a coverage or effectiveness claim.",
            }
        )

    return record


def generate_metrics() -> dict:
    """Return the complete point-in-time portfolio inventory."""
    products = {name: collect_repository(name) for name in REPOSITORIES}
    observed = [p for p in products.values() if p["availability"] == "observed"]
    return {
        "schema_version": "portfolio-source-inventory-v2",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "generator": "generate_metrics.py",
        "classification": "static_source_inventory",
        "limitations": [
            "No tests are executed by this collector.",
            "Source counts do not measure security effectiveness or production readiness.",
            "No runtime telemetry, uptime, alert, customer, or deployment data is collected.",
            "A dirty sibling worktree means observations may not match its recorded revision.",
        ],
        "summary": {
            "repositories_configured": len(REPOSITORIES),
            "repositories_observed": len(observed),
            "repositories_unavailable": len(REPOSITORIES) - len(observed),
            "test_functions_discovered": sum(
                p["test_function_count"] or 0 for p in observed
            ),
        },
        "products": products,
    }


def main() -> None:
    metrics = generate_metrics()
    OUTPUT_PATH.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    summary = metrics["summary"]
    print(f"Wrote {OUTPUT_PATH}")
    print(
        "Observed "
        f"{summary['repositories_observed']}/{summary['repositories_configured']} "
        "configured repositories; "
        f"{summary['test_functions_discovered']} test declarations found."
    )


if __name__ == "__main__":
    main()
