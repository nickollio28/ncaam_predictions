import pandas as pd
from ast import literal_eval

file_path = 'kenpom_archive_data\data_2024-03-10_18-05-50.csv'

df = pd.read_csv(file_path)

df['data'] = df['data'].apply(lambda x: literal_eval(x) if isinstance(x, str) else x)

# Explode the DataFrame so each dictionary in the list becomes a separate row
df_exploded = df.explode('data')

# Convert the dictionaries in the 'data' column to separate columns
# This step assumes 'data' is now a column of dictionaries after explosion
df_final = pd.json_normalize(df_exploded['data'])

print(df_final)

