from pydantic import BaseModel
from typing import Optional, List

class SupplierScoreResponse(BaseModel):
    supplier_id: int
    score: float
    rating: str # "EXCELLENT", "GOOD", "FAIR", "POOR"
    on_time_rate: float
    avg_lead_time_days: float
    delay_rate: float

class SupplierLeadTimeAnalytics(BaseModel):
    supplier_id: int
    average_lead_time: float
    median_lead_time: float
    standard_deviation: float
    minimum: float
    maximum: float
    delay_frequency: float

class SupplierDelayRiskResponse(BaseModel):
    supplier_id: int
    risk_level: str # "HIGH", "MEDIUM", "LOW"
    risk_factors: List[str]

class SupplierComparisonProduct(BaseModel):
    supplier_id: int
    supplier_name: str
    avg_lead_time: float
    on_time_rate: float
    delay_rate: float
    avg_order_qty: float
    score: float

class SupplierComparisonResponse(BaseModel):
    product_id: int
    suppliers: List[SupplierComparisonProduct]
