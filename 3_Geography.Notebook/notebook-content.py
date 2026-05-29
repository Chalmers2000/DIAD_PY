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

# # Geography
# 1. Create a schema
# 2. Remove top 3 rows and Load CSV
# 3. Create ZipCountry text column
# 4. Write to Delta table


# MARKDOWN ********************

# ## 1. Create the Schema

# CELL ********************

from pyspark.sql.types import StructType, StructField, StringType

# Define the schema
geoschema = StructType([
    StructField("Zip", StringType(), True),      #  nullable
    StructField("City", StringType(), True),     # Nullable
    StructField("State", StringType(), True),    # Nullable
    StructField("Region", StringType(), True),   # Nullable
    StructField("District", StringType(), True), # Nullable
    StructField("Country", StringType(), True)  #  nullable
])


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 2. Drop top 3 rows and Load CSV with schema

# CELL ********************

from pyspark.sql.functions import col

# Step 1: Read the CSV as a raw DataFrame (treat everything as string initially)
df_raw = spark.read.format("csv").option("header", "false").load("Files/USSales/geo.csv")

# Step 2: Drop the first 3 rows
# Lambda is a python thing for creating an in-line expression you'll only use once
df_trimmed = df_raw.rdd.zipWithIndex().filter(lambda row: row[1] >= 3).map(lambda row: row[0]).toDF()

# Step 3: Extract the new header from the remaining data
new_header = df_trimmed.first()  # The fourth row becomes the new header
df_trimmed = df_trimmed.toDF(*new_header)  # Rename columns using the new header

# Step 4: Read the CSV again, this time enforcing the correct schema
df = df_trimmed.select([col(c).cast(t.dataType) for c, t in zip(df_trimmed.columns, geoschema)])

# Step 5: Display the cleaned DataFrame
display(df)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 3. Add the ZipCountry column

# CELL ********************

# Adding the ZipCountry text column

from pyspark.sql.functions import concat_ws

df = df.withColumn("ZipCountry", concat_ws(",", df["Zip"], df["Country"]))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Verifying the results of the new column

df.select("Zip", "Country", "ZipCountry").show(5)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 4. Write the Delta table

# CELL ********************

# Let's write the Delta table

df.write.format("delta").mode("overwrite").saveAsTable("Geography")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
