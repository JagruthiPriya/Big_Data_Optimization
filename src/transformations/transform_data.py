from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    trim,
    lower,
    round,
    count,
    sum as spark_sum,
    when
)

# 1. Create Spark Session

spark = (
    SparkSession.builder
    .appName("DataTransformationPipeline")
    .master("local[*]")
    .getOrCreate()
)

print("Spark Transformation Started")

# 2. Read Parquet Files

customers = spark.read.parquet("data/processed/customers")
products = spark.read.parquet("data/processed/products")
orders = spark.read.parquet("data/processed/orders")

# 3. Clean Customer Data

customers_clean = (
    customers
    .filter(col("customer_id").isNotNull())
    .filter(col("customer_name").isNotNull())
    .filter(trim(col("customer_name")) != "")
    .filter(col("age") >= 18)
    .dropDuplicates(["customer_id"])
)

print("\nCLEAN CUSTOMER DATA")
customers_clean.show()

# 4. Clean Product Data

products_clean = (
    products
    .filter(col("product_id").isNotNull())
    .filter(col("product_name").isNotNull())
    .filter(col("price") > 0)
    .filter(col("stock") >= 0)
    .dropDuplicates(["product_id"])
)

print("\nCLEAN PRODUCT DATA")
products_clean.show()

# 5. Remove Duplicate Orders

orders_deduplicated = orders.dropDuplicates(["order_id"])

print(
    "Orders before deduplication:",
    orders.count()
)

print(
    "Orders after deduplication:",
    orders_deduplicated.count()
)

# 6. Clean Orders

valid_statuses = ["Completed", "Pending", "Cancelled"]

orders_clean = (
    orders_deduplicated
    .filter(col("order_id").isNotNull())
    .filter(col("customer_id").isNotNull())
    .filter(col("product_id").isNotNull())
    .filter(col("quantity") > 0)
    .filter(lower(trim(col("status"))).isin(
        [status.lower() for status in valid_statuses]
    ))
)

print("\nCLEAN ORDER DATA")
orders_clean.show()

# 7. Join Customers and Orders

customer_orders = orders_clean.join(
    customers_clean,
    on="customer_id",
    how="inner"
)

# 8. Join Products

sales_data = customer_orders.join(
    products_clean,
    on="product_id",
    how="inner"
)

# 9. Calculate Order Amount

sales_data = sales_data.withColumn(
    "order_amount",
    round(col("quantity") * col("price"), 2)
)

print("\nFINAL SALES DATA")
sales_data.select(
    "order_id",
    "customer_name",
    "product_name",
    "quantity",
    "price",
    "order_amount",
    "status"
).show()

# 10. Sales Summary by Product

product_summary = (
    sales_data
    .groupBy("product_name")
    .agg(
        count("order_id").alias("total_orders"),
        spark_sum("quantity").alias("total_quantity"),
        spark_sum("order_amount").alias("total_sales")
    )
)

print("\nPRODUCT SALES SUMMARY")
product_summary.show()

# 11. Sales Summary by City

city_summary = (
    sales_data
    .groupBy("city")
    .agg(
        count("order_id").alias("total_orders"),
        spark_sum("order_amount").alias("total_sales")
    )
)

print("\nCITY SALES SUMMARY")
city_summary.show()

# 12. Save Cleaned Data

sales_data.write.mode("overwrite").parquet(
    "data/processed/clean_sales"
)

product_summary.write.mode("overwrite").parquet(
    "data/processed/product_summary"
)

city_summary.write.mode("overwrite").parquet(
    "data/processed/city_summary"
)

print("\nTransformation Completed Successfully")

# 13. Stop Spark

spark.stop()
