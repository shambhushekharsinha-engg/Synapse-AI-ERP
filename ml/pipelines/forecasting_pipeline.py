import pandas as pd
from ml.models.baseline import NaiveForecaster, MovingAverageForecaster, SeasonalNaiveForecaster
from ml.evaluation.metrics import evaluate_forecast
import sys
import os

def load_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'])
    return df.sort_values(by='date')

def chronological_split(df: pd.DataFrame, train_ratio=0.7, val_ratio=0.15):
    # Sort chronologically to prevent leakage
    df = df.sort_values(by='date')
    
    n = len(df)
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))
    
    train = df.iloc[:train_end]
    val = df.iloc[train_end:val_end]
    test = df.iloc[val_end:]
    
    return train, val, test

def run_baseline_pipeline():
    data_path = "ml/data/synthetic/synthetic_demand.csv"
    if not os.path.exists(data_path):
        print(f"Error: Data not found at {data_path}. Run synthetic generator first.")
        sys.exit(1)
        
    df = load_data(data_path)
    
    # We will evaluate for a single product-warehouse combination as a test
    product_id = df['product_id'].iloc[0]
    warehouse_id = df['warehouse_id'].iloc[0]
    
    subset = df[(df['product_id'] == product_id) & (df['warehouse_id'] == warehouse_id)].copy()
    
    train, val, test = chronological_split(subset)
    horizon = len(test)
    y_test = test['demand'].values
    
    models = {
        "Naive": NaiveForecaster(),
        "MovingAverage (7)": MovingAverageForecaster(window=7),
        "SeasonalNaive (7)": SeasonalNaiveForecaster(season_length=7)
    }
    
    print(f"--- Baseline Evaluation for Product {product_id} at Warehouse {warehouse_id} ---")
    print(f"Train size: {len(train)}, Val size: {len(val)}, Test size: {horizon}\n")
    
    results = []
    for name, model in models.items():
        # Fit on combined train + val for test evaluation
        combined_train = pd.concat([train, val])
        model.fit(combined_train)
        
        preds = model.predict(horizon)
        metrics = evaluate_forecast(y_test, preds)
        
        metrics['Model'] = name
        results.append(metrics)
        
    results_df = pd.DataFrame(results).set_index('Model')
    print(results_df.to_markdown())

if __name__ == "__main__":
    run_baseline_pipeline()
