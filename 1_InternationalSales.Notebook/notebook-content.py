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

# # International Sales
# 1. Create a schema, so we get the datatypes right, like Zip as Text
# 2. Load all the *.csv files in the /Files/InternationalSales folder
# 3. Write a Delta table InternationalSales


# MARKDOWN ********************

# ## 1. Schema and 2. Load


# CELL ********************

from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType, DecimalType

# Define the schema
# True indicates the field is nullable
salesschema = StructType([
    StructField("ProductID", IntegerType(), True),
    StructField("Date", DateType(), True),
    StructField("Zip", StringType(), True),
    StructField("Units", IntegerType(), True),
    StructField("Revenue", DecimalType(10, 2), True),
    StructField("Country", StringType(), True)
])


# Load the CSV file with the defined schema
df = spark.read.csv("Files/InternationalSales/*.csv", schema=salesschema, header=True)

# Show the data
df.show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Verification step
# * Let's double-check that all the files were read

# CELL ********************

# Did we get all the countries? 

row_count = df.count()
print(f"Number of rows: {row_count}")

distinct_countries = df.select("Country").distinct().show()


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 3. Write the Table

# CELL ********************

# Let's write the Delta table

df.write.format("delta").mode("overwrite").saveAsTable("InternationalSales")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

row_count = df.count()
print(f"Number of rows: {row_count}")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
