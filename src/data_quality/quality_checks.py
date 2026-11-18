from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    trim,
    lower,
    count,
    lit
)

spark = (
    SparkSession.builder
    .appName("DataQualityChecks")
    .master("local[*]")
    .getOrCreate()
)

print("Starting Data Quality Checks")

# Read raw datasets
customers = spark.read.option(
    "header", True
).option("inferSchema", True).csv(
    "data/raw/customers.csv"
)

products = spark.read.option(
    "header", True
).option("inferSchema", True).csv(
    "data/raw/products.csv"
)

orders = spark.read.option(
    "header", True
).option("inferSchema", True).csv(
    "data/raw/orders.csv"
)

# 1. Invalid customers
invalid_customers = customers.filter(
    col("customer_name").isNull()
    | (trim(col("customer_name")) == "")
    | (col("age") < 18)
)

# 2. Invalid products
invalid_products = products.filter(
    col("product_name").isNull()
    | (trim(col("product_name")) == "")
    | (col("price") <= 0)
    | (col("stock") < 0)
)

# 3. Duplicate orders
duplicate_orders = orders.groupBy(
    "order_id"
).agg(
    count("*").alias("record_count")
).filter(
    col("record_count") > 1
)

# 4. Invalid order quantities
invalid_quantities = orders.filter(
    col("quantity").isNull()
    | (col("quantity") <= 0)
)

# 5. Invalid order statuses
valid_statuses = ["completed", "pending", "cancelled"]

invalid_statuses = orders.filter(
    ~lower(trim(col("status"))).isin(valid_statuses)
    | col("status").isNull()
)

# 6. Orders with unknown customers
invalid_customer_orders = orders.join(
    customers.select("customer_id"),
    on="customer_id",
    how="left_anti"
)

# 7. Orders with unknown products
invalid_product_orders = orders.join(
    products.select("product_id"),
    on="product_id",
    how="left_anti"
)

# Print results
checks = [
    ("Invalid Customers", invalid_customers),
    ("Invalid Products", invalid_products),
    ("Duplicate Orders", duplicate_orders),
    ("Invalid Quantities", invalid_quantities),
    ("Invalid Statuses", invalid_statuses),
    ("Unknown Customer Orders", invalid_customer_orders),
    ("Unknown Product Orders", invalid_product_orders)
]

print("\nDATA QUALITY RESULTS")

report_rows = []

for check_name, dataframe in checks:

    issue_count = dataframe.count()

    print(f"{check_name}: {issue_count}")

    report_rows.append(
        (check_name, issue_count,
         "PASS" if issue_count == 0 else "FAIL")
    )

    dataframe.write.mode("overwrite").parquet(
        f"data/quality/flagged_records/{check_name.lower().replace(' ', '_')}"
    )

# Create quality report
report = spark.createDataFrame(
    report_rows,
    ["check_name", "issue_count", "result"]
)

report.show(truncate=False)

report.coalesce(1).write.mode(
    "overwrite"
).option("header", True).csv(
    "reports/data_quality/quality_report"
)

print("\nQuality report saved")
print("Flagged records saved")
print("Data Quality Checks Completed")

spark.stop()
