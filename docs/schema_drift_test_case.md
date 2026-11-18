# Schema Drift Test Case

## 1. Objective

Verify that the data pipeline detects schema changes and prevents records that do not match the expected customer schema from passing validation.

## 2. Expected Customer Schema

| Field | Expected Data Type |
|---|---|
| customer_id | Integer |
| customer_name | String |
| age | Integer |
| city | String |
| email | String |

All five fields are required. Additional properties are not allowed.

## 3. Test Scenarios

### Scenario 1: Valid Customer Record

Input:

```json
{
  "customer_id": 101,
  "customer_name": "John Smith",
  "age": 28,
  "city": "Hyderabad",
  "email": "john@gmail.com"
}
```

Expected result: PASS

Reason: All fields match the expected schema.

### Scenario 2: Schema Drift

Input:

```json
{
  "customer_id": 102,
  "customer_name": "Jane Wilson",
  "age": "Thirty Two",
  "city": "Bangalore",
  "email": "jane@gmail.com"
}
```

Expected result: FAIL

Reason: The `age` field changed from integer to string.

## 4. Execution

Run:

```bash
python src/data_quality/schema_validation.py
```

Check the generated report:

```bash
cat reports/schema_validation/schema_report.json
```

## 5. Actual Test Results

| Test | Expected | Observed |
|---|---|---|
| Valid customer record | PASS | PASS |
| Drift customer record | FAIL | FAIL |

## 6. Conclusion

Schema validation successfully accepted the valid customer record and rejected the record containing a changed data type.

The test demonstrates that schema drift can be detected before incompatible data enters downstream processing.
