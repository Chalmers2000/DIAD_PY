# DIAD_PY
Dashboard-in-a-Day re-imagined as pySpark data load instead of Power Query
## One tiny crib
* All the data for DIAD is available as a download from Microsoft's DAID workshop site,
* https://learn.microsoft.com/en-us/training/modules/intro-power-bi/
* However, some of the data is in Microsoft Excel.
* Instead of forcing the use of Pandas libraries to extract from Excel, I have simply done a 'Save As CSV' from the source Excel file, preserving the challenge of removing header and footer rows, etc.
* I have also added a simple Date.csv table for convenience, since the actual workshop creates it with DAX in a later module, and not part of the data ingestion module.

