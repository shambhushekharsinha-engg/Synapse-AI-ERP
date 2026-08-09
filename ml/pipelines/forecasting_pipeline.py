import pandas as pd
from ml.models.baseline import NaiveForecaster, MovingAverageForecaster, SeasonalNaiveForecaster
from ml.models.xgboost_forecaster import XGBoostForecaster
from ml.evaluation.metrics import evaluate_forecast
from ml.pipelines.split import chronological_split
from ml.features.feature_engineering import FeatureEngineer
import sys
import os

def load_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'])
    return df

def run_pipeline():
    data_path = "ml/data/synthetic/synthetic_demand.csv"
    if not os.path.exists(data_path):
        print(f"Error: Data not found at {data_path}. Run synthetic generator first.")
        sys.exit(1)
        
    df = load_data(data_path)
    
    # Feature Engineering
    print("Engineering features...")
    fe = FeatureEngineer()
    df_features = fe.run(df)
    
    # Chronological Split
    print("Performing chronological global split...")
    train, val, test = chronological_split(df_features, train_ratio=0.7, val_ratio=0.15, date_col='date')
    
    print(f"Train dates: {train['date'].min().date()} to {train['date'].max().date()} ({len(train)} rows)")
    print(f"Val dates:   {val['date'].min().date()} to {val['date'].max().date()} ({len(val)} rows)")
    print(f"Test dates:  {test['date'].min().date()} to {test['date'].max().date()} ({len(test)} rows)")
    
    # We will evaluate for a single product-warehouse combination as a representative test
    product_id = test['product_id'].iloc[0]
    warehouse_id = test['warehouse_id'].iloc[0]
    
    # Filter the split sets for this combination to evaluate the baseline forecasters
    mask_train = (train['product_id'] == product_id) & (train['warehouse_id'] == warehouse_id)
    mask_val = (val['product_id'] == product_id) & (val['warehouse_id'] == warehouse_id)
    mask_test = (test['product_id'] == product_id) & (test['warehouse_id'] == warehouse_id)
    
    train_subset = train[mask_train].copy()
    val_subset = val[mask_val].copy()
    test_subset = test[mask_test].copy()
    
    horizon = len(test_subset)
    y_test = test_subset['demand'].values
    
    # XGBoost handles all series natively, but we'll train it on the global set
    print("\nTraining XGBoost Forecaster on global dataset...")
    xgb_model = XGBoostForecaster()
    xgb_model.fit(train, val)
    # Predict for the specific subset
    xgb_preds = xgb_model.predict(test_subset)
    
    models = {
        "Naive": NaiveForecaster(),
        "MovingAverage (7)": MovingAverageForecaster(window=7),
        "SeasonalNaive (7)": SeasonalNaiveForecaster(season_length=7)
    }
    
    print(f"\n--- Model Comparison for Product {product_id} at Warehouse {warehouse_id} ---")
    
    results = []
    
    # Evaluate Baselines
    for name, model in models.items():
        # Fit on combined train + val subset
        combined_train = pd.concat([train_subset, val_subset])
        model.fit(combined_train)
        preds = model.predict(horizon)
        metrics = evaluate_forecast(y_test, preds)
        metrics['Model'] = name
        results.append(metrics)
        
    # Evaluate XGBoost
    xgb_metrics = evaluate_forecast(y_test, xgb_preds)
    xgb_metrics['Model'] = 'XGBoost'
    results.append(xgb_metrics)
        
    results_df = pd.DataFrame(results).set_index('Model')
    print(results_df.to_markdown())

if __name__ == "__main__":
    run_pipeline()
