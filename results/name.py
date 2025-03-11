import pandas as pd

# Load both Excel sheets into Pandas DataFrames
df_main = pd.read_excel("main.xlsx")  # Replace "main.xlsx" with the path to your main Excel file
df_sheet_d = pd.read_excel("sheet_d.xlsx")  # Replace "sheet_d.xlsx" with the path to your Sheet D Excel file

# Remove any leading or trailing whitespaces in both DataFrames
df_main['Column F'] = df_main['Column F'].str.strip()
df_sheet_d['Column D'] = df_sheet_d['Column D'].str.strip()

# Find matching values between the two DataFrames
matches = df_main[df_main['Column F'].isin(df_sheet_d['Column D'])]

# Replace matching values in df_main with NaN (empty cell)
for match in matches['Column F']:
    df_main.loc[df_main['Column F'] == match, 'Column F'] = pd.NA

# Write the modified df_main back to the main Excel file
df_main.to_excel("main_modified.xlsx", index=False)  # Modify the path as needed
