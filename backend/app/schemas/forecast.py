from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class ForecastPoint(BaseModel):
    date: date
    predicted_demand: float

class ForecastResponse(BaseModel):
    product_id: int
    warehouse_id: Optional[int] = None
    horizon_days: int
    model: str
    model_version: str
    forecast: List[ForecastPoint]
