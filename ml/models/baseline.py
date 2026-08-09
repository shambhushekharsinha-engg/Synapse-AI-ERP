import pandas as pd
import numpy as np

class BaseForecaster:
    def fit(self, train_df: pd.DataFrame):
        raise NotImplementedError

    def predict(self, horizon: int) -> np.ndarray:
        raise NotImplementedError

class NaiveForecaster(BaseForecaster):
    def __init__(self):
        self.last_value = None

    def fit(self, train_df: pd.DataFrame):
        # Assumes train_df is sorted chronologically
        self.last_value = train_df['demand'].iloc[-1]
        return self

    def predict(self, horizon: int) -> np.ndarray:
        return np.full(horizon, self.last_value)

class MovingAverageForecaster(BaseForecaster):
    def __init__(self, window: int = 7):
        self.window = window
        self.mean_value = None

    def fit(self, train_df: pd.DataFrame):
        self.mean_value = train_df['demand'].iloc[-self.window:].mean()
        return self

    def predict(self, horizon: int) -> np.ndarray:
        return np.full(horizon, self.mean_value)

class SeasonalNaiveForecaster(BaseForecaster):
    def __init__(self, season_length: int = 7):
        self.season_length = season_length
        self.last_season = None

    def fit(self, train_df: pd.DataFrame):
        self.last_season = train_df['demand'].iloc[-self.season_length:].values
        return self

    def predict(self, horizon: int) -> np.ndarray:
        repeats = int(np.ceil(horizon / self.season_length))
        tiled = np.tile(self.last_season, repeats)
        return tiled[:horizon]
