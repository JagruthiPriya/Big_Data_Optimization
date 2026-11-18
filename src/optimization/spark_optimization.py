from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    broadcast,
    sum as spark_sum
)
from pyspark.storagelevel import StorageLevel
import time

# 1. Create Spark Session
spark = (
    SparkSession.builder
    .appName("SparkPerformanceOptimization")
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "4")
    .config("spark.sql.adaptive.enabled", "true")
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
    .getOrCreate()
)

print("Spark Optimization Started")

# 2. Read datasets
sales = spark.read.parquet("data/processed/clean_sales")
products = spark.read.parquet("data/processed/products")

# 3. Partitioning
partitioned_sales = sales.repartition(4, col("city"))

print("\nPARTITIONING")
print("Number of partitions:", partitioned_sales.rdd.getNumPartitions())

# Save partitioned data
partitioned_sales.write.mode("overwrite").partitionBy(
    "city"
).parquet("data/processed/partitioned_sales")

print("Partitioned data saved")

# 4. Caching
print("\nCACHING")

partitioned_sales.persist(StorageLevel.MEMORY_AND_DISK)

start = time.time()
partitioned_sales.count()
first_time = time.time() - start

start = time.time()
partitioned_sales.count()
second_time = time.time() - start

print("First execution:", round(first_time, 3), "seconds")
print("Second execution:", round(second_time, 3), "seconds")

# 5. Broadcast Join
print("\nBROADCAST JOIN")

broadcast_result = sales.join(
    broadcast(products),
    on="product_id",
    how="inner"
)

broadcast_result.show()

# 6. AQE Configuration
print("\nADAPTIVE QUERY EXECUTION")

print(
    "AQE enabled:",
    spark.conf.get("spark.sql.adaptive.enabled")
)

# 7. Explain execution plan
broadcast_result.explain("formatted")

# 8. Aggregation
summary = (
    broadcast_result
    .groupBy("city")
    .agg(
        spark_sum("order_amount").alias("total_sales")
    )
)

summary.show()

# 9. Release cached data
partitioned_sales.unpersist()

print("\nSpark Optimization Completed")

spark.stop()
