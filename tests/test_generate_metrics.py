import json
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import generate_metrics


def make_repo(root: Path, name: str, test_source: str = "def test_one():\n    pass\n") -> Path:
    repo = root / name
    tests = repo / "tests"
    tests.mkdir(parents=True)
    (tests / "test_example.py").write_text(test_source, encoding="utf-8")
    return repo


def test_count_test_functions_uses_python_syntax(tmp_path):
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_valid.py").write_text(
        "def test_sync():\n    pass\n\nasync def test_async():\n    pass\n",
        encoding="utf-8",
    )
    (tests / "test_invalid.py").write_text("def test_broken(:\n", encoding="utf-8")
    (tests / "helper.py").write_text("def test_not_collected():\n    pass\n", encoding="utf-8")

    assert generate_metrics.count_test_functions(tests) == 2


def test_missing_repository_is_explicitly_unavailable(tmp_path):
    with patch.object(generate_metrics, "REPOS_DIR", tmp_path):
        record = generate_metrics.collect_repository("missing")

    assert record["availability"] == "unavailable"
    assert record["source"] == "none"
    assert record["test_function_count"] is None
    assert record["revision"] is None


def test_present_repository_reports_static_count_not_passing_tests(tmp_path):
    make_repo(tmp_path, "sample")
    with patch.object(generate_metrics, "REPOS_DIR", tmp_path):
        record = generate_metrics.collect_repository("sample")

    assert record["availability"] == "observed"
    assert record["source"] == "repository_source_snapshot"
    assert record["test_function_count"] == 1
    assert "not executed" in record["observations"][0]["interpretation"]


def test_aws_rule_count_is_labeled_as_declaration_count(tmp_path):
    repo = make_repo(tmp_path, "aws-agent-identity-guard")
    source_dir = repo / "src" / "aws_agent_identity_guard"
    source_dir.mkdir(parents=True)
    (source_dir / "scanner.py").write_text(
        'RULES = ["AIG001", "AIG001", "AIG-T002"]\n', encoding="utf-8"
    )

    with patch.object(generate_metrics, "REPOS_DIR", tmp_path):
        record = generate_metrics.collect_repository("aws-agent-identity-guard")

    assert record["rule_id_count"] == 2
    assert "not a coverage" in record["observations"][1]["interpretation"]


def test_generate_metrics_has_no_baseline_or_effectiveness_fields(tmp_path):
    make_repo(tmp_path, generate_metrics.REPOSITORIES[0])
    with patch.object(generate_metrics, "REPOS_DIR", tmp_path):
        metrics = generate_metrics.generate_metrics()

    assert metrics["schema_version"] == "portfolio-source-inventory-v2"
    assert metrics["classification"] == "static_source_inventory"
    assert metrics["summary"]["repositories_observed"] == 1
    assert metrics["summary"]["repositories_unavailable"] == 10

    forbidden = ("detection_rate", "fp_rate", "uptime", "threats_blocked", "baseline")

    def keys(value):
        if isinstance(value, dict):
            for key, child in value.items():
                yield key
                yield from keys(child)
        elif isinstance(value, list):
            for child in value:
                yield from keys(child)

    assert not set(forbidden).intersection(keys(metrics))


def test_generated_inventory_is_deterministic_except_timestamp(tmp_path):
    for name in generate_metrics.REPOSITORIES:
        make_repo(tmp_path, name)

    with patch.object(generate_metrics, "REPOS_DIR", tmp_path):
        first = generate_metrics.generate_metrics()
        second = generate_metrics.generate_metrics()

    first.pop("generated_at_utc")
    second.pop("generated_at_utc")
    assert first == second


def test_output_is_valid_json():
    data = json.loads(generate_metrics.OUTPUT_PATH.read_text(encoding="utf-8"))
    assert data["schema_version"] == "portfolio-source-inventory-v2"
