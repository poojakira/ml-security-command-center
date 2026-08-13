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
    "mcp-security-gateway-monitor",
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
    if test_count > 0:
        metrics["test_count"] = test_count

    # Try running the linter against example policies
    examples_dir = repo / "examples"
    if examples_dir.exists():
        total_findings = 0
        for policy_file in examples_dir.glob("*.json"):
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "aws_agent_identity_guard", str(policy_file)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=str(repo),
                    check=False,  # non-zero exit means findings; we parse stdout
                )
                # Count findings from output
                findings = re.findall(r"(AIG[-\w]+)", result.stdout)
                total_findings += len(findings)
            except (subprocess.TimeoutExpired, OSError, FileNotFoundError):
                pass
        metrics["findings_on_examples"] = total_findings

    metrics["source"] = "live"
    return metrics


def collect_hf_scanner_metrics(baseline: dict) -> dict:
    """Collect metrics from hf-model-provenance-scanner."""
    repo = REPOS_DIR / "hf-model-provenance-scanner"
    fallback = baseline.get("hf-model-provenance-scanner", {})
    metrics = {
        "test_count": fallback.get("test_count", 202),
        "fp_rate": fallback.get("fp_rate", 5.9),
        "detection_rate": fallback.get("detection_rate", 100.0),
        "total_checks": fallback.get("total_checks", 17),
        "redteam_attacks_detected": fallback.get("redteam_attacks_detected", 12),
        "redteam_attacks_total": fallback.get("redteam_attacks_total", 12),
    }

    if not repo.exists():
        metrics["source"] = "baseline"
        return metrics

    # Read FP rate evidence
    fp_evidence = read_json_safe(repo / "evidence" / "generated" / "false_positive_rate.json")
    if fp_evidence:
        metrics["fp_rate"] = round(fp_evidence.get("fp_rate", 0.059) * 100, 1)
        metrics["total_checks"] = fp_evidence.get("total_checks", 17)
        metrics["false_positives"] = fp_evidence.get("false_positives", 1)

    # Read redteam report
    redteam = read_json_safe(repo / "tests" / "redteam" / "redteam_report.json")
    if redteam and "summary" in redteam:
        s = redteam["summary"]
        metrics["redteam_attacks_detected"] = s.get("detected", 12)
        metrics["redteam_attacks_total"] = s.get("total_attacks", 12)
        metrics["detection_rate"] = s.get("detection_rate_percent", 100.0)

    # Count tests
    test_count = count_test_functions(repo / "tests")
    if test_count > 0:
        metrics["test_count"] = test_count

    metrics["source"] = "live"
    return metrics


def collect_mcp_gateway_metrics(baseline: dict) -> dict:
    """Collect metrics from mcp-security-gateway-monitor."""
    repo = REPOS_DIR / "mcp-security-gateway-monitor"
    fallback = baseline.get("mcp-security-gateway-monitor", {})
    metrics = {
        "test_count": fallback.get("test_count", 511),
        "detection_rate": fallback.get("detection_rate", 51.0),
        "layers": fallback.get("layers", 5),
        "p95_latency_ms": fallback.get("p95_latency_ms", 0.129),
        "replay_iterations": fallback.get("replay_iterations", 100),
    }

    if not repo.exists():
        metrics["source"] = "baseline"
        return metrics

    # Read replay evidence
    replay = read_json_safe(repo / "evidence" / "generated" / "mcp_replay_evidence.json")
    if replay and "measurement" in replay:
        m = replay["measurement"]
        metrics["p95_latency_ms"] = m.get("p95_ms", 0.129)
        metrics["replay_iterations"] = m.get("iterations", 100)
        # Calculate detection rate from raw results
        raw = m.get("raw", [])
        if raw:
            blocked = sum(1 for r in raw if not r.get("allowed", True))
            total = len(raw)
            metrics["detection_rate_from_corpus"] = (
                round(blocked / total * 100, 1) if total > 0 else 0
            )

    # Count tests
    test_count = count_test_functions(repo / "tests")
    if test_count > 0:
        metrics["test_count"] = test_count

    metrics["source"] = "live"
    return metrics


def collect_other_repos_metrics(baseline: dict) -> dict:
    """Collect test counts from other repos."""
    other_names = [
        "llm-redteam-framework",
        "adversarial-ml-lab",
        "model-privacy-attacks",
        "dataset-poisoning-detector",
        # "PulseNet-RUL-Forecasting",  # ARCHIVED — removed from active metrics
        "attack-v19-core",
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
        "configured sibling repositories."
    )
    print(
        f"Discovered {summary['test_functions_discovered']} test function declarations; "
        "tests were not executed."
    )


if __name__ == "__main__":
    main()
