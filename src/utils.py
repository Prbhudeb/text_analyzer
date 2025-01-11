import pandas as pd

def get_value(df, column_name):
    if column_name in df.columns:  # Check if the column exists
        value = df[column_name].iloc[0] if not pd.isnull(df[column_name].iloc[0]) else 0
        return float(value)
    return 0  # Default to 0 if column doesn't exist

def get_value_from_dict(data_dict, key):
    value = data_dict.get(key, 0)  # Get the value, default to 0 if the key is missing
    return float(value) if value is not None else 0  # Convert to float if not None