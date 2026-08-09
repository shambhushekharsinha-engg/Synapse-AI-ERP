import pandas as pd
import numpy as np
import xgboost as xgb
import os
from ml.models.baseline import BaseForecaster

class XGBoostForecaster(BaseForecaster):
    def __init__(self, **kwargs):
        self.model = xgb.XGBRegressor(
            objective='reg:squarederror',
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42,
            early_stopping_rounds=10,
            **kwargs
        )
        self.features = None

    def fit(self, train_df: pd.DataFrame, val_df: pd.DataFrame = None):
        exclude_cols = ['date', 'demand']
        self.features = [c for c in train_df.columns if c not in exclude_cols]
        
        X_train = train_df[self.features]
        y_train = train_df['demand']
        
        if val_df is not None:
            X_val = val_df[self.features]
            y_val = val_df['demand']
            eval_set = [(X_train, y_train), (X_val, y_val)]
            self.model.fit(X_train, y_train, eval_set=eval_set, verbose=False)
        else:
            self.model.fit(X_train, y_train, verbose=False)
            
        return self

    def predict(self, test_df: pd.DataFrame) -> np.ndarray:
        X_test = test_df[self.features]
        return self.model.predict(X_test)
        
    def save(self, filepath: str):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.model.save_model(filepath)
