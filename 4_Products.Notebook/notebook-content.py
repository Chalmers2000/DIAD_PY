# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "1ab2288d-f800-4bcd-9d15-7c411f5885ca",
# META       "default_lakehouse_name": "DIAD_PY",
# META       "default_lakehouse_workspace_id": "b32dbcae-7841-4ecd-80a9-3ff5332da28f",
# META       "known_lakehouses": []
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Products
# 1. Define Schema
# 2. Load CSV
# 3. Category - Fill Down
# 4. Product column - Split into "Product" and "Segment" columns
# 5. Price column - Split into "Currency" and "MSRP" columns
# 6. Write Delta table


# MARKDOWN ********************

# ## 1. Create Schema

# CELL ********************

from pyspark.sql.types import StructType, StructField, IntegerType, StringType

# Define the schema for products.csv
products_schema = StructType([
    StructField("ProductID", IntegerType(), False),   # Not nullable (assuming ProductID is always present)
    StructField("Product", StringType(), True),      # Nullable text field
    StructField("Category", StringType(), True),     # Nullable text field
    StructField("ManufacturerID", IntegerType(), True), # Nullable integer field
    StructField("Price", StringType(), True)        # Stored as text (string)
])


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 2. Load CSV

# CELL ********************

df = spark.read.format("csv") \
    .option("header", "true") \
    .schema(products_schema) \
    .load("Files/USSales/products.csv")  # Ensure no trailing backslash here

# Display the DataFrame
display(df)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 3. Split Product column

# CELL ********************

# Split the Product column into Product and Segment

from pyspark.sql.functions import split

# Split the "Product" column into "Product" and "Segment"
df = df.withColumn("Segment", split(df["Product"], "\|")[1]) \
       .withColumn("Product", split(df["Product"], "\|")[0])  # Overwrite "Product" column

# Display the updated DataFrame
display(df)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 4. Fill Down "Category" column

# CELL ********************

# Fill Down the Category column

from pyspark.sql.window import Window
from pyspark.sql.functions import last

# Define a window that orders rows naturally
window_spec = Window.orderBy("ProductID").rowsBetween(Window.unboundedPreceding, 0)

# Fill down the Category column
df = df.withColumn("Category", last("Category", ignorenulls=True).over(window_spec))

# Display the updated DataFrame
display(df)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 5. Split Price column

# CELL ********************

# Split the Price column into "Currency" and "MSRP"

from pyspark.sql.functions import split, regexp_replace
from pyspark.sql.types import DecimalType

# Split the "Price" column into Currency and MSRP
df = df.withColumn("Currency", split(df["Price"], " ")[0]) \
       .withColumn("MSRP", regexp_replace(split(df["Price"], " ")[1], ",", "").cast(DecimalType(10,2))) \
       .drop("Price")  # Remove the original "Price" column

# Display the updated DataFrame
display(df)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 6. Write Delta table

# CELL ********************

# Let's write the Delta table

df.write.format("delta").mode("overwrite").saveAsTable("Products")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
