from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    StringType,
    DoubleType
)

# 1. Create Spark Session
spark = (
    SparkSession.builder
    .appName("BigDataProcessingPipeline")
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "4")
    .getOrCreate()
)

print("Spark Session Created Successfully")

# 2. Customer Schema
customer_schema = StructType([
    StructField("customer_id", IntegerType(), True),
    StructField("customer_name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("city", StringType(), True),
    StructField("email", StringType(), True)
])

# 3. Product Schema
product_schema = StructType([
    StructField("product_id", IntegerType(), True),
    StructField("product_name", StringType(), True),
    StructField("category", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("stock", IntegerType(), True)
])

# 4. Order Schema
order_schema = StructType([
    StructField("order_id", IntegerType(), True),
    StructField("customer_id", IntegerType(), True),
    StructField("product_id", IntegerType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("order_date", StringType(), True),
    StructField("status", StringType(), True)
])

# 5. Read CSV files
customers_df = (
    spark.read
    .option("header", True)
    .schema(customer_schema)
    .csv("data/raw/customers.csv")
)

products_df = (
    spark.read
    .option("header", True)
    .schema(product_schema)
    .csv("data/raw/products.csv")
)

orders_df = (
    spark.read
    .option("header", True)
    .schema(order_schema)
    .csv("data/raw/orders.csv")
)

# 6. Display datasets
print("\nCUSTOMER DATA")
customers_df.show()

print("\nPRODUCT DATA")
products_df.show()

print("\nORDER DATA")
orders_df.show()

# 7. Display schemas
print("\nCUSTOMER SCHEMA")
customers_df.printSchema()

print("\nPRODUCT SCHEMA")
products_df.printSchema()

print("\nORDER SCHEMA")
orders_df.printSchema()

# 8. Record counts
print("\nRECORD COUNTS")
print("Customers:", customers_df.count())
print("Products:", products_df.count())
print("Orders:", orders_df.count())

# 9. Save as Parquet
customers_df.write.mode("overwrite").parquet(
    "data/processed/customers"
)

products_df.write.mode("overwrite").parquet(
    "data/processed/products"
)

orders_df.write.mode("overwrite").parquet(
    "data/processed/orders"
)

print("\nParquet Files Created Successfully")

# 10. Stop Spark
spark.stop()
