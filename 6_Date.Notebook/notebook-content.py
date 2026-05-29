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

# # Date
# 1. Load CSV file with Date type column
# 2. Add columns for Year, Quarter, Month, MonthNo
# 3. Write to Delta

# MARKDOWN ********************

# ## 1. Load from CSV

# CELL ********************

# from pyspark.sql import SparkSession
# Initialize Spark session
# spark = SparkSession.builder.appName("DateTable").getOrCreate()


from pyspark.sql.functions import col
from pyspark.sql.types import DateType

# Load CSV with header option
df = spark.read.format("csv").option("header", "true").load("Files/USSales/Date.csv")

# Assuming the column name is 'date', cast it explicitly to DateType
df = df.withColumn("date", col("date").cast(DateType()))

# Display DataFrame
df.show()


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 2. Extending the Date table
# * Adding Year, Quarter, Month, Day of Month, Month Name
# * Also explicitly asking to see the schema to ensure the types were created properly

# CELL ********************

from pyspark.sql.functions import col, year, quarter, month, dayofmonth, date_format
from pyspark.sql.types import DateType

# Add new date-related columns
df = df.withColumn("Year", year(col("date"))) \
       .withColumn("Quarter", quarter(col("date"))) \
       .withColumn("MonthName", date_format(col("date"), "MMMM")) \
       .withColumn("MonthNumber", month(col("date"))) \
       .withColumn("DayNumber", dayofmonth(col("date")))

# Display DataFrame
df.show()

# Print schema to verify column types
df.printSchema()


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 3. Write to Delta table

# CELL ********************

# Write the output to a Delta table

df.write.format("delta").mode("overwrite").saveAsTable("Date")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
