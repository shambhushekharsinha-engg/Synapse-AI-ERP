import pytest
import pandas as pd
import numpy as np
import os
from datetime import datetime

from ml.ingestion.synthetic_generator import SyntheticERPGenerator
from ml.features.feature_engineering import FeatureEngineer
from ml.pipelines.split import chronological_split
from ml.models.baseline import NaiveForecaster
from ml.models.xgboost_forecaster import XGBoostForecaster
from ml.registry import ModelRegistry
from app.services.forecast import ForecastService

@pytest.fixture(scope="module")
def setup_data():
    gen = SyntheticERPGenerator(seed=42, num_products=2, num_warehouses=1, days=60)
    out_dir = "ml/tests/data"
    gen.run(out_dir)
    return pd.read_csv(f"{out_dir}/synthetic_demand.csv")

def test_synthetic_reproducibility(setup_data):
    gen2 = SyntheticERPGenerator(seed=42, num_products=2, num_warehouses=1, days=60)
    gen2.run("ml/tests/data2")
    df2 = pd.read_csv("ml/tests/data2/synthetic_demand.csv")
    pd.testing.assert_frame_equal(setup_data, df2)

def test_feature_engineering_leakage(setup_data):
    setup_data['date'] = pd.to_datetime(setup_data['date'])
    fe = FeatureEngineer()
    df_features = fe.run(setup_data)
    
    # Check that unknown futures are dropped
    assert 'inventory_level' not in df_features.columns
    assert 'stockout' not in df_features.columns
    
    # Check that they exist as lag_1
    assert 'inventory_level_lag_1' in df_features.columns
    assert 'stockout_lag_1' in df_features.columns

def test_chronological_split(setup_data):
    setup_data['date'] = pd.to_datetime(setup_data['date'])
    fe = FeatureEngineer()
    df_features = fe.run(setup_data)
    
    train, val, test = chronological_split(df_features, train_ratio=0.7, val_ratio=0.15, date_col='date')
    
    assert train['date'].max() < val['date'].min()
    assert val['date'].max() < test['date'].min()

def test_registry_and_service(setup_data):
    fe = FeatureEngineer()
    df_features = fe.run(setup_data)
    train, val, test = chronological_split(df_features, train_ratio=0.7, val_ratio=0.15, date_col='date')
    
    model = XGBoostForecaster()
    model.fit(train, val)
    os.makedirs("ml/artifacts", exist_ok=True)
    model.save("ml/artifacts/xgboost_forecaster.json")
    
    registry = ModelRegistry()
    registry.load_model("xgboost", "ml/artifacts/xgboost_forecaster.json")
    assert registry.get_model("xgboost") is not None
