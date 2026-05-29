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

# # Manufacturer
# 1. Remove bottom 3 rows
# 2. Transpose or Unpivot
# 3. Promote headers
# 4. Add Manufacturer Groups column, conditional column
# 5. Write to Delta


# MARKDOWN ********************

# ## 1, 2, 3: Cleanup and Transpose
# * We're using AI generated code to do all these steps
# * AI decided on "stack" and "pivot" capabilities in Python to turn the table on its side and promote headers

# CELL ********************

# from pyspark.sql import SparkSession
# spark = SparkSession.builder.getOrCreate()


from pyspark.sql.functions import first, col


# 1. Read the CSV. 
#    Make sure header=True so Column1..Column15 become column names.
df = spark.read.option("header", "true").csv("Files/USSales/manufacturer.csv")

# 2. Unpivot the wide columns (Column2..Column15) using stack.
#    We know there are exactly 14 manufacturer columns, so stack(14, ...) is used.
#    The idea is that each row in df currently looks like:
#         Row( Column1="ManufacturerID", Column2="1", Column3="2", ..., Column15="14" )
#         Row( Column1="Manufacturer",   Column2="Contoso, Ltd.", ..., )
#         Row( Column1="Logo",          Column2="http://...", ... )
#    We want to turn columns 2..15 into rows keyed by (ID, val).
#
#    stack(14, 
#        '1', Column2,     # For ID=1, use the value in Column2
#        '2', Column3,
#        ...
#        '14', Column15
#    ) AS (ID, val)
#
#    We'll also keep Column1 so we know whether val belongs to ManufacturerID, Manufacturer, or Logo.
#

df_unpivot = df.selectExpr(
    """
    stack(
        14,
        '1',  Column2,
        '2',  Column3,
        '3',  Column4,
        '4',  Column5,
        '5',  Column6,
        '6',  Column7,
        '7',  Column8,
        '8',  Column9,
        '9',  Column10,
        '10', Column11,
        '11', Column12,
        '12', Column13,
        '13', Column14,
        '14', Column15
    ) as (ID, val)
    """,
    "Column1"
)

# df_unpivot will have rows like:
#  ID   val                        Column1
# ---   -------------------------  -----------
#  1    1                          ManufacturerID
#  2    2                          ManufacturerID
#  ...
#  1    Contoso, Ltd.             Manufacturer
#  2    Tailwind Traders          Manufacturer
#  ...
#  1    https://.../Contoso.png   Logo
#  2    https://.../Tailwind.png  Logo
#  etc.

# 3. Now pivot on Column1 (which has values "ManufacturerID","Manufacturer","Logo"),
#    aggregating with first(val), grouping by ID (which runs from '1'..'14').
df_pivot = (
    df_unpivot
    .groupBy("ID")
    .pivot("Column1")
    .agg(first("val"))
)

# df_pivot will have columns:
#   ID, ManufacturerID, Manufacturer, Logo

# 4. We can select and rename/cast as needed:
final_df = df_pivot.select(
    col("ID").cast("int").alias("ManufacturerID"),
    "Manufacturer",
    "Logo"
)

# Show the final unpivoted DataFrame
# df.show() instead of display(df)

final_df.show(truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 4. Adding a Conditional Column
# * More AI generated code for this
# * AI chose .when and .otherwise methods of df in Python

# CELL ********************

from pyspark.sql.functions import when, col

# Define the conditions for the new column
final_df = final_df.withColumn(
    "ManufacturerGroups",
    when(col("Manufacturer").contains("VanArsdel, Ltd."), "VanArsdel")
    .when(
        col("Manufacturer").rlike(
            "Fabrikam, Inc.|Nod Publishers|Tailwind Traders|Wide World Importers"
        ),
        "Top Competitors",
    )
    .otherwise("Others"),
)

# Show the resulting DataFrame
final_df.show()


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 5. Write to Delta table

# CELL ********************

# Let's write the Delta table

final_df.write.format("delta").mode("overwrite").saveAsTable("Manufacturer")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
