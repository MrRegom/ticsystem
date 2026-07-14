import pandas as pd
import json

file_path = r'c:\proyectos\ticsystem\doccs\Entrega equipos Marga_Marga PISOS.xlsx'
xl = pd.ExcelFile(file_path)
print(f"Sheet names: {xl.sheet_names}")

# Read first sheet
df = xl.parse(xl.sheet_names[0])
print(f"Columns: {df.columns.tolist()}")

# Print first 2 rows
print(df.head(2).to_json(orient='records', force_ascii=False))
