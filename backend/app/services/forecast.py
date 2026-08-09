import pandas as pd
from datetime import datetime, timedelta
from typing import List, Optional
from ml.registry import ModelRegistry
from ml.features.feature_engineering import FeatureEngineer
from app.schemas.forecast import ForecastResponse, ForecastPoint

class ForecastService:
    def __init__(self, model_registry: ModelRegistry):
        self.registry = model_registry
        self.feature_engineer = FeatureEngineer()
        
    def get_forecast(self, product_id: int, warehouse_id: Optional[int], horizon_days: int) -> ForecastResponse:
        # 1. Fetch Model
        try:
            model = self.registry.get_model("xgboost")
        except KeyError:
            raise RuntimeError("Model 'xgboost' is not currently loaded or available.")

        # 2. Fetch Historical Data
        # In a real system, this queries the PostgreSQL database for the last ~60 days of demand.
        # For this MVP, we load the synthetic CSV to mock the DB fetch.
        data_path = "../ml/data/synthetic/synthetic_demand.csv"
        try:
            df = pd.read_csv(data_path)
        except Exception:
            raise RuntimeError("Historical data could not be loaded for feature engineering.")
            
        df['date'] = pd.to_datetime(df['date'])
        
        if warehouse_id is None:
            # Default to warehouse 1 if none provided
            warehouse_id = df['warehouse_id'].unique()[0]
            
        # Validate Product/Warehouse exist
        subset = df[(df['product_id'] == product_id) & (df['warehouse_id'] == warehouse_id)].copy()
        if subset.empty:
            raise ValueError(f"No historical data found for product {product_id} at warehouse {warehouse_id}.")

        # 3. Engineer Features (using the EXACT same logic as training)
        df_features = self.feature_engineer.run(subset)
        
        # 4. Generate Future Dates and Predict
        # We need to construct a dummy test DataFrame that mimics the horizon.
        # In a real autoregressive system, we'd iteratively predict and shift.
        # For this Gate 5 MVP, we will grab the last row's features and assume they hold, 
        # or properly construct future features. To keep it robust without retraining, 
        # we'll just predict using the last known feature state for simplicity, 
        # but output varying dates.
        
        last_row = df_features.iloc[[-1]].copy()
        
        # Check if the model has a cached features list
        if model.features:
            features = model.features
        else:
            exclude_cols = ['date', 'demand']
            features = [c for c in df_features.columns if c not in exclude_cols]
            
        X = last_row[features]
        # In real life, we predict multiple steps. Here we'll just duplicate the row for the horizon 
        # (Naive autoregression simulation just for API structure)
        X_horizon = pd.concat([X] * horizon_days, ignore_index=True)
        
        preds = model.model.predict(X_horizon)
        
        # 5. Format Response
        last_date = subset['date'].max()
        forecast_points = []
        for i in range(horizon_days):
            target_date = last_date + timedelta(days=i+1)
            # Ensure no negative predictions
            pred_val = max(0.0, float(preds[i]))
            forecast_points.append(ForecastPoint(
                date=target_date.date(),
                predicted_demand=round(pred_val, 2)
            ))
            
        return ForecastResponse(
            product_id=product_id,
            warehouse_id=warehouse_id,
            horizon_days=horizon_days,
            model="xgboost",
            model_version="v1.0.0",
            forecast=forecast_points
        )
