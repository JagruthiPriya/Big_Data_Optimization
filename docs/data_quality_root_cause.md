# Data Quality Root Cause Analysis

## 1. Objective

Document the data-quality issues identified during the Big_Data_Processing pipeline and explain their root causes and handling.

## 2. Data Quality Results

| Check | Invalid Records | Root Cause |
|---|---:|---|
| Invalid customers | 2 | One customer is under 18 and another has a missing name |
| Invalid products | 0 | All product records passed validation |
| Duplicate orders by order ID | 0 | No repeated order IDs were detected |
| Invalid quantities | 2 | One order has negative quantity and another has zero quantity |
| Invalid statuses | 1 | One order contains an unsupported status |
| Unknown customer orders | 1 | An order references a customer ID that does not exist |
| Unknown product orders | 0 | All referenced products exist |

## 3. Root Cause Details

### Invalid Customers
- Customer 105 has age 17, below the minimum allowed age of 18.
- Customer 110 has a missing customer name.
- Both records are flagged for review.

### Invalid Quantities
- Order 313 has quantity -1.
- Order 314 has quantity 0.
- Valid orders must have a quantity greater than zero.

### Invalid Status
- Order 315 has status `Unknown`.
- Supported statuses are Completed, Pending, and Cancelled.

### Unknown Customer Reference
- Order 312 references customer ID 999.
- Customer ID 999 does not exist in the customer dataset.
- This is a referential integrity issue.

## 4. Pipeline Handling

1. Read raw customer, product, and order data.
2. Apply validation rules.
3. Identify invalid and inconsistent records.
4. Store flagged records separately in `data/quality/flagged_records/`.
5. Generate the quality report under `reports/data_quality/quality_report/`.
6. Exclude invalid records from downstream clean-data processing where applicable.

## 5. Recommendations

- Enforce required fields during ingestion.
- Validate customer age and order quantity.
- Restrict order status to approved values.
- Validate customer and product references before joining.
- Monitor data-quality failure counts.
- Investigate flagged records before correcting or reprocessing them.

## 6. Conclusion

The pipeline identified multiple data-quality issues and stored flagged records separately. This helps prevent invalid data from silently affecting downstream analytics and reporting.
