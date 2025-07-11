import pandas as pd
import os

def save_data(filepath, data_dict):
    df = pd.DataFrame([data_dict])
    if os.path.exists(filepath):
        df_existing = pd.read_csv(filepath)
        df = pd.concat([df_existing, df], ignore_index=True)
    df.to_csv(filepath, index=False)
