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

# # Sales
# 1. Define schema
# 2. Load CSV
# 3. Populate Country field with "USA"
# 4. Load InternationalSales into a dataframe, and append
# 5. Add the ZipCountry column as text
# 6. Write to Delta table


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
df = spark.read.csv("Files/USSales/Sales.csv", schema=salesschema, header=True)

# Show the data
df.show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Verify the load worked properly
# * Quickly double-check the file

# CELL ********************

# Did we get all the data? 

row_count = df.count()
print(f"Number of rows: {row_count}")

distinct_countries = df.select("Zip").distinct().show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 3. Populate the "USA" values in Country column

# CELL ********************

# Populate the Country column with USA

from pyspark.sql.functions import lit

# Populate the 'Country' field with "USA"
df = df.withColumn("Country", lit("USA"))

# Show the updated data
df.show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 4. Append the InternationalSales table to the Sales table
# 1. Load the df_intl dataframe

# CELL ********************

# Load the InternationalSales table into a second dataframe

df_intl = spark.sql("SELECT * FROM DIAD_PY.internationalsales")
display(df_intl)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Append the df_intl dataframe to the df dataframe
# Union only works here because both df and df_intl have the exact same schema

df = df.union(df_intl)

display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Verify the Union worked

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

# ## 5. Add the Calculated column ZipCountry

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

# ## 6. Write the Delta table

# CELL ********************

# Let's write the Delta table

df.write.format("delta").mode("overwrite").saveAsTable("Sales")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
