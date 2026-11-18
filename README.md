# Big Data Processing Using PySpark

## Project Overview

This project demonstrates a big data processing pipeline using PySpark. It focuses on data ingestion, transformation, Spark optimization, data quality validation, automated testing, schema drift detection, and pipeline monitoring.

The project uses sample customer, product, and order datasets to simulate a retail data processing workflow.

## Technologies Used

- Python
- Apache Spark / PySpark
- SQL and Spark DataFrames
- Parquet
- Pytest
- JSON Schema
- Linux / WSL
- Git and GitHub

## Project Architecture

```text
Raw CSV Data
     |
     v
PySpark Data Ingestion
     |
     v
Data Transformation
     |
     v
Clean Sales Data
     |
     +----------------------+
     |                      |
     v                      v
Spark Optimization     Data Quality Checks
     |                      |
     v                      v
Partitioning,           Flagged Records
Caching, Broadcast      and Quality Report
Joins and AQE
     |
     v
Schema Validation
     |
     v
Schema Drift Detection
     |
     v
Monitoring and Alerts
     |
     v
QA Validation Sign-off
```

## Project Features

### 1. Data Ingestion
- Read customer, product, and order CSV files.
- Apply explicit PySpark schemas.
- Store ingested data in Parquet format.

### 2. Data Transformation
- Clean and validate datasets.
- Join customer, product, and order data.
- Calculate order amounts.
- Generate city-wise and product-wise summaries.

### 3. Spark Optimization
- Data repartitioning.
- Partitioned Parquet storage.
- DataFrame caching and persistence.
- Broadcast joins.
- Adaptive Query Execution (AQE).
- Execution plan inspection.

### 4. Data Quality
- Customer validation.
- Product validation.
- Duplicate order ID checks.
- Quantity and order status validation.
- Referential integrity checks.
- Flagged record storage.
- Data quality reporting.

### 5. Testing
- Unit tests using Pytest.
- Integration tests.
- Code coverage reporting.

### 6. Schema Validation
- JSON Schema validation.
- Schema drift simulation.
- Detection of incompatible data types.

### 7. Monitoring and QA
- Pipeline metrics simulation.
- Critical and warning alerts.
- Evidence-based QA checks.
- QA sign-off report with a release recommendation.

## Project Structure

```text
Big_Data_Processing/
|
|-- data/
|   |-- raw/
|   |-- processed/
|   |-- quality/
|   `-- schema_drift/
|
|-- docs/
|   |-- data_quality_root_cause.md
|   `-- schema_drift_test_case.md
|
|-- schemas/
|   `-- customer_schema.json
|
|-- src/
|   |-- ingestion/
|   |-- transformations/
|   |-- optimization/
|   |-- data_quality/
|   `-- monitoring/
|
|-- tests/
|   |-- test_validators.py
|   `-- test_integration.py
|
|-- reports/
|   |-- data_quality/
|   |-- monitoring/
|   |-- qa/
|   `-- schema_validation/
|
|-- htmlcov/
|-- requirements.txt
`-- README.md
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Big_Data_Processing
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the pipeline scripts

Run the scripts from the project root in this order:

```bash
python src/ingestion/read_data.py
python src/transformations/transform_data.py
python src/optimization/spark_optimization.py
python src/data_quality/quality_checks.py
python src/data_quality/schema_validation.py
python src/monitoring/monitor_pipeline.py
python src/monitoring/qa_signoff.py
```

## Run Tests

```bash
python -m pytest tests/ -v
```

## Generate Coverage Report

```bash
python -m pytest tests/ --cov=src.data_quality.validators --cov-report=term-missing --cov-report=html
```

Open the HTML report:

```bash
explorer.exe htmlcov/index.html
```

## Reports Generated

| Report | Location |
|---|---|
| Data quality report | `reports/data_quality/quality_report/` |
| Schema validation report | `reports/schema_validation/schema_report.json` |
| Monitoring report | `reports/monitoring/monitoring_report.json` |
| QA sign-off report | `reports/qa/qa_signoff.json` |
| Coverage report | `htmlcov/index.html` |

## QA Results

The recorded QA validation completed with:

- Total checks: 14
- Passed checks: 14
- Failed checks: 0
- QA recommendation: PASS
- Simulated pipeline health: FAILED
- Release recommendation: HOLD

**Important:** Monitoring metrics are simulated to demonstrate alert detection. The release HOLD is intentional because the simulation triggers critical data-quality and schema-drift alerts. It does not indicate that the QA tests failed.

## Learning Outcomes

- Building PySpark data processing workflows.
- Applying Spark optimization techniques.
- Implementing data quality validation.
- Writing unit and integration tests.
- Detecting schema drift.
- Generating monitoring alerts and QA reports.

## Future Improvements

- Integrate Apache Airflow for workflow orchestration.
- Use cloud object storage such as Amazon S3.
- Add real-time ingestion with Apache Kafka.
- Implement automated data-quality alert notifications.
- Benchmark performance with larger datasets.
