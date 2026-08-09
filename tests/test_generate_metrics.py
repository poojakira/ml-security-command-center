"""
test_generate_metrics.py — Verify generate_metrics.py produces deterministic,
real (non-random) metrics.json from committed baseline values.

Runs in isolation: temporarily renames the parent directory so no sibling repos
are found, forcing baseline fallback mode. Asserts all values are deterministic
and match expected baseline numbers.
"""

import json
import sys
from pathlib import Path
from unittest.mock import patch

# Add parent to path so we can import generate_metrics
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import generate_metrics


def test_baseline_loads_successfully():
    """metrics_baseline.json exists and parses correctly."""
    baseline = generate_metrics.load_baseline()
    assert isinstance(baseline, dict)
    assert len(baseline) > 0, "Baseline should have product entries"
    assert "aws-agent-identity-guard" in baseline
    assert "hf-model-provenance-scanner" in baseline


def test_generate_metrics_produces_valid_schema():
    """generate_metrics() returns a dict with required schema fields."""
    metrics = generate_metrics.generate_metrics()
    assert metrics["schema_version"] == "command-center-metrics-v1"
    assert "generated_at_utc" in metrics
    assert metrics["generator"] == "generate_metrics.py"
    assert "summary" in metrics
    assert "products" in metrics


def test_metrics_have_no_random_values():
    """Run generate_metrics() twice — results must be identical (except timestamp)."""
    m1 = generate_metrics.generate_metrics()
    m2 = generate_metrics.generate_metrics()

    # Remove timestamps for comparison
    m1.pop("generated_at_utc")
    m2.pop("generated_at_utc")

    assert m1 == m2, "Metrics should be deterministic (no random values)"


def test_all_products_have_test_count():
    """Every product entry must have a positive test_count."""
    metrics = generate_metrics.generate_metrics()
    products = metrics["products"]
    for name, data in products.items():
        assert "test_count" in data, f"{name} missing test_count"
        assert isinstance(data["test_count"], int), f"{name} test_count not int"
        assert data["test_count"] > 0, f"{name} has test_count=0, should have baseline value"


def test_all_products_have_source():
    """Every product entry must declare its data source."""
    metrics = generate_metrics.generate_metrics()
    products = metrics["products"]
    for name, data in products.items():
        assert "source" in data, f"{name} missing source field"
        assert data["source"] in ("live", "baseline"), f"{name} has unexpected source: {data['source']}"


def test_summary_totals_consistent():
    """Summary total_test_functions equals sum of individual test_counts."""
    metrics = generate_metrics.generate_metrics()
    total_from_summary = metrics["summary"]["total_test_functions"]
    total_from_products = sum(
        p["test_count"] for p in metrics["products"].values()
    )
    assert total_from_summary == total_from_products, (
        f"Summary says {total_from_summary} but product sum is {total_from_products}"
    )


def test_aws_guard_has_rule_count():
    """aws-agent-identity-guard must report rule_count >= 22."""
    metrics = generate_metrics.generate_metrics()
    aws = metrics["products"]["aws-agent-identity-guard"]
    assert aws["rule_count"] >= 22, f"Expected >= 22 rules, got {aws['rule_count']}"


def test_hf_scanner_has_detection_metrics():
    """hf-model-provenance-scanner must report FP rate and detection rate."""
    metrics = generate_metrics.generate_metrics()
    hf = metrics["products"]["hf-model-provenance-scanner"]
    assert "fp_rate" in hf
    assert hf["fp_rate"] == 5.9
    assert hf["detection_rate"] == 100.0


def test_mcp_gateway_has_performance_metrics():
    """mcp-security-gateway-monitor must report latency and detection."""
    metrics = generate_metrics.generate_metrics()
    mcp = metrics["products"]["mcp-security-gateway-monitor"]
    assert mcp["layers"] == 5
    assert mcp["p95_latency_ms"] == 0.129
    assert mcp["detection_rate"] == 51.0


def test_baseline_fallback_when_repos_missing():
    """When no sibling repos exist, baseline values are used (source='baseline')."""
    # Patch REPOS_DIR to a nonexistent path
    fake_repos = Path("C:/nonexistent_path_for_testing_12345")
    with patch.object(generate_metrics, "REPOS_DIR", fake_repos):
        metrics = generate_metrics.generate_metrics()

    products = metrics["products"]
    # All should be "baseline" source since no repos found
    for name, data in products.items():
        assert data["source"] == "baseline", (
            f"{name} should use baseline when repos missing, got source={data['source']}"
        )
    # Values should still be real (from baseline file)
    assert products["aws-agent-identity-guard"]["rule_count"] == 25
    assert products["hf-model-provenance-scanner"]["test_count"] == 202
    assert products["mcp-security-gateway-monitor"]["test_count"] == 511


def test_no_zero_test_counts_in_baseline_mode():
    """In baseline mode, no product should have test_count=0."""
    fake_repos = Path("C:/nonexistent_path_for_testing_12345")
    with patch.object(generate_metrics, "REPOS_DIR", fake_repos):
        metrics = generate_metrics.generate_metrics()

    for name, data in metrics["products"].items():
        assert data["test_count"] > 0, (
            f"{name} has test_count=0 in baseline mode — baseline file may be incomplete"
        )


def test_metrics_json_is_valid_json():
    """The output metrics.json file must be valid JSON."""
    output_path = generate_metrics.SCRIPT_DIR / "metrics.json"
    if output_path.exists():
        content = output_path.read_text(encoding="utf-8")
        data = json.loads(content)  # Should not raise
        assert data["schema_version"] == "command-center-metrics-v1"
