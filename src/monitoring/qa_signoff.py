
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parents[2]

def load_json(relative_path):
    path = PROJECT_ROOT / relative_path
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)

print("Starting Evidence-Based QA Validation")

# Check that important project outputs exist
required_paths = [
    "data/processed/customers",
    "data/processed/products",
    "data/processed/orders",
    "data/processed/clean_sales",
    "data/processed/partitioned_sales",
    "reports/data_quality/quality_report",
    "reports/monitoring/monitoring_report.json",
    "reports/schema_validation/schema_report.json",
    "htmlcov/index.html"
]

checks = {
    f"output_exists_{Path(path).name}": (PROJECT_ROOT / path).exists()
    for path in required_paths
}

# Run the actual unit and integration tests
test_result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/", "-q"],
    cwd=PROJECT_ROOT,
    capture_output=True,
    text=True
)
checks["unit_and_integration_tests"] = test_result.returncode == 0

# Check schema validation evidence
schema_report = load_json("reports/schema_validation/schema_report.json")
checks["valid_schema_record_passed"] = (
    schema_report.get("valid_customer") == "PASS"
)
checks["schema_drift_was_detected"] = (
    schema_report.get("drift_customer") == "FAIL"
)

# Check monitoring alert simulation
monitoring_report = load_json(
    "reports/monitoring/monitoring_report.json"
)

alerts = monitoring_report.get("alerts", [])
checks["data_quality_alert_generated"] = any(
    "CRITICAL: Data quality checks failed" in alert
    for alert in alerts
)
checks["schema_drift_alert_generated"] = any(
    "CRITICAL: Schema drift detected" in alert
    for alert in alerts
)

# Calculate QA result
passed = sum(checks.values())
total = len(checks)
failed = total - passed

qa_recommendation = "PASS" if failed == 0 else "FAIL"

# The monitoring report is intentionally unhealthy for this simulation.
pipeline_status = monitoring_report.get("pipeline_status", "UNKNOWN")
release_recommendation = (
    "HOLD - simulated pipeline has critical alerts"
    if pipeline_status == "FAILED"
    else "REVIEW - check pipeline health"
)

qa_report = {
    "project": "Big_Data_Processing",
    "signoff_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "total_checks": total,
    "passed_checks": passed,
    "failed_checks": failed,
    "qa_recommendation": qa_recommendation,
    "simulated_pipeline_health": pipeline_status,
    "release_recommendation": release_recommendation,
    "checks": checks,
    "test_output": test_result.stdout.strip(),
    "note": (
        "Monitoring metrics are simulated. Critical alerts are "
        "deliberately triggered to test alert detection."
    )
}

report_dir = PROJECT_ROOT / "reports" / "qa"
report_dir.mkdir(parents=True, exist_ok=True)

report_path = report_dir / "qa_signoff.json"
with report_path.open("w", encoding="utf-8") as file:
    json.dump(qa_report, file, indent=4)

print("\nFINAL QA SUMMARY")
print("Total checks:", total)
print("Passed:", passed)
print("Failed:", failed)
print("QA recommendation:", qa_recommendation)
print("Simulated pipeline health:", pipeline_status)
print("Release recommendation:", release_recommendation)

if failed:
    print("\nFailed checks:")
    for name, result in checks.items():
        if not result:
            print("-", name)

print("\nQA sign-off report saved:", report_path)
