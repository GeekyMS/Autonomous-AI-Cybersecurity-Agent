import os
import pandas as pd

all_files = os.listdir('./archive-2')
csv_files = [f for f in all_files if f.endswith('.csv')]

all_data = []
for file in csv_files:
    file_path = os.path.join('./archive-2', file)
    df = pd.read_csv(file_path)
    all_data.append(df)

combined_df = pd.concat(all_data, ignore_index=True)
combined_df.to_csv('combined_data.csv', index=False)