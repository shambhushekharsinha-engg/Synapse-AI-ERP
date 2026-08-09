import pandas as pd
import numpy as np

class FeatureEngineer:
    def __init__(self):
        pass
        
    def add_temporal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['date'] = pd.to_datetime(df['date'])
        df['day_of_week'] = df['date'].dt.dayofweek
        df['month'] = df['date'].dt.month
        df['week_of_year'] = df['date'].dt.isocalendar().week.astype(int)
        df['year'] = df['date'].dt.year
        df['quarter'] = df['date'].dt.quarter
        
        # Simple holiday indicator (using day_of_year logic from synthetic gen as proxy)
        df['day_of_year'] = df['date'].dt.dayofyear
        df['is_holiday_season'] = df['day_of_year'].apply(lambda x: 1 if 320 <= x <= 360 else 0)
        return df

    def add_lag_and_rolling_features(self, df: pd.DataFrame, target_col: str = 'demand') -> pd.DataFrame:
        """
        Creates lag and rolling features.
        Assumes df is sorted chronologically and grouped by product and warehouse.
        """
        df = df.copy()
        
        # Lags
        lags = [1, 7, 14, 28]
        for lag in lags:
            df[f'lag_{lag}'] = df.groupby(['product_id', 'warehouse_id'])[target_col].shift(lag)
            
        # Rolling features
        windows = [7, 28]
        for window in windows:
            # We must shift by 1 before rolling to avoid data leakage!
            shifted = df.groupby(['product_id', 'warehouse_id'])[target_col].shift(1)
            df[f'rolling_mean_{window}'] = shifted.groupby([df['product_id'], df['warehouse_id']]).rolling(window=window, min_periods=1).mean().reset_index(level=[0,1], drop=True)
            if window == 28:
                df[f'rolling_std_{window}'] = shifted.groupby([df['product_id'], df['warehouse_id']]).rolling(window=window, min_periods=1).std().reset_index(level=[0,1], drop=True)
                
        # Fill NAs introduced by lags
        df.fillna(0, inplace=True)
        return df
        
    def add_business_and_supply_features(self, df: pd.DataFrame) -> pd.DataFrame:
        # In this dataset, price, promotion, lead_time, supplier_delay are already present
        # But we could engineer ratios or indicators here if needed.
        # For XGBoost, categorical encoding might be needed, but XGBoost can handle them natively if typed as category
        return df

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.add_temporal_features(df)
        df = self.add_lag_and_rolling_features(df)
        df = self.add_business_and_supply_features(df)
        return df
