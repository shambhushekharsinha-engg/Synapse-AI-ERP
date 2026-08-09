import os
from ml.models.xgboost_forecaster import XGBoostForecaster

class ModelRegistry:
    _instance = None
    _models = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelRegistry, cls).__new__(cls)
        return cls._instance

    def load_model(self, name: str, filepath: str):
        if name not in self._models:
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Model artifact not found at {filepath}")
            
            # For now, we only support XGBoostForecaster
            model = XGBoostForecaster()
            model.model.load_model(filepath)
            
            # Note: We must also store the features list used by the model
            # In a real scenario, this should be serialized alongside the model in a JSON envelope.
            # For this MVP, we will derive it from the FeatureEngineer at prediction time or hardcode.
            self._models[name] = model
            print(f"Loaded model {name} from {filepath}")
        return self._models[name]

    def get_model(self, name: str) -> XGBoostForecaster:
        if name not in self._models:
            raise KeyError(f"Model {name} not loaded.")
        return self._models[name]
