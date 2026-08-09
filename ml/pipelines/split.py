import pandas as pd

def chronological_split(df: pd.DataFrame, train_ratio=0.7, val_ratio=0.15, date_col='date'):
    """
    Splits the dataset chronologically into train, validation, and test sets.
    Prevents leakage by ensuring all training data is strictly before validation,
    and all validation is strictly before test, globally across all series.
    """
    df = df.sort_values(by=date_col)
    unique_dates = df[date_col].unique()
    
    n_dates = len(unique_dates)
    train_end_idx = int(n_dates * train_ratio)
    val_end_idx = int(n_dates * (train_ratio + val_ratio))
    
    train_dates = unique_dates[:train_end_idx]
    val_dates = unique_dates[train_end_idx:val_end_idx]
    test_dates = unique_dates[val_end_idx:]
    
    train_df = df[df[date_col].isin(train_dates)]
    val_df = df[df[date_col].isin(val_dates)]
    test_df = df[df[date_col].isin(test_dates)]
    
    return train_df, val_df, test_df
