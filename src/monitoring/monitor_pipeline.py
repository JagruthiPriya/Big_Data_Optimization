import json
import os
from datetime import datetime

print("Starting Pipeline Monitoring")

# Simulated pipeline metrics
metrics = {
    "pipeline_name": "Big_Data_Processing",
    "execution_date": datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    ),
    "records_processed": 15,
    "records_validated": 10,
    "records_rejected": 5,
    "execution_time_seconds": 12.5,
    "data_quality_failures": 4,
    "schema_drift_detected": True
}

# Alert rules
alerts = []

if metrics["records_rejected"] > 0:
    alerts.append(
        "WARNING: Invalid records detected"
    )

if metrics["data_quality_failures"] > 0:
    alerts.append(
        "CRITICAL: Data quality checks failed"
    )

if metrics["schema_drift_detected"]:
    alerts.append(
        "CRITICAL: Schema drift detected"
    )

if metrics["execution_time_seconds"] > 30:
    alerts.append(
        "WARNING: Pipeline execution is slow"
    )

# Monitoring status
if any("CRITICAL" in alert for alert in alerts):
    status = "FAILED"
elif alerts:
    status = "WARNING"
else:
    status = "HEALTHY"

monitoring_report = {
    "metrics": metrics,
    "alerts": alerts,
    "pipeline_status": status
}

# Save monitoring report
os.makedirs("reports/monitoring", exist_ok=True)

with open(
    "reports/monitoring/monitoring_report.json",
    "w"
) as file:
    json.dump(
        monitoring_report,
        file,
        indent=4
    )

print("\nPIPELINE MONITORING RESULTS")

print("Records processed:", metrics["records_processed"])
print("Records validated:", metrics["records_validated"])
print("Records rejected:", metrics["records_rejected"])

print("\nALERTS")

for alert in alerts:
    print(alert)

print("\nPipeline Status:", status)

print("\nMonitoring report saved")
print("Pipeline Monitoring Completed")
