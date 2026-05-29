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
# META       "known_lakehouses": [
# META         {
# META           "id": "1ab2288d-f800-4bcd-9d15-7c411f5885ca"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!

df = spark.sql("SELECT * FROM DIAD_PY.sales")
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#### ATTENTION: AI-generated code can include errors or operations you didn't intend. Review the code in this cell carefully before running it.

# Describe the schema of df
df.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_products = spark.sql("SELECT * FROM DIAD_PY.products LIMIT 1000")
display(df_products)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Create a new dataframe df_productsales by performing a left outer join on df and df_products on the ProductID column
# df = spark.read.table("df")
# df_products = spark.read.table("df_products")

# Perform the left outer join
df_productsales = df.join(df_products, df.ProductID == df_products.ProductID, "left_outer")

# Display the new dataframe
display(df_productsales)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#### ATTENTION: AI-generated code can include errors or operations you didn't intend. Review the code in this cell carefully before running it.

# Get the number of rows in df_productsales
num_rows = df_productsales.count()
print(f'The number of rows in df_productsales: {num_rows}')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#### ATTENTION: AI-generated code can include errors or operations you didn't intend. Review the code in this cell carefully before running it.

# Filter the dataframe for product "Currus RP-11" and sum the revenue
revenue_sum = df_productsales.filter(df_productsales.Product == "Currus RP-11").groupBy().sum("Revenue").collect()[0][0]
print(f'The sum of revenue where product is "Currus RP-11": {revenue_sum}')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#### ATTENTION: AI-generated code can include errors or operations you didn't intend. Review the code in this cell carefully before running it.

import matplotlib.pyplot as plt

# Filter the dataframe for product "Currus RP-11"
df_filtered = df_productsales.filter(df_productsales.Product == "Currus RP-11")

# Convert to Pandas DataFrame for plotting
pandas_df = df_filtered.select("Units").toPandas()

# Create histogram
plt.figure(figsize=(10, 6))
plt.hist(pandas_df["Units"], bins=30, edgecolor='black', alpha=0.7)
plt.title('Histogram of Unit Sales for Product "Currus RP-11"')
plt.xlabel('Units Sold')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#### ATTENTION: AI-generated code can include errors or operations you didn't intend. Review the code in this cell carefully before running it.

import matplotlib.pyplot as plt

# Filter the dataframe for product "Currus RP-11"
df_filtered = df_productsales.filter(df_productsales.Product == "Currus RP-11")

# Convert to Pandas DataFrame for plotting
pandas_df = df_filtered.select("Units").toPandas()

# Create boxplot
plt.figure(figsize=(10, 6))
plt.boxplot(pandas_df["Units"], vert=True, patch_artist=True)
plt.title('Boxplot of Units Sold for Product "Currus RP-11"')
plt.ylabel('Units Sold')
plt.grid(True)
plt.show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
